#!/usr/bin/env python3
"""
Mobile Helper Functions for Zone-H Mobile Mirror Tool
Utility functions untuk validasi, sanitasi, dan operasi file di mobile
Author: Hadi Ramdhani
"""

import os
import json
import csv
from urllib.parse import urlparse
from datetime import datetime


def validate_url_mobile(url):
    """Validasi format URL untuk mobile"""
    try:
        if not url or not isinstance(url, str):
            return False
            
        # Add protocol if missing
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url
            
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False


def sanitize_url_mobile(url):
    """Sanitasi URL untuk keamanan di mobile"""
    if not url:
        return ""
        
    # Remove whitespace and dangerous characters
    url = url.strip()
    
    # Remove potentially dangerous characters
    dangerous_chars = ['<', '>', '"', "'", '&', '%', '$', '#', '{', '}', '[', ']', '\\', '^', '`']
    for char in dangerous_chars:
        url = url.replace(char, '')
    
    # Add protocol if missing
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
        
    # Remove trailing slash
    url = url.rstrip('/')
    
    return url


def extract_domain_mobile(url):
    """Ekstrak domain dari URL untuk mobile"""
    try:
        parsed = urlparse(url)
        return parsed.netloc
    except:
        return ''


def get_url_info_mobile(url):
    """Dapatkan informasi dasar tentang URL untuk mobile"""
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


def save_results_to_json_mobile(results, filename=None):
    """Simpan hasil ke file JSON untuk mobile"""
    if not filename:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"mobile_mirror_results_{timestamp}.json"
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        return filename
    except Exception as e:
        raise Exception(f"Failed to save JSON: {str(e)}")


def save_results_to_csv_mobile(results, filename=None):
    """Simpan hasil ke file CSV untuk mobile"""
    if not filename:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"mobile_mirror_results_{timestamp}.csv"
    
    if not results:
        raise Exception("No results to export")
    
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['url', 'status', 'status_code', 'title', 'timestamp']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)
        return filename
    except Exception as e:
        raise Exception(f"Failed to save CSV: {str(e)}")


def load_urls_from_file_mobile(filepath):
    """Load URLs dari file text untuk mobile"""
    urls = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    urls.append(line)
        return urls
    except Exception as e:
        raise Exception(f"Failed to load URLs: {str(e)}")


def calculate_success_rate_mobile(results):
    """Hitung tingkat keberhasilan untuk mobile"""
    if not results:
        return 0.0
    
    success_count = sum(1 for r in results if r.get('status') == 'Success')
    return (success_count / len(results)) * 100


def generate_mobile_report(results):
    """Generate laporan dari hasil untuk mobile"""
    if not results:
        return "No results to report"
    
    total = len(results)
    success = sum(1 for r in results if r.get('status') == 'Success')
    failed = total - success
    success_rate = (success / total) * 100 if total > 0 else 0
    
    report = f"""📱 ZONE-H MOBILE MIRROR REPORT
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


def format_timestamp_mobile(timestamp=None):
    """Format timestamp untuk mobile"""
    if timestamp is None:
        timestamp = datetime.now()
    return timestamp.strftime('%Y-%m-%d %H:%M:%S')


def check_network_status():
    """Check network status untuk mobile"""
    try:
        import socket
        # Try to connect to a reliable host
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True
    except (socket.error, OSError):
        return False


def get_file_size_mobile(filepath):
    """Get file size in human readable format untuk mobile"""
    try:
        size = os.path.getsize(filepath)
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"
    except:
        return "Unknown"


# Export functions
__all__ = [
    'validate_url_mobile', 'sanitize_url_mobile', 'extract_domain_mobile', 
    'get_url_info_mobile', 'save_results_to_json_mobile', 'save_results_to_csv_mobile',
    'load_urls_from_file_mobile', 'calculate_success_rate_mobile', 'generate_mobile_report',
    'format_timestamp_mobile', 'check_network_status', 'get_file_size_mobile'
]