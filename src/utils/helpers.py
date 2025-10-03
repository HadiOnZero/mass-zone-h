#!/usr/bin/env python3
"""
Helper Functions for Zone-H Mass Mirror Tool
Utility functions untuk validasi, sanitasi, dan operasi file
Author: Hadi Ramdhani
"""

import os
import json
import csv
from urllib.parse import urlparse
from datetime import datetime


def validate_url(url):
    """Validasi format URL"""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False


def sanitize_url(url):
    """Sanitasi URL untuk keamanan"""
    # Remove potentially dangerous characters
    dangerous_chars = ['<', '>', '"', "'", '&', '%', '$', '#', '{', '}', '[', ']', '\\', '^', '`']
    for char in dangerous_chars:
        url = url.replace(char, '')
    return url.strip()


def extract_domain(url):
    """Ekstrak domain dari URL"""
    try:
        parsed = urlparse(url)
        return parsed.netloc
    except:
        return ''


def get_url_info(url):
    """Dapatkan informasi dasar tentang URL"""
    try:
        parsed = urlparse(url)
        return {
            'scheme': parsed.scheme,
            'domain': parsed.netloc,
            'path': parsed.path,
            'full_url': url
        }
    except:
        return {'error': 'Invalid URL'}


def save_results_to_json(results, filename):
    """Simpan hasil ke file JSON"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error saving JSON: {e}")
        return False


def save_results_to_csv(results, filename):
    """Simpan hasil ke file CSV"""
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            if results:
                fieldnames = results[0].keys()
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(results)
        return True
    except Exception as e:
        print(f"Error saving CSV: {e}")
        return False


def load_urls_from_file(filename):
    """Load URLs dari file text"""
    urls = []
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    urls.append(line)
        return urls
    except Exception as e:
        print(f"Error loading URLs: {e}")
        return []


def calculate_success_rate(results):
    """Hitung tingkat keberhasilan"""
    if not results:
        return 0
    
    success_count = sum(1 for r in results if r.get('status') == 'Success')
    return (success_count / len(results)) * 100


def generate_report(results):
    """Generate laporan dari hasil"""
    if not results:
        return "No results to report"
    
    total = len(results)
    success = sum(1 for r in results if r.get('status') == 'Success')
    failed = total - success
    success_rate = (success / total) * 100 if total > 0 else 0
    
    report = f"""
🛡️ ZONE-H MASS MIRROR REPORT
═══════════════════════════════════════

📊 STATISTICS:
• Total URLs: {total}
• Successful: {success}
• Failed: {failed}
• Success Rate: {success_rate:.1f}%

⏰ Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

🔍 DETAILED RESULTS:
"""
    
    for i, result in enumerate(results, 1):
        status = result.get('status', 'Unknown')
        url = result.get('url', 'N/A')
        status_code = result.get('status_code', 'N/A')
        title = result.get('title', 'N/A')
        timestamp = result.get('timestamp', 'N/A')
        
        report += f"\n{i}. {url}\n"
        report += f"   Status: {status} (Code: {status_code})\n"
        report += f"   Title: {title}\n"
        report += f"   Time: {timestamp}\n"
    
    return report