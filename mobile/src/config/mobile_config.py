#!/usr/bin/env python3
"""
Configuration file for Zone-H Mobile Mirror Tool
Contains default settings and configurations for mobile version
"""

import os

# Application Settings
APP_NAME = "Zone-H Mobile Mirror"
APP_VERSION = "1.0.0"
APP_AUTHOR = "Hadi Ramdhani"

# Mobile Default Settings
MOBILE_DEFAULT_SETTINGS = {
    'delay': 2,                    # Delay between requests (seconds) - optimized for mobile
    'timeout': 15,                 # Request timeout (seconds) - longer for mobile networks
    'max_threads': 3,              # Maximum concurrent threads - reduced for mobile
    'retry_attempts': 2,           # Number of retry attempts for failed requests
    'user_agent': 'Mozilla/5.0 (Linux; Android 10; Mobile) AppleWebKit/537.36',
    
    # Mobile UI Settings
    'mobile_ui': {
        'primary_color': '#00ff00',      # Hacker green
        'accent_color': '#ffffff',       # White accent
        'background_color': '#000000',   # Black background
        'text_color': '#ffffff',         # White text
        'error_color': '#ff0000',        # Red for errors
        'success_color': '#00ff00',      # Green for success
        'card_radius': 15,               # Card corner radius
        'button_radius': 25,             # Button corner radius
        'font_size_small': 12,           # Small font size
        'font_size_medium': 14,          # Medium font size
        'font_size_large': 18,           # Large font size
        'font_size_title': 24,           # Title font size
    },
    
    # Mobile Network Settings
    'mobile_network': {
        'verify_ssl': True,
        'allow_redirects': True,
        'max_redirects': 3,              # Reduced for mobile
        'keep_alive': True,
        'compression': True,
        'mobile_optimized': True,        # Enable mobile optimizations
    }
}

# Mobile User Agents List
MOBILE_USER_AGENTS = [
    'Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (Linux; Android 9; Mi 9) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36',
    'Mozilla/5.0 (iPad; CPU OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
]

# Mobile HTTP Headers
MOBILE_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Cache-Control': 'max-age=0',
}

# Mobile App Configuration
MOBILE_APP_CONFIG = {
    'min_android_version': '5.0',      # Minimum Android version
    'min_ios_version': '11.0',         # Minimum iOS version
    'orientation': 'portrait',         # Preferred orientation
    'fullscreen': False,               # Fullscreen mode
    'keep_screen_on': True,            # Keep screen on during mirror
    'vibrate_on_completion': True,     # Vibrate when mirror completes
    'show_notifications': True,        # Show completion notifications
}

# Error Messages for Mobile
MOBILE_ERROR_MESSAGES = {
    'INVALID_URL': 'Invalid URL format',
    'CONNECTION_ERROR': 'Connection failed - Check your internet',
    'TIMEOUT_ERROR': 'Request timeout - Try again later',
    'HTTP_ERROR': 'HTTP error occurred',
    'SSL_ERROR': 'SSL certificate error',
    'UNKNOWN_ERROR': 'Unknown error occurred',
    'MOBILE_NETWORK_ERROR': 'Mobile network error',
    'NO_INTERNET': 'No internet connection available',
}

# Success Messages for Mobile
MOBILE_SUCCESS_MESSAGES = {
    'MIRROR_STARTED': 'Mass mirror process started',
    'MIRROR_COMPLETED': 'Mirror completed successfully!',
    'URL_ADDED': 'URL added to queue',
    'SETTINGS_SAVED': 'Settings saved',
    'APP_READY': 'Zone-H Mobile Mirror ready',
}

# Warning Messages for Mobile
MOBILE_WARNING_MESSAGES = {
    'NO_URLS': 'Please enter at least one URL',
    'INVALID_URLS': 'Please enter valid URLs',
    'PROCESS_RUNNING': 'Mirror already running',
    'EMPTY_RESULTS': 'No results to export',
    'BATTERY_LOW': 'Low battery - Consider charging',
    'MOBILE_DATA': 'Using mobile data - Watch your usage',
}

def get_mobile_config_path():
    """Get mobile configuration file path"""
    if os.name == 'nt':  # Windows
        return os.path.join(os.environ['APPDATA'], 'ZoneHMobile')
    else:  # Linux/Mac/Android/iOS
        return os.path.join(os.path.expanduser('~'), '.config', 'ZoneHMobile')

def ensure_mobile_config_dir():
    """Ensure mobile configuration directory exists"""
    config_path = get_mobile_config_path()
    if not os.path.exists(config_path):
        os.makedirs(config_path)
    return config_path

# Export settings
__all__ = [
    'APP_NAME', 'APP_VERSION', 'APP_AUTHOR',
    'MOBILE_DEFAULT_SETTINGS', 'MOBILE_USER_AGENTS', 'MOBILE_HEADERS',
    'MOBILE_APP_CONFIG', 'MOBILE_ERROR_MESSAGES', 'MOBILE_SUCCESS_MESSAGES', 
    'MOBILE_WARNING_MESSAGES', 'get_mobile_config_path', 'ensure_mobile_config_dir'
]