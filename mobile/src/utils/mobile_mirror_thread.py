#!/usr/bin/env python3
"""
ZoneH Mobile Mirror Thread Module
Thread untuk proses mass mirror dengan Kivy
Author: Hadi Ramdhani
"""

import requests
import time
import threading
from datetime import datetime
from kivy.clock import Clock
from bs4 import BeautifulSoup


class ZoneHMobileMirror(threading.Thread):
    """Thread untuk proses mass mirror di mobile"""
    
    def __init__(self, urls, delay=2, callback=None):
        super().__init__()
        self.urls = urls
        self.delay = delay
        self.callback = callback
        self.is_running = True
        self.results = []
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; Mobile) AppleWebKit/537.36'
        })
        
    def run(self):
        """Eksekusi mass mirror untuk mobile"""
        total_urls = len(self.urls)
        successful = 0
        failed = 0
        
        for i, url in enumerate(self.urls):
            if not self.is_running:
                break
                
            try:
                # Emit log message via callback
                if self.callback:
                    Clock.schedule_once(lambda dt: self.callback(
                        'log', f"[{datetime.now().strftime('%H:%M:%S')}] Processing: {url}"
                    ), 0)
                
                # Validasi URL
                if not url.startswith(('http://', 'https://')):
                    url = 'http://' + url
                    
                # Request ke URL dengan timeout lebih lama untuk mobile
                response = self.session.get(url, timeout=15)
                
                if response.status_code == 200:
                    successful += 1
                    
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
                    
                    if self.callback:
                        Clock.schedule_once(lambda dt: self.callback(
                            'log', f"[{datetime.now().strftime('%H:%M:%S')}] ✓ Success: {url}"
                        ), 0)
                    
                else:
                    failed += 1
                    
                    if self.callback:
                        Clock.schedule_once(lambda dt: self.callback(
                            'log', f"[{datetime.now().strftime('%H:%M:%S')}] ✗ Failed: {url} (Status: {response.status_code})"
                        ), 0)
                    
                    result = {
                        'url': url,
                        'status': 'Failed',
                        'status_code': response.status_code,
                        'title': 'N/A',
                        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
                
                self.results.append(result)
                
                # Emit result via callback
                if self.callback:
                    Clock.schedule_once(lambda dt, res=result: self.callback('result', res), 0)
                
            except requests.exceptions.Timeout:
                failed += 1
                error_msg = f"[{datetime.now().strftime('%H:%M:%S')}] ✗ Timeout: {url}"
                
                if self.callback:
                    Clock.schedule_once(lambda dt: self.callback('log', error_msg), 0)
                
                result = {
                    'url': url,
                    'status': 'Timeout',
                    'status_code': 'N/A',
                    'title': 'Request timeout',
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                self.results.append(result)
                
            except requests.exceptions.ConnectionError:
                failed += 1
                error_msg = f"[{datetime.now().strftime('%H:%M:%S')}] ✗ Connection error: {url}"
                
                if self.callback:
                    Clock.schedule_once(lambda dt: self.callback('log', error_msg), 0)
                
                result = {
                    'url': url,
                    'status': 'Connection Error',
                    'status_code': 'N/A',
                    'title': 'Connection failed',
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                self.results.append(result)
                
            except requests.exceptions.RequestException as e:
                failed += 1
                error_msg = f"[{datetime.now().strftime('%H:%M:%S')}] ✗ Error: {url} ({str(e)})"
                
                if self.callback:
                    Clock.schedule_once(lambda dt: self.callback('log', error_msg), 0)
                
                result = {
                    'url': url,
                    'status': 'Error',
                    'status_code': 'N/A',
                    'title': str(e),
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                self.results.append(result)
                
            except Exception as e:
                failed += 1
                error_msg = f"[{datetime.now().strftime('%H:%M:%S')}] ✗ Unexpected error: {url} ({str(e)})"
                
                if self.callback:
                    Clock.schedule_once(lambda dt: self.callback('log', error_msg), 0)
                
                result = {
                    'url': url,
                    'status': 'Error',
                    'status_code': 'N/A',
                    'title': str(e),
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                self.results.append(result)
            
            # Update progress
            progress = int((i + 1) / total_urls * 100)
            if self.callback:
                Clock.schedule_once(lambda dt, p=progress: self.callback('progress', p), 0)
            
            # Delay antar request - optimized for mobile
            if i < total_urls - 1 and self.is_running:
                time.sleep(self.delay)
        
        # Summary
        summary_msg = f"""
📱 MOBILE MIRROR COMPLETED
═══════════════════════════════════════
Total URLs: {total_urls}
Successful: {successful}
Failed: {failed}
Success Rate: {(successful/total_urls*100):.1f}%
"""
        
        if self.callback:
            Clock.schedule_once(lambda dt: self.callback('log', summary_msg), 0)
            Clock.schedule_once(lambda dt: self.callback('completed', self.results), 0)
        
    def stop(self):
        """Hentikan proses mirror"""
        self.is_running = False
        
    def get_results(self):
        """Dapatkan hasil mirror"""
        return self.results