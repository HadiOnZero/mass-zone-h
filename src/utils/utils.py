#!/usr/bin/env python3
"""
Utility functions for Zone-H Mass Mirror Tool
Contains helper functions for URL validation, file operations, etc.
Author: Hadi Ramdhani
"""

import re
import os
import json
import csv
from datetime import datetime
from urllib.parse import urlparse, urljoin
import requests
from bs4 import BeautifulSoup

def validate_url(url):
    """
    Validate if a string is a valid URL
    
    Args:
        url (str): URL to validate
        
    Returns:
        bool: True if valid URL, False otherwise
    """
    if not url or not isinstance(url, str):
        return False
        
    # Add protocol if missing
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
    
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

def sanitize_url(url):
    """
    Clean and normalize URL
    
    Args:
        url (str): URL to sanitize
        
    Returns:
        str: Sanitized URL
    """
    if not url:
        return ""
        
    # Remove whitespace
    url = url.strip()
    
    # Add protocol if missing
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
        
    # Remove trailing slash
    url = url.rstrip('/')
    
    return url

def extract_domain(url):
    """
    Extract domain from URL
    
    Args:
        url (str): URL to extract domain from
        
    Returns:
        str: Domain name
    """
    try:
        parsed = urlparse(url)
        return parsed.netloc
    except:
        return ""

def get_url_info(url):
    """
    Get basic information about a URL
    
    Args:
        url (str): URL to analyze
        
    Returns:
        dict: URL information
    """
    try:
        parsed = urlparse(url)
        return {
            'scheme': parsed.scheme,
            'domain': parsed.netloc,
            'path': parsed.path,
            'query': parsed.query,
            'fragment': parsed.fragment
        }
    except:
        return {}

def is_responsive(url, timeout=10):
    """
    Check if a URL is responsive
    
    Args:
        url (str): URL to check
        timeout (int): Timeout in seconds
        
    Returns:
        bool: True if responsive, False otherwise
    """
    try:
        response = requests.head(url, timeout=timeout)
        return response.status_code < 500
    except:
        return False

def get_page_title(url, timeout=10):
    """
    Get page title from URL
    
    Args:
        url (str): URL to get title from
        timeout (int): Timeout in seconds
        
    Returns:
        str: Page title or empty string
    """
    try:
        response = requests.get(url, timeout=timeout)
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.find('title')
        return title.text.strip() if title else ""
    except:
        return ""

def save_results_to_json(results, filename=None):
    """
    Save mirror results to JSON file
    
    Args:
        results (list): List of result dictionaries
        filename (str): Output filename (optional)
        
    Returns:
        str: Path to saved file
    """
    if not filename:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"mirror_results_{timestamp}.json"
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        return filename
    except Exception as e:
        raise Exception(f"Failed to save JSON: {str(e)}")

def save_results_to_csv(results, filename=None):
    """
    Save mirror results to CSV file
    
    Args:
        results (list): List of result dictionaries
        filename (str): Output filename (optional)
        
    Returns:
        str: Path to saved file
    """
    if not filename:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"mirror_results_{timestamp}.csv"
    
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

def load_urls_from_file(filepath):
    """
    Load URLs from text file
    
    Args:
        filepath (str): Path to file containing URLs
        
    Returns:
        list: List of URLs
    """
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

def save_urls_to_file(urls, filepath):
    """
    Save URLs to text file
    
    Args:
        urls (list): List of URLs
        filepath (str): Output file path
        
    Returns:
        str: Path to saved file
    """
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            for url in urls:
                f.write(f"{url}\n")
        return filepath
    except Exception as e:
        raise Exception(f"Failed to save URLs: {str(e)}")

def format_timestamp(timestamp=None):
    """
    Format timestamp for display
    
    Args:
        timestamp (datetime): Timestamp to format (optional)
        
    Returns:
        str: Formatted timestamp
    """
    if timestamp is None:
        timestamp = datetime.now()
    return timestamp.strftime('%Y-%m-%d %H:%M:%S')

def calculate_success_rate(results):
    """
    Calculate success rate from results
    
    Args:
        results (list): List of result dictionaries
        
    Returns:
        float: Success rate percentage
    """
    if not results:
        return 0.0
    
    successful = sum(1 for r in results if r.get('status') == 'Success')
    return (successful / len(results)) * 100

def get_file_size(filepath):
    """
    Get file size in human readable format
    
    Args:
        filepath (str): Path to file
        
    Returns:
        str: File size (e.g., "1.5 MB")
    """
    try:
        size = os.path.getsize(filepath)
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"
    except:
        return "Unknown"

def create_backup(filepath):
    """
    Create backup of a file
    
    Args:
        filepath (str): Path to file to backup
        
    Returns:
        str: Path to backup file
    """
    try:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_path = f"{filepath}.backup_{timestamp}"
        import shutil
        shutil.copy2(filepath, backup_path)
        return backup_path
    except Exception as e:
        raise Exception(f"Failed to create backup: {str(e)}")

def clean_old_backups(directory, days=7):
    """
    Clean old backup files
    
    Args:
        directory (str): Directory containing backups
        days (int): Age in days to keep
        
    Returns:
        int: Number of files deleted
    """
    import glob
    import time
    
    deleted_count = 0
    cutoff_time = time.time() - (days * 24 * 60 * 60)
    
    backup_pattern = os.path.join(directory, "*.backup_*")
    for backup_file in glob.glob(backup_pattern):
        try:
            if os.path.getmtime(backup_file) < cutoff_time:
                os.remove(backup_file)
                deleted_count += 1
        except:
            pass
    
    return deleted_count

def generate_report(results):
    """
    Generate summary report from results
    
    Args:
        results (list): List of result dictionaries
        
    Returns:
        dict: Summary report
    """
    if not results:
        return {
            'total': 0,
            'successful': 0,
            'failed': 0,
            'success_rate': 0.0,
            'start_time': None,
            'end_time': None,
            'duration': None
        }
    
    successful = sum(1 for r in results if r.get('status') == 'Success')
    failed = len(results) - successful
    success_rate = calculate_success_rate(results)
    
    # Get time range
    timestamps = [r.get('timestamp') for r in results if r.get('timestamp')]
    start_time = min(timestamps) if timestamps else None
    end_time = max(timestamps) if timestamps else None
    
    return {
        'total': len(results),
        'successful': successful,
        'failed': failed,
        'success_rate': success_rate,
        'start_time': start_time,
        'end_time': end_time,
        'duration': None  # Could be calculated if needed
    }

# Export functions
__all__ = [
    'validate_url', 'sanitize_url', 'extract_domain', 'get_url_info',
    'is_responsive', 'get_page_title', 'save_results_to_json', 'save_results_to_csv',
    'load_urls_from_file', 'save_urls_to_file', 'format_timestamp',
    'calculate_success_rate', 'get_file_size', 'create_backup', 'clean_old_backups',
    'generate_report'
]