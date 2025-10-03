#!/usr/bin/env python3
"""
Zone-H Mass Mirror Application
A desktop application for mass mirroring Zone-H notifications
Author: Hadi Ramdhani
"""

import sys
import os
import math
import requests
import threading
import time
from datetime import datetime
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup

from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QTextEdit, QLineEdit,
                             QLabel, QProgressBar, QTableWidget, QTableWidgetItem,
                             QHeaderView, QMessageBox, QSplitter, QGroupBox,
                             QCheckBox, QSpinBox, QComboBox, QFileDialog, QDialog,
                             QDialogButtonBox, QTextBrowser)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt5.QtGui import QFont, QPalette, QColor, QIcon, QPixmap

# Import local modules
from config import DEFAULT_SETTINGS, USER_AGENTS, ERROR_MESSAGES, SUCCESS_MESSAGES, WARNING_MESSAGES
from utils import (validate_url, sanitize_url, extract_domain, get_url_info,
                  save_results_to_json, save_results_to_csv, load_urls_from_file,
                  calculate_success_rate, generate_report)

class AboutDialog(QDialog):
    """About Dialog untuk Zone-H Mass Mirror Tool"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("About Zone-H Mass Mirror Tool")
        self.setFixedSize(500, 600)
        self.setModal(True)
        self.init_ui()
        self.apply_hacker_theme()
        
    def init_ui(self):
        """Inisialisasi UI about dialog"""
        layout = QVBoxLayout()
        
        # Header dengan logo/teks
        header_label = QLabel("ZONE-H MASS MIRROR")
        header_label.setAlignment(Qt.AlignCenter)
        header_label.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: #00ff00;
                padding: 20px;
                margin: 10px;
                border: 2px solid rgba(0, 255, 0, 0.6);
                border-radius: 15px;
                background-color: rgba(0, 255, 0, 0.1);
                text-shadow: 0 0 10px rgba(0, 255, 0, 0.8);
                letter-spacing: 3px;
            }
        """)
        layout.addWidget(header_label)
        
        # Informasi aplikasi
        info_text = f"""
        <div style='color: #00ff00; font-family: "Courier New", monospace;'>
        <h3 style='color: #00ff00; text-align: center;'>🛡️ Zone-H Mass Mirror Tool 🛡️</h3>
        
        <p><strong>Version:</strong> 1.0.0</p>
        <p><strong>Author:</strong> Hadi Ramdhani</p>
        <p><strong>License:</strong> MIT License</p>
        
        <h4 style='color: #00ff00;'>📋 Description:</h4>
        <p>Aplikasi desktop elegan untuk melakukan mass mirror terhadap notifikasi Zone-H
        dengan desain hacker ala-ala (hitam & hijau).</p>
        
        <h4 style='color: #00ff00;'>✨ Features:</h4>
        <ul>
            <li>🎯 Mass Mirror multiple URLs secara bersamaan</li>
            <li>🎨 Desain Hacker dengan tema hitam dan hijau neon</li>
            <li>📊 Real-time Progress monitoring</li>
            <li>📈 Statistik hasil mirror yang detail</li>
            <li>⚙️ Customizable Settings (delay, timeout, user agent)</li>
            <li>🛡️ Robust Error Handling</li>
            <li>📝 Console log untuk debugging</li>
            <li>🔄 Thread-safe operation</li>
        </ul>
        
        <h4 style='color: #00ff00;'>🔧 Technical Details:</h4>
        <ul>
            <li>Built with Python 3.6+</li>
            <li>GUI Framework: PyQt5</li>
            <li>HTTP Library: requests</li>
            <li>HTML Parser: BeautifulSoup4</li>
            <li>Multi-threading support</li>
        </ul>
        
        <h4 style='color: #00ff00;'>⚠️ Disclaimer:</h4>
        <p><em>Aplikasi ini dibuat untuk keperluan edukasi dan testing keamanan.
        Pengguna bertanggung jawab atas penggunaannya sesuai dengan hukum yang berlaku.</em></p>
        
        <p style='text-align: center; margin-top: 20px;'>
        <strong>© 2024 Hadi Ramdhani - Elite Hacker Tools</strong>
        </p>
        </div>
        """
        
        # Text browser untuk konten
        text_browser = QTextBrowser()
        text_browser.setHtml(info_text)
        text_browser.setStyleSheet("""
            QTextBrowser {
                background-color: rgba(0, 0, 0, 0.8);
                color: #00ff00;
                border: 1px solid rgba(0, 255, 0, 0.4);
                border-radius: 10px;
                padding: 15px;
                font-family: 'Courier New', monospace;
                font-size: 12px;
                line-height: 1.5;
            }
        """)
        layout.addWidget(text_browser)
        
        # Additional buttons
        button_layout = QHBoxLayout()
        
        # GitHub button
        github_button = QPushButton("🐙 GitHub")
        github_button.clicked.connect(self.open_github)
        github_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(102, 0, 255, 0.2);
                color: #bb88ff;
                font-weight: bold;
                padding: 8px 15px;
                border: 1px solid rgba(102, 0, 255, 0.5);
                border-radius: 15px;
                text-shadow: 0 0 5px rgba(187, 136, 255, 0.8);
                margin: 2px;
            }
            QPushButton:hover {
                background-color: rgba(102, 0, 255, 0.3);
                border: 1px solid rgba(102, 0, 255, 0.8);
            }
            QPushButton:pressed {
                background-color: rgba(102, 0, 255, 0.1);
            }
        """)
        button_layout.addWidget(github_button)
        
        # Documentation button
        docs_button = QPushButton("📚 Documentation")
        docs_button.clicked.connect(self.open_documentation)
        docs_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 102, 204, 0.2);
                color: #44aaff;
                font-weight: bold;
                padding: 8px 15px;
                border: 1px solid rgba(0, 102, 204, 0.5);
                border-radius: 15px;
                text-shadow: 0 0 5px rgba(68, 170, 255, 0.8);
                margin: 2px;
            }
            QPushButton:hover {
                background-color: rgba(0, 102, 204, 0.3);
                border: 1px solid rgba(0, 102, 204, 0.8);
            }
            QPushButton:pressed {
                background-color: rgba(0, 102, 204, 0.1);
            }
        """)
        button_layout.addWidget(docs_button)
        
        # Contact button
        contact_button = QPushButton("📧 Contact")
        contact_button.clicked.connect(self.open_contact)
        contact_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 102, 0, 0.2);
                color: #ff8844;
                font-weight: bold;
                padding: 8px 15px;
                border: 1px solid rgba(255, 102, 0, 0.5);
                border-radius: 15px;
                text-shadow: 0 0 5px rgba(255, 136, 68, 0.8);
                margin: 2px;
            }
            QPushButton:hover {
                background-color: rgba(255, 102, 0, 0.3);
                border: 1px solid rgba(255, 102, 0, 0.8);
            }
            QPushButton:pressed {
                background-color: rgba(255, 102, 0, 0.1);
            }
        """)
        button_layout.addWidget(contact_button)
        
        button_layout.addStretch()
        
        # Close button
        close_button = QPushButton("✖ Close")
        close_button.clicked.connect(self.accept)
        close_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 0, 0, 0.2);
                color: #ff4444;
                font-weight: bold;
                padding: 8px 20px;
                border: 1px solid rgba(255, 0, 0, 0.5);
                border-radius: 15px;
                text-shadow: 0 0 5px rgba(255, 68, 68, 0.8);
                margin: 2px;
            }
            QPushButton:hover {
                background-color: rgba(255, 0, 0, 0.3);
                border: 1px solid rgba(255, 0, 0, 0.8);
            }
            QPushButton:pressed {
                background-color: rgba(255, 0, 0, 0.1);
            }
        """)
        button_layout.addWidget(close_button)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
        
    def open_github(self):
        """Buka halaman GitHub"""
        QMessageBox.information(self, "GitHub", "Coming soon! Repository GitHub akan segera tersedia.")
        
    def open_documentation(self):
        """Buka dokumentasi"""
        documentation_text = """
🛡️ ZONE-H MASS MIRROR TOOL - DOCUMENTATION

📋 PENDAHULUAN
Aplikasi ini dirancang untuk melakukan mass mirror terhadap notifikasi Zone-H
dengan antarmuka yang elegan dan fitur yang lengkap.

🔧 CARA PENGGUNAAN:
1. Masukkan URLs target di area input (satu per baris)
2. Atur pengaturan (delay, timeout, user agent)
3. Klik START MIRROR untuk memulai
4. Monitor progress di progress bar
5. Lihat hasil di tabel kanan

⚙️ PENGATURAN:
• Delay: Waktu tunggu antar request (1-10 detik)
• Timeout: Batas waktu request (5-60 detik)
• User Agent: Pilih user agent yang digunakan

📊 FITUR:
• Mass mirror multiple URLs
• Real-time progress monitoring
• Export hasil ke JSON/CSV
• Error handling yang robust
• Thread-safe operation

⚠️ DISCLAIMER:
Aplikasi ini untuk keperluan edukasi dan testing keamanan.
Gunakan dengan bijak dan sesuai hukum yang berlaku.
        """
        QMessageBox.information(self, "Documentation", documentation_text)
        
    def open_contact(self):
        """Buka informasi kontak"""
        contact_text = """
📧 CONTACT INFORMATION

👨‍💻 Author: Hadi Ramdhani
🏢 Organization: Elite Hacker Tools
📅 Version: 1.0.0
📄 License: MIT License

💬 Untuk pertanyaan, saran, atau laporan bug:
• Email: hadiramdhani@example.com
• GitHub: Coming soon!
• Forum: Coming soon!

🌟 Jika Anda merasa aplikasi ini bermanfaat:
• Berikan bintang di GitHub
• Share ke teman-teman
• Donasi untuk support pengembangan

⚠️ IMPORTANT:
Aplikasi ini dibuat untuk keperluan edukasi.
Pengguna bertanggung jawab atas penggunaannya.
        """
        QMessageBox.information(self, "Contact", contact_text)
        
    def apply_hacker_theme(self):
        """Terapkan tema hacker untuk about dialog"""
        self.setStyleSheet("""
            QDialog {
                background-color: #000000;
                color: #00ff00;
                border: 2px solid rgba(0, 255, 0, 0.6);
                border-radius: 20px;
            }
        """)

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

