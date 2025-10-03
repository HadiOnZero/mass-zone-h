#!/usr/bin/env python3
"""
Configuration file for Zone-H Mass Mirror Tool
Contains default settings and configurations
"""

import os

# Application Settings
APP_NAME = "Zone-H Mass Mirror Tool"
APP_VERSION = "1.0.0"
APP_AUTHOR = "Hadi Ramdhani"

# Default Settings
DEFAULT_SETTINGS = {
    'delay': 1,                    # Delay between requests (seconds)
    'timeout': 10,                 # Request timeout (seconds)
    'max_threads': 5,              # Maximum concurrent threads
    'retry_attempts': 3,           # Number of retry attempts for failed requests
    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    
    # UI Settings
    'window_width': 1200,
    'window_height': 800,
    'window_title': f'{APP_NAME} v{APP_VERSION}',
    
    # Colors (Hacker Theme)
    'colors': {
        'background': '#000000',
        'text': '#00ff00',
        'accent': '#00ff00',
        'success': '#00ff00',
        'error': '#ff0000',
        'warning': '#ffff00',
        'info': '#0080ff',
        'border': '#00ff00',
        'highlight': '#003300',
        'dark_highlight': '#001100'
    },
    
    # Network Settings
    'network': {
        'verify_ssl': True,
        'allow_redirects': True,
        'max_redirects': 5,
        'keep_alive': True,
        'compression': True
    }
}

# User Agents List
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Mozilla/5.0 (X11; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.59',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.59'
]

# Common HTTP Headers
DEFAULT_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
}

# File Extensions for filtering
VALID_EXTENSIONS = [
    '.html', '.htm', '.php', '.asp', '.aspx', '.jsp', '.js', '.css',
    '.xml', '.json', '.txt', '.md', '.py', '.pl', '.rb', '.sh'
]

# Error Messages
ERROR_MESSAGES = {
    'INVALID_URL': 'Invalid URL format',
    'CONNECTION_ERROR': 'Connection failed',
    'TIMEOUT_ERROR': 'Request timeout',
    'HTTP_ERROR': 'HTTP error occurred',
    'SSL_ERROR': 'SSL certificate error',
    'UNKNOWN_ERROR': 'Unknown error occurred'
}

# Success Messages
SUCCESS_MESSAGES = {
    'MIRROR_STARTED': 'Mass mirror process started',
    'MIRROR_COMPLETED': 'Mass mirror process completed successfully',
    'URL_ADDED': 'URL added to queue',
    'SETTINGS_SAVED': 'Settings saved successfully'
}

# Warning Messages
WARNING_MESSAGES = {
    'NO_URLS': 'Please enter at least one URL',
    'INVALID_URLS': 'Please enter valid URLs',
    'PROCESS_RUNNING': 'Mirror process is already running',
    'EMPTY_RESULTS': 'No results to export'
}

def get_config_path():
    """Get configuration file path"""
    if os.name == 'nt':  # Windows
        return os.path.join(os.environ['APPDATA'], 'ZoneHMirror')
    else:  # Linux/Mac
        return os.path.join(os.path.expanduser('~'), '.config', 'ZoneHMirror')

def ensure_config_dir():
    """Ensure configuration directory exists"""
    config_path = get_config_path()
    if not os.path.exists(config_path):
        os.makedirs(config_path)
    return config_path

# Export settings
__all__ = [
    'APP_NAME', 'APP_VERSION', 'APP_AUTHOR',
    'DEFAULT_SETTINGS', 'USER_AGENTS', 'DEFAULT_HEADERS',
    'VALID_EXTENSIONS', 'ERROR_MESSAGES', 'SUCCESS_MESSAGES', 'WARNING_MESSAGES',
    'get_config_path', 'ensure_config_dir'
]