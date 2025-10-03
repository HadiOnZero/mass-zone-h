#!/usr/bin/env python3
"""
ZoneH Mirror Thread Module
Thread untuk proses mass mirror dengan PyQt5
Author: Hadi Ramdhani
"""

import requests
import time
from datetime import datetime
from PyQt5.QtCore import QThread, pyqtSignal
from bs4 import BeautifulSoup


class ZoneHMirror(QThread):
    """Thread untuk proses mass mirror"""
    progress_updated = pyqtSignal(int)
    log_updated = pyqtSignal(str)
    mirror_completed = pyqtSignal(dict)
    
    def __init__(self, urls, delay=1):
        super().__init__()
        self.urls = urls
        self.delay = delay
        self.is_running = True
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
    def run(self):
        """Eksekusi mass mirror"""
        total_urls = len(self.urls)
        successful = 0
        failed = 0
        
        for i, url in enumerate(self.urls):
            if not self.is_running:
                break
                
            try:
                self.log_updated.emit(f"[{datetime.now().strftime('%H:%M:%S')}] Processing: {url}")
                
                # Validasi URL
                if not url.startswith(('http://', 'https://')):
                    url = 'http://' + url
                    
                # Request ke URL
                response = self.session.get(url, timeout=10)
                
                if response.status_code == 200:
                    successful += 1
                    self.log_updated.emit(f"[{datetime.now().strftime('%H:%M:%S')}] ✓ Success: {url}")
                    
                    # Parse konten untuk informasi tambahan
                    soup = BeautifulSoup(response.content, 'html.parser')
                    title = soup.find('title')
                    title_text = title.text.strip() if title else 'No Title'
                    
                    result = {
                        'url': url,
                        'status': 'Success',
                        'status_code': response.status_code,
                        'title': title_text,
                        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
                    
                else:
                    failed += 1
                    self.log_updated.emit(f"[{datetime.now().strftime('%H:%M:%S')}] ✗ Failed: {url} (Status: {response.status_code})")
                    
                    result = {
                        'url': url,
                        'status': 'Failed',
                        'status_code': response.status_code,
                        'title': 'N/A',
                        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
                
                self.mirror_completed.emit(result)
                
            except requests.exceptions.RequestException as e:
                failed += 1
                self.log_updated.emit(f"[{datetime.now().strftime('%H:%M:%S')}] ✗ Error: {url} ({str(e)})")
                
                result = {
                    'url': url,
                    'status': 'Error',
                    'status_code': 'N/A',
                    'title': str(e),
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                self.mirror_completed.emit(result)
                
            except Exception as e:
                failed += 1
                self.log_updated.emit(f"[{datetime.now().strftime('%H:%M:%S')}] ✗ Unexpected error: {url} ({str(e)})")
                
                result = {
                    'url': url,
                    'status': 'Error',
                    'status_code': 'N/A',
                    'title': str(e),
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                self.mirror_completed.emit(result)
            
            # Update progress
            progress = int((i + 1) / total_urls * 100)
            self.progress_updated.emit(progress)
            
            # Delay antar request
            if i < total_urls - 1:
                time.sleep(self.delay)
        
        # Summary
        self.log_updated.emit(f"\n[{datetime.now().strftime('%H:%M:%S')}] === MIRROR COMPLETED ===")
        self.log_updated.emit(f"Total URLs: {total_urls}")
        self.log_updated.emit(f"Successful: {successful}")
        self.log_updated.emit(f"Failed: {failed}")
        self.log_updated.emit(f"Success Rate: {(successful/total_urls*100):.1f}%")
        
    def stop(self):
        """Hentikan proses mirror"""
        self.is_running = False