class ZoneHApp(QMainWindow):
    """Aplikasi utama Zone-H Mass Mirror"""
    
    def __init__(self):
        super().__init__()
        self.mirror_thread = None
        self.results = []
        self.glow_timer = QTimer()
        self.glow_phase = 0
        self.init_ui()
        self.apply_hacker_theme()
        self.start_glow_animation()
        
    def init_ui(self):
        """Inisialisasi antarmuka pengguna"""
        self.setWindowTitle('Zone-H Mass Mirror - Elite Mirror Tool')
        self.setGeometry(100, 100, 1200, 800)
        
        # Widget utama
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        # Layout utama
        main_layout = QHBoxLayout(main_widget)
        
        # Splitter untuk membagi area
        splitter = QSplitter(Qt.Horizontal)
        
        # Panel kiri - Input dan kontrol
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        
        # Header
        header_label = QLabel('ZONE-H MASS MIRROR')
        header_label.setAlignment(Qt.AlignCenter)
        header_label.setStyleSheet("""
            QLabel {
                font-size: 28px;
                font-weight: bold;
                color: #00ff00;
                padding: 15px;
                border: 1px solid rgba(0, 255, 0, 0.4);
                border-radius: 20px;
                background-color: rgba(0, 255, 0, 0.08);
                backdrop-filter: blur(10px);
                box-shadow:
                    0 0 30px rgba(0, 255, 0, 0.3),
                    inset 0 0 20px rgba(0, 255, 0, 0.1);
                text-shadow: 0 0 15px rgba(0, 255, 0, 0.8);
                letter-spacing: 2px;
            }
        """)
        left_layout.addWidget(header_label)
        
        # Input URLs
        input_group = QGroupBox("Target URLs")
        input_layout = QVBoxLayout()
        
        self.url_input = QTextEdit()
        self.url_input.setPlaceholderText("Masukkan URLs target (satu per baris)\nContoh:\nhttp://site1.com\nhttp://site2.com\nhttps://site3.com")
        self.url_input.setMaximumHeight(200)
        input_layout.addWidget(self.url_input)
        
        input_group.setLayout(input_layout)
        left_layout.addWidget(input_group)
        
        # Settings
        settings_group = QGroupBox("Settings")
        settings_layout = QVBoxLayout()
        
        # Delay setting
        delay_layout = QHBoxLayout()
        delay_layout.addWidget(QLabel("Delay (detik):"))
        self.delay_spinbox = QSpinBox()
        self.delay_spinbox.setRange(1, 10)
        self.delay_spinbox.setValue(1)
        delay_layout.addWidget(self.delay_spinbox)
        delay_layout.addStretch()
        settings_layout.addLayout(delay_layout)
        
        # Timeout setting
        timeout_layout = QHBoxLayout()
        timeout_layout.addWidget(QLabel("Timeout (detik):"))
        self.timeout_spinbox = QSpinBox()
        self.timeout_spinbox.setRange(5, 60)
        self.timeout_spinbox.setValue(10)
        timeout_layout.addWidget(self.timeout_spinbox)
        timeout_layout.addStretch()
        settings_layout.addLayout(timeout_layout)
        
        # User Agent
        ua_layout = QHBoxLayout()
        ua_layout.addWidget(QLabel("User Agent:"))
        self.ua_combo = QComboBox()
        self.ua_combo.addItems([
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        ])
        ua_layout.addWidget(self.ua_combo)
        ua_layout.addStretch()
        settings_layout.addLayout(ua_layout)
        
        settings_group.setLayout(settings_layout)
        left_layout.addWidget(settings_group)
        
        # File operations
        file_group = QGroupBox("File Operations")
        file_layout = QHBoxLayout()
        
        self.load_button = QPushButton("LOAD URLs")
        self.load_button.clicked.connect(self.load_urls_from_file)
        self.load_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 102, 0, 0.15);
                color: #ff8844;
                font-weight: bold;
                font-size: 11px;
                padding: 10px 15px;
                border: 1px solid rgba(255, 102, 0, 0.3);
                border-radius: 25px;
                backdrop-filter: blur(10px);
                box-shadow:
                    0 0 15px rgba(255, 102, 0, 0.3),
                    inset 0 0 15px rgba(255, 102, 0, 0.1),
                    0 3px 10px rgba(0, 0, 0, 0.3);
                transition: all 0.3s ease;
                text-shadow: 0 0 8px rgba(255, 136, 68, 0.8);
            }
            QPushButton:hover {
                background-color: rgba(255, 102, 0, 0.25);
                border: 1px solid rgba(255, 102, 0, 0.6);
                box-shadow:
                    0 0 25px rgba(255, 102, 0, 0.5),
                    inset 0 0 25px rgba(255, 102, 0, 0.2),
                    0 5px 15px rgba(0, 0, 0, 0.4);
                transform: translateY(-1px);
            }
            QPushButton:pressed {
                background-color: rgba(255, 102, 0, 0.1);
                box-shadow:
                    0 0 8px rgba(255, 102, 0, 0.4),
                    inset 0 0 12px rgba(255, 102, 0, 0.3),
                    0 2px 6px rgba(0, 0, 0, 0.5);
                transform: translateY(1px);
            }
        """)
        file_layout.addWidget(self.load_button)
        
        self.export_json_button = QPushButton("EXPORT JSON")
        self.export_json_button.clicked.connect(self.export_results_json)
        self.export_json_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(102, 0, 255, 0.15);
                color: #8844ff;
                font-weight: bold;
                font-size: 11px;
                padding: 10px 15px;
                border: 1px solid rgba(102, 0, 255, 0.3);
                border-radius: 25px;
                backdrop-filter: blur(10px);
                box-shadow:
                    0 0 15px rgba(102, 0, 255, 0.3),
                    inset 0 0 15px rgba(102, 0, 255, 0.1),
                    0 3px 10px rgba(0, 0, 0, 0.3);
                transition: all 0.3s ease;
                text-shadow: 0 0 8px rgba(136, 68, 255, 0.8);
            }
            QPushButton:hover {
                background-color: rgba(102, 0, 255, 0.25);
                border: 1px solid rgba(102, 0, 255, 0.6);
                box-shadow:
                    0 0 25px rgba(102, 0, 255, 0.5),
                    inset 0 0 25px rgba(102, 0, 255, 0.2),
                    0 5px 15px rgba(0, 0, 0, 0.4);
                transform: translateY(-1px);
            }
            QPushButton:pressed {
                background-color: rgba(102, 0, 255, 0.1);
                box-shadow:
                    0 0 8px rgba(102, 0, 255, 0.4),
                    inset 0 0 12px rgba(102, 0, 255, 0.3),
                    0 2px 6px rgba(0, 0, 0, 0.5);
                transform: translateY(1px);
            }
        """)
        file_layout.addWidget(self.export_json_button)
        
        self.export_csv_button = QPushButton("EXPORT CSV")
        self.export_csv_button.clicked.connect(self.export_results_csv)
        self.export_csv_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 0, 255, 0.15);
                color: #ff44ff;
                font-weight: bold;
                font-size: 11px;
                padding: 10px 15px;
                border: 1px solid rgba(255, 0, 255, 0.3);
                border-radius: 25px;
                backdrop-filter: blur(10px);
                box-shadow:
                    0 0 15px rgba(255, 0, 255, 0.3),
                    inset 0 0 15px rgba(255, 0, 255, 0.1),
                    0 3px 10px rgba(0, 0, 0, 0.3);
                transition: all 0.3s ease;
                text-shadow: 0 0 8px rgba(255, 68, 255, 0.8);
            }
            QPushButton:hover {
                background-color: rgba(255, 0, 255, 0.25);
                border: 1px solid rgba(255, 0, 255, 0.6);
                box-shadow:
                    0 0 25px rgba(255, 0, 255, 0.5),
                    inset 0 0 25px rgba(255, 0, 255, 0.2),
                    0 5px 15px rgba(0, 0, 0, 0.4);
                transform: translateY(-1px);
            }
            QPushButton:pressed {
                background-color: rgba(255, 0, 255, 0.1);
                box-shadow:
                    0 0 8px rgba(255, 0, 255, 0.4),
                    inset 0 0 12px rgba(255, 0, 255, 0.3),
                    0 2px 6px rgba(0, 0, 0, 0.5);
                transform: translateY(1px);
            }
        """)
        file_layout.addWidget(self.export_csv_button)
        
        file_group.setLayout(file_layout)
        left_layout.addWidget(file_group)
        
        # Control buttons
        button_layout = QHBoxLayout()
        
        self.start_button = QPushButton("START MIRROR")
        self.start_button.clicked.connect(self.start_mirror)
        self.start_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 255, 0, 0.15);
                color: #00ff00;
                font-weight: bold;
                font-size: 12px;
                padding: 12px 20px;
                border: 1px solid rgba(0, 255, 0, 0.3);
                border-radius: 30px;
                backdrop-filter: blur(10px);
                box-shadow:
                    0 0 20px rgba(0, 255, 0, 0.3),
                    inset 0 0 20px rgba(0, 255, 0, 0.1),
                    0 4px 15px rgba(0, 0, 0, 0.3);
                transition: all 0.3s ease;
                text-shadow: 0 0 10px rgba(0, 255, 0, 0.8);
            }
            QPushButton:hover {
                background-color: rgba(0, 255, 0, 0.25);
                border: 1px solid rgba(0, 255, 0, 0.6);
                box-shadow:
                    0 0 30px rgba(0, 255, 0, 0.6),
                    inset 0 0 30px rgba(0, 255, 0, 0.2),
                    0 6px 20px rgba(0, 0, 0, 0.4);
                transform: translateY(-2px);
            }
            QPushButton:pressed {
                background-color: rgba(0, 255, 0, 0.1);
                box-shadow:
                    0 0 10px rgba(0, 255, 0, 0.4),
                    inset 0 0 15px rgba(0, 255, 0, 0.3),
                    0 2px 8px rgba(0, 0, 0, 0.5);
                transform: translateY(1px);
            }
            QPushButton:disabled {
                background-color: rgba(100, 100, 100, 0.15);
                color: #666666;
                border: 1px solid rgba(100, 100, 100, 0.3);
                box-shadow: none;
                text-shadow: none;
            }
        """)
        button_layout.addWidget(self.start_button)
        
        self.stop_button = QPushButton("STOP")
        self.stop_button.clicked.connect(self.stop_mirror)
        self.stop_button.setEnabled(False)
        self.stop_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 0, 0, 0.15);
                color: #ff4444;
                font-weight: bold;
                font-size: 12px;
                padding: 12px 20px;
                border: 1px solid rgba(255, 0, 0, 0.3);
                border-radius: 30px;
                backdrop-filter: blur(10px);
                box-shadow:
                    0 0 20px rgba(255, 0, 0, 0.3),
                    inset 0 0 20px rgba(255, 0, 0, 0.1),
                    0 4px 15px rgba(0, 0, 0, 0.3);
                transition: all 0.3s ease;
                text-shadow: 0 0 10px rgba(255, 68, 68, 0.8);
            }
            QPushButton:hover {
                background-color: rgba(255, 0, 0, 0.25);
                border: 1px solid rgba(255, 0, 0, 0.6);
                box-shadow:
                    0 0 30px rgba(255, 0, 0, 0.6),
                    inset 0 0 30px rgba(255, 0, 0, 0.2),
                    0 6px 20px rgba(0, 0, 0, 0.4);
                transform: translateY(-2px);
            }
            QPushButton:pressed {
                background-color: rgba(255, 0, 0, 0.1);
                box-shadow:
                    0 0 10px rgba(255, 0, 0, 0.4),
                    inset 0 0 15px rgba(255, 0, 0, 0.3),
                    0 2px 8px rgba(0, 0, 0, 0.5);
                transform: translateY(1px);
            }
            QPushButton:disabled {
                background-color: rgba(100, 100, 100, 0.15);
                color: #666666;
                border: 1px solid rgba(100, 100, 100, 0.3);
                box-shadow: none;
                text-shadow: none;
            }
        """)
        button_layout.addWidget(self.stop_button)
        
        self.clear_button = QPushButton("CLEAR")
        self.clear_button.clicked.connect(self.clear_all)
        self.clear_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 102, 204, 0.15);
                color: #44aaff;
                font-weight: bold;
                font-size: 12px;
                padding: 12px 20px;
                border: 1px solid rgba(0, 102, 204, 0.3);
                border-radius: 30px;
                backdrop-filter: blur(10px);
                box-shadow:
                    0 0 20px rgba(0, 102, 204, 0.3),
                    inset 0 0 20px rgba(0, 102, 204, 0.1),
                    0 4px 15px rgba(0, 0, 0, 0.3);
                transition: all 0.3s ease;
                text-shadow: 0 0 10px rgba(68, 170, 255, 0.8);
            }
            QPushButton:hover {
                background-color: rgba(0, 102, 204, 0.25);
                border: 1px solid rgba(0, 102, 204, 0.6);
                box-shadow:
                    0 0 30px rgba(0, 102, 204, 0.6),
                    inset 0 0 30px rgba(0, 102, 204, 0.2),
                    0 6px 20px rgba(0, 0, 0, 0.4);
                transform: translateY(-2px);
            }
            QPushButton:pressed {
                background-color: rgba(0, 102, 204, 0.1);
                box-shadow:
                    0 0 10px rgba(0, 102, 204, 0.4),
                    inset 0 0 15px rgba(0, 102, 204, 0.3),
                    0 2px 8px rgba(0, 0, 0, 0.5);
                transform: translateY(1px);
            }
        """)
        button_layout.addWidget(self.clear_button)
        
        # About button
        self.about_button = QPushButton("ABOUT")
        self.about_button.clicked.connect(self.show_about)
        self.about_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 215, 0, 0.15);
                color: #ffd700;
                font-weight: bold;
                font-size: 12px;
                padding: 12px 20px;
                border: 1px solid rgba(255, 215, 0, 0.3);
                border-radius: 30px;
                backdrop-filter: blur(10px);
                box-shadow:
                    0 0 20px rgba(255, 215, 0, 0.3),
                    inset 0 0 20px rgba(255, 215, 0, 0.1),
                    0 4px 15px rgba(0, 0, 0, 0.3);
                transition: all 0.3s ease;
                text-shadow: 0 0 10px rgba(255, 215, 0, 0.8);
            }
            QPushButton:hover {
                background-color: rgba(255, 215, 0, 0.25);
                border: 1px solid rgba(255, 215, 0, 0.6);
                box-shadow:
                    0 0 30px rgba(255, 215, 0, 0.6),
                    inset 0 0 30px rgba(255, 215, 0, 0.2),
                    0 6px 20px rgba(0, 0, 0, 0.4);
                transform: translateY(-2px);
            }
            QPushButton:pressed {
                background-color: rgba(255, 215, 0, 0.1);
                box-shadow:
                    0 0 10px rgba(255, 215, 0, 0.4),
                    inset 0 0 15px rgba(255, 215, 0, 0.3),
                    0 2px 8px rgba(0, 0, 0, 0.5);
                transform: translateY(1px);
            }
        """)
        button_layout.addWidget(self.about_button)
        
        left_layout.addLayout(button_layout)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid rgba(0, 255, 0, 0.4);
                border-radius: 20px;
                text-align: center;
                background-color: rgba(0, 0, 0, 0.3);
                color: #00ff00;
                font-weight: bold;
                font-size: 11px;
                padding: 3px;
                backdrop-filter: blur(5px);
                box-shadow:
                    inset 0 0 10px rgba(0, 255, 0, 0.2),
                    0 2px 8px rgba(0, 0, 0, 0.5);
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(0, 255, 0, 0.6),
                    stop:0.5 rgba(0, 255, 0, 0.8),
                    stop:1 rgba(0, 255, 0, 1));
                border-radius: 13px;
                box-shadow: 0 0 10px rgba(0, 255, 0, 0.5);
            }
        """)
        left_layout.addWidget(self.progress_bar)
        
        # Log area
        log_group = QGroupBox("Console Log")
        log_layout = QVBoxLayout()
        
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setMaximumHeight(150)
        self.log_output.setStyleSheet("""
            QTextEdit {
                background-color: rgba(0, 0, 0, 0.8);
                color: #00ff00;
                font-family: 'Courier New', monospace;
                border: 1px solid rgba(0, 255, 0, 0.3);
                border-radius: 15px;
                backdrop-filter: blur(5px);
                box-shadow:
                    inset 0 0 20px rgba(0, 255, 0, 0.1),
                    0 3px 10px rgba(0, 0, 0, 0.3);
                font-size: 11px;
                line-height: 1.4;
            }
            QTextEdit QScrollBar:vertical {
                background-color: rgba(0, 0, 0, 0.5);
                width: 12px;
                border-radius: 6px;
            }
            QTextEdit QScrollBar::handle:vertical {
                background-color: rgba(0, 255, 0, 0.4);
                border-radius: 6px;
                min-height: 20px;
            }
            QTextEdit QScrollBar::handle:vertical:hover {
                background-color: rgba(0, 255, 0, 0.6);
            }
        """)
        log_layout.addWidget(self.log_output)
        
        log_group.setLayout(log_layout)
        left_layout.addWidget(log_group)
        
        left_layout.addStretch()
        
        # Panel kanan - Results table
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        
        # Results table
        results_group = QGroupBox("Mirror Results")
        results_layout = QVBoxLayout()
        
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(5)
        self.results_table.setHorizontalHeaderLabels(['URL', 'Status', 'Status Code', 'Title', 'Timestamp'])
        
        # Auto resize columns
        header = self.results_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.Stretch)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        
        self.results_table.setStyleSheet("""
            QTableWidget {
                background-color: rgba(26, 26, 26, 0.7);
                color: #00ff00;
                gridline-color: rgba(0, 255, 0, 0.2);
                border: 1px solid rgba(0, 255, 0, 0.3);
                border-radius: 18px;
                backdrop-filter: blur(5px);
                box-shadow:
                    inset 0 0 15px rgba(0, 255, 0, 0.1),
                    0 3px 10px rgba(0, 0, 0, 0.3);
            }
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid rgba(0, 255, 0, 0.1);
            }
            QTableWidget::item:selected {
                background-color: rgba(0, 100, 0, 0.4);
                color: #00ff00;
                border: 1px solid rgba(0, 255, 0, 0.5);
            }
            QHeaderView::section {
                background-color: rgba(0, 80, 0, 0.6);
                color: #00ff00;
                padding: 10px 5px;
                border: 1px solid rgba(0, 255, 0, 0.3);
                font-weight: bold;
                font-size: 12px;
                backdrop-filter: blur(5px);
            }
            QHeaderView::section:first {
                border-top-left-radius: 12px;
            }
            QHeaderView::section:last {
                border-top-right-radius: 12px;
            }
        """)
        
        results_layout.addWidget(self.results_table)
        
        # Statistics
        stats_layout = QHBoxLayout()
        
        self.total_label = QLabel("Total: 0")
        self.success_label = QLabel("Success: 0")
        self.failed_label = QLabel("Failed: 0")
        
        for label in [self.total_label, self.success_label, self.failed_label]:
            label.setStyleSheet("""
                QLabel {
                    color: #00ff00;
                    font-weight: bold;
                    padding: 8px 12px;
                    border: 1px solid rgba(0, 255, 0, 0.3);
                    border-radius: 20px;
                    background-color: rgba(0, 255, 0, 0.08);
                    backdrop-filter: blur(5px);
                    box-shadow:
                        0 0 10px rgba(0, 255, 0, 0.2),
                        inset 0 0 8px rgba(0, 255, 0, 0.1);
                    text-shadow: 0 0 5px rgba(0, 255, 0, 0.5);
                    font-size: 11px;
                    margin: 2px;
                }
            """)
            stats_layout.addWidget(label)
        
        stats_layout.addStretch()
        results_layout.addLayout(stats_layout)
        
        results_group.setLayout(results_layout)
        right_layout.addWidget(results_group)
        
        # Tambahkan panel ke splitter
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setSizes([400, 800])
        
        main_layout.addWidget(splitter)
        
        # Status bar
        self.statusBar().showMessage('Ready - Zone-H Mass Mirror Tool v1.0')
        self.statusBar().setStyleSheet("""
            QStatusBar {
                background-color: rgba(0, 0, 0, 0.9);
                color: #00ff00;
                border-top: 1px solid rgba(0, 255, 0, 0.3);
                font-family: 'Courier New', monospace;
                font-size: 11px;
                padding: 5px;
                backdrop-filter: blur(5px);
                box-shadow: 0 -2px 10px rgba(0, 255, 0, 0.1);
            }
        """)
        
    def apply_hacker_theme(self):
        """Terapkan tema hacker (hitam dan biru)"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #000000;
                color: #00ff00;
            }
            QWidget {
                background-color: #000000;
                color: #00ff00;
            }
            QGroupBox {
                color: #00ff00;
                border: 1px solid rgba(0, 255, 0, 0.4);
                border-radius: 15px;
                margin-top: 10px;
                font-weight: bold;
                padding-top: 10px;
                background-color: rgba(0, 255, 0, 0.05);
                backdrop-filter: blur(5px);
                box-shadow:
                    0 0 15px rgba(0, 255, 0, 0.2),
                    inset 0 0 10px rgba(0, 255, 0, 0.1);
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
            QTextEdit {
                background-color: rgba(10, 10, 10, 0.7);
                color: #00ff00;
                border: 1px solid rgba(0, 255, 0, 0.4);
                border-radius: 10px;
                font-family: 'Courier New', monospace;
                backdrop-filter: blur(5px);
                box-shadow:
                    inset 0 0 15px rgba(0, 255, 0, 0.1),
                    0 2px 8px rgba(0, 0, 0, 0.3);
            }
            QLineEdit {
                background-color: rgba(10, 10, 10, 0.7);
                color: #00ff00;
                border: 1px solid rgba(0, 255, 0, 0.4);
                border-radius: 12px;
                padding: 8px;
                backdrop-filter: blur(5px);
                box-shadow:
                    inset 0 0 10px rgba(0, 255, 0, 0.1),
                    0 2px 5px rgba(0, 0, 0, 0.3);
            }
            QSpinBox {
                background-color: rgba(10, 10, 10, 0.7);
                color: #00ff00;
                border: 1px solid rgba(0, 255, 0, 0.4);
                border-radius: 12px;
                padding: 5px;
                backdrop-filter: blur(5px);
                box-shadow:
                    inset 0 0 8px rgba(0, 255, 0, 0.1),
                    0 2px 5px rgba(0, 0, 0, 0.3);
            }
            QComboBox {
                background-color: rgba(10, 10, 10, 0.7);
                color: #00ff00;
                border: 1px solid rgba(0, 255, 0, 0.4);
                border-radius: 12px;
                padding: 5px;
                backdrop-filter: blur(5px);
                box-shadow:
                    inset 0 0 8px rgba(0, 255, 0, 0.1),
                    0 2px 5px rgba(0, 0, 0, 0.3);
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #00ff00;
            }
        """)
        
        # Menu bar
        self.create_menu_bar()
        
    def create_menu_bar(self):
        """Buat menu bar dengan opsi About"""
        menubar = self.menuBar()
        
        # Help menu
        help_menu = menubar.addMenu('Help')
        
        # About action
        about_action = help_menu.addAction('About')
        about_action.triggered.connect(self.show_about)
        
        # Style the menu bar
        menubar.setStyleSheet("""
            QMenuBar {
                background-color: rgba(0, 0, 0, 0.9);
                color: #00ff00;
                border-bottom: 1px solid rgba(0, 255, 0, 0.3);
                font-family: 'Courier New', monospace;
                font-size: 12px;
            }
            QMenuBar::item {
                background-color: transparent;
                padding: 6px 10px;
                margin: 2px;
                border-radius: 5px;
            }
            QMenuBar::item:selected {
                background-color: rgba(0, 255, 0, 0.2);
                border: 1px solid rgba(0, 255, 0, 0.4);
            }
            QMenu {
                background-color: rgba(0, 0, 0, 0.95);
                color: #00ff00;
                border: 1px solid rgba(0, 255, 0, 0.4);
                border-radius: 8px;
                font-family: 'Courier New', monospace;
                font-size: 11px;
            }
            QMenu::item {
                padding: 8px 20px;
                border-radius: 5px;
            }
            QMenu::item:selected {
                background-color: rgba(0, 255, 0, 0.3);
                border: 1px solid rgba(0, 255, 0, 0.6);
            }
        """)
        
    def show_about(self):
        """Tampilkan about dialog"""
        about_dialog = AboutDialog(self)
        about_dialog.exec_()
        
    def show_help_quick(self):
        """Tampilkan help cepat"""
        help_text = """
🛡️ ZONE-H MASS MIRROR TOOL - QUICK HELP

🔧 LANGKAH PENGGUNAAN:
1. Masukkan URLs di area input (satu per baris)
2. Atur delay dan timeout sesuai kebutuhan
3. Pilih user agent yang sesuai
4. Klik START MIRROR untuk memulai
5. Monitor progress di progress bar
6. Lihat hasil di tabel kanan

📊 FITUR UTAMA:
• Mass mirror multiple URLs
• Real-time progress monitoring
• Export hasil ke JSON/CSV
• Error handling yang robust
• Thread-safe operation

⚠️ TIPS:
• Gunakan delay 2-3 detik untuk hasil optimal
• Periksa koneksi internet sebelum mulai
• Validasi URLs untuk menghindari error

💡 KLIK "About" untuk info lebih lanjut!
        """
        QMessageBox.information(self, "Quick Help", help_text)
        
    def start_mirror(self):
        """Mulai proses mass mirror"""
        # Ambil URLs dari input
        urls_text = self.url_input.toPlainText().strip()
        if not urls_text:
            QMessageBox.warning(self, 'Warning', 'Please enter at least one URL!')
            return
            
        # Parse URLs
        urls = [url.strip() for url in urls_text.split('\n') if url.strip()]
        if not urls:
            QMessageBox.warning(self, 'Warning', 'Please enter valid URLs!')
            return
            
        # Update UI
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.clear_button.setEnabled(False)
        self.progress_bar.setValue(0)
        self.results.clear()
        self.results_table.setRowCount(0)
        
        # Update status
        self.statusBar().showMessage(f'Mirroring {len(urls)} URLs...')
        self.log_output.append(f"[{datetime.now().strftime('%H:%M:%S')}] Starting mass mirror for {len(urls)} URLs...")
        
        # Buat dan jalankan thread
        self.mirror_thread = ZoneHMirror(urls, self.delay_spinbox.value())
        self.mirror_thread.progress_updated.connect(self.update_progress)
        self.mirror_thread.log_updated.connect(self.update_log)
        self.mirror_thread.mirror_completed.connect(self.add_result)
        self.mirror_thread.finished.connect(self.mirror_finished)
        self.mirror_thread.start()
        
    def stop_mirror(self):
        """Hentikan proses mirror"""
        if self.mirror_thread and self.mirror_thread.isRunning():
            self.mirror_thread.stop()
            self.log_output.append(f"[{datetime.now().strftime('%H:%M:%S')}] Stopping mirror process...")
            self.statusBar().showMessage('Stopping mirror process...')
            
    def update_progress(self, value):
        """Update progress bar"""
        self.progress_bar.setValue(value)
        
    def update_log(self, message):
        """Update log output"""
        self.log_output.append(message)
        
    def add_result(self, result):
        """Tambahkan hasil ke tabel"""
        row_position = self.results_table.rowCount()
        self.results_table.insertRow(row_position)
        
        # Tambahkan data ke tabel
        self.results_table.setItem(row_position, 0, QTableWidgetItem(result['url']))
        self.results_table.setItem(row_position, 1, QTableWidgetItem(result['status']))
        self.results_table.setItem(row_position, 2, QTableWidgetItem(str(result['status_code'])))
        self.results_table.setItem(row_position, 3, QTableWidgetItem(result['title']))
        self.results_table.setItem(row_position, 4, QTableWidgetItem(result['timestamp']))
        
        # Warna berdasarkan status
        if result['status'] == 'Success':
            for col in range(5):
                self.results_table.item(row_position, col).setBackground(QColor(0, 50, 0))
        else:
            for col in range(5):
                self.results_table.item(row_position, col).setBackground(QColor(50, 0, 0))
                
        # Update statistik
        self.update_statistics()
        
    def update_statistics(self):
        """Update label statistik"""
        total = self.results_table.rowCount()
        success = 0
        failed = 0
        
        for row in range(total):
            status = self.results_table.item(row, 1).text()
            if status == 'Success':
                success += 1
            else:
                failed += 1
                
        self.total_label.setText(f"Total: {total}")
        self.success_label.setText(f"Success: {success}")
        self.failed_label.setText(f"Failed: {failed}")
        
    def mirror_finished(self):
        """Mirror selesai"""
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.clear_button.setEnabled(True)
        self.statusBar().showMessage('Mirror completed!')
        self.log_output.append(f"[{datetime.now().strftime('%H:%M:%S')}] Mirror process completed!")
        
    def clear_all(self):
        """Bersihkan semua data"""
        self.url_input.clear()
        self.results_table.setRowCount(0)
        self.log_output.clear()
        self.progress_bar.setValue(0)
        self.results.clear()
        self.update_statistics()
        # Quick help button in status bar
        self.statusBar().addPermanentWidget(QLabel(" | "))
        help_label = QLabel("🛡️ About")
        help_label.setStyleSheet("color: #00ff00; font-weight: bold;")
        help_label.setToolTip("Click to open About dialog")
        help_label.mousePressEvent = lambda event: self.show_about()
        self.statusBar().addPermanentWidget(help_label)
        
        self.statusBar().showMessage('Ready - Zone-H Mass Mirror Tool v1.0')
        
    def load_urls_from_file(self):
        """Load URLs from file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Load URLs from File", "", "Text Files (*.txt);;All Files (*.*)"
        )
        
        if file_path:
            try:
                urls = load_urls_from_file(file_path)
                if urls:
                    self.url_input.clear()
                    self.url_input.setPlainText('\n'.join(urls))
                    self.log_output.append(f"[{datetime.now().strftime('%H:%M:%S')}] Loaded {len(urls)} URLs from {os.path.basename(file_path)}")
                    self.statusBar().showMessage(f'Loaded {len(urls)} URLs from file')
                else:
                    QMessageBox.warning(self, 'Warning', 'No valid URLs found in file!')
            except Exception as e:
                QMessageBox.critical(self, 'Error', f'Failed to load URLs: {str(e)}')
                
    def export_results_json(self):
        """Export results to JSON file"""
        if not self.results:
            QMessageBox.warning(self, 'Warning', 'No results to export!')
            return
            
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Export Results to JSON", f"mirror_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            "JSON Files (*.json);;All Files (*.*)"
        )
        
        if file_path:
            try:
                save_results_to_json(self.results, file_path)
                self.log_output.append(f"[{datetime.now().strftime('%H:%M:%S')}] Results exported to {os.path.basename(file_path)}")
                self.statusBar().showMessage(f'Results exported to {os.path.basename(file_path)}')
                QMessageBox.information(self, 'Success', f'Results exported successfully!\nFile: {os.path.basename(file_path)}')
            except Exception as e:
                QMessageBox.critical(self, 'Error', f'Failed to export results: {str(e)}')
                
    def export_results_csv(self):
        """Export results to CSV file"""
        if not self.results:
            QMessageBox.warning(self, 'Warning', 'No results to export!')
            return
            
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Export Results to CSV", f"mirror_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            "CSV Files (*.csv);;All Files (*.*)"
        )
        
        if file_path:
            try:
                save_results_to_csv(self.results, file_path)
                self.log_output.append(f"[{datetime.now().strftime('%H:%M:%S')}] Results exported to {os.path.basename(file_path)}")
                self.statusBar().showMessage(f'Results exported to {os.path.basename(file_path)}')
                QMessageBox.information(self, 'Success', f'Results exported successfully!\nFile: {os.path.basename(file_path)}')
            except Exception as e:
                QMessageBox.critical(self, 'Error', f'Failed to export results: {str(e)}')
        
    def start_glow_animation(self):
        """Start the pulsing glow animation for buttons"""
        self.glow_timer.timeout.connect(self.update_glow_effect)
        self.glow_timer.start(100)  # Update every 100ms
        
    def update_glow_effect(self):
        """Update the glow effect animation"""
        self.glow_phase += 0.2
        if self.glow_phase > 6.28:  # 2 * pi
            self.glow_phase = 0
            
        # Calculate glow intensity using sine wave
        intensity = (math.sin(self.glow_phase) + 1) / 2  # 0 to 1
        glow_strength = 0.3 + (intensity * 0.4)  # 0.3 to 0.7
        
        # Update START button glow
        if self.start_button.isEnabled():
            glow_color = f"rgba(0, 255, 0, {glow_strength})"
            self.start_button.setStyleSheet(f"""
                QPushButton {{
                    background-color: rgba(0, 255, 0, 0.15);
                    color: #00ff00;
                    font-weight: bold;
                    font-size: 12px;
                    padding: 12px 20px;
                    border: 1px solid rgba(0, 255, 0, 0.3);
                    border-radius: 30px;
                    backdrop-filter: blur(10px);
                    box-shadow:
                        0 0 {20 + int(intensity * 15)}px {glow_color},
                        inset 0 0 20px rgba(0, 255, 0, 0.1),
                        0 4px 15px rgba(0, 0, 0, 0.3);
                    transition: all 0.3s ease;
                    text-shadow: 0 0 {10 + int(intensity * 5)}px rgba(0, 255, 0, 0.8);
                }}
                QPushButton:hover {{
                    background-color: rgba(0, 255, 0, 0.25);
                    border: 1px solid rgba(0, 255, 0, 0.6);
                    box-shadow:
                        0 0 30px rgba(0, 255, 0, 0.6),
                        inset 0 0 30px rgba(0, 255, 0, 0.2),
                        0 6px 20px rgba(0, 0, 0, 0.4);
                    transform: translateY(-2px);
                }}
                QPushButton:pressed {{
                    background-color: rgba(0, 255, 0, 0.1);
                    box-shadow:
                        0 0 10px rgba(0, 255, 0, 0.4),
                        inset 0 0 15px rgba(0, 255, 0, 0.3),
                        0 2px 8px rgba(0, 0, 0, 0.5);
                    transform: translateY(1px);
                }}
                QPushButton:disabled {{
                    background-color: rgba(100, 100, 100, 0.15);
                    color: #666666;
                    border: 1px solid rgba(100, 100, 100, 0.3);
                    box-shadow: none;
                    text-shadow: none;
                }}
            """)
        
    def closeEvent(self, event):
        """Handle close event"""
        # Stop glow animation
        if self.glow_timer.isActive():
            self.glow_timer.stop()
            
        if self.mirror_thread and self.mirror_thread.isRunning():
            reply = QMessageBox.question(self, 'Exit',
                                       'Mirror process is still running. Are you sure you want to exit?',
                                       QMessageBox.Yes | QMessageBox.No,
                                       QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.mirror_thread.stop()
                self.mirror_thread.wait()
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()

def main():
    """Fungsi utama"""
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    # Create and show main window
    window = ZoneHApp()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()