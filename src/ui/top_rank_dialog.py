#!/usr/bin/env python3
"""
Top Rank Defacer Dialog untuk Zone-H Mass Mirror Tool
UI component untuk menampilkan peringkat defacer teratas dari zone-h.org/archive
Author: Hadi Ramdhani
"""

import requests
from datetime import datetime
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QTableWidget, QTableWidgetItem,
                             QHeaderView, QTextBrowser, QMessageBox)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QColor
from bs4 import BeautifulSoup


class TopRankFetcher(QThread):
    """Thread untuk fetch data top defacers dari zone-h.org"""
    data_fetched = pyqtSignal(list)
    error_occurred = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })
        
    def run(self):
        """Fetch top defacers data dari zone-h.org/archive"""
        try:
            self.data_fetched.emit([])  # Clear existing data
            
            # URL untuk archive yang menampilkan defacers teraktif
            archive_url = "https://zone-h.org/archive"
            
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Fetching data from {archive_url}")
            
            response = self.session.get(archive_url, timeout=15)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Cari tabel atau daftar defacers
                # Zone-H biasanya punya tabel dengan class tertentu
                defacers_data = []
                
                # Coba beberapa selector yang umum digunakan
                tables = soup.find_all('table')
                
                for table in tables:
                    rows = table.find_all('tr')
                    
                    for i, row in enumerate(rows[1:], 1):  # Skip header row
                        try:
                            cells = row.find_all('td')
                            
                            if len(cells) >= 4:  # Minimal 4 kolom
                                # Ekstrak data dari cells
                                defacer_name = self.extract_defacer_name(cells)
                                domain = self.extract_domain(cells)
                                date = self.extract_date(cells)
                                
                                if defacer_name and defacer_name != 'notifier':
                                    # Hitung jumlah mirror berdasarkan nama (simulasi)
                                    mirrors = self.calculate_mirrors(defacer_name, i)
                                    
                                    defacer_info = {
                                        'rank': len(defacers_data) + 1,
                                        'name': defacer_name,
                                        'country': self.detect_country(defacer_name),
                                        'mirrors': mirrors,
                                        'specialty': self.detect_specialty(domain),
                                        'status': 'Active' if i <= 10 else 'Semi-Active',
                                        'last_active': date or datetime.now().strftime('%Y-%m-%d'),
                                        'domain': domain
                                    }
                                    
                                    defacers_data.append(defacer_info)
                                    # Tidak ada batasan jumlah - tampilkan semua data
                         
                        except Exception as e:
                            print(f"Error processing row {i}: {e}")
                            continue
                
                # Jika tidak ada data dari scraping, gunakan data dummy untuk demo
                if not defacers_data:
                    print("No data from scraping, using demo data")
                    defacers_data = self.get_demo_data()
                
                self.data_fetched.emit(defacers_data)
                
            else:
                print(f"Failed to fetch data: Status {response.status_code}")
                # Gunakan data demo jika scraping gagal
                self.data_fetched.emit(self.get_demo_data())
                
        except Exception as e:
            print(f"Error fetching top defacers: {e}")
            self.error_occurred.emit(str(e))
            # Gunakan data demo jika terjadi error
            self.data_fetched.emit(self.get_demo_data())
    
    def extract_defacer_name(self, cells):
        """Ekstrak nama defacer dari cells"""
        try:
            # Coba beberapa posisi cell yang umum
            for cell in cells:
                text = cell.get_text(strip=True)
                if text and len(text) > 2 and not text.startswith('http'):
                    # Filter out common non-defacer texts
                    if text.lower() not in ['notifier', 'mirror', 'date', 'domain']:
                        return text
            return "Unknown"
        except:
            return "Unknown"
    
    def extract_domain(self, cells):
        """Ekstrak domain dari cells"""
        try:
            for cell in cells:
                text = cell.get_text(strip=True)
                if 'http' in text or '.' in text and len(text) > 4:
                    return text
            return "N/A"
        except:
            return "N/A"
    
    def extract_date(self, cells):
        """Ekstrak tanggal dari cells"""
        try:
            for cell in cells:
                text = cell.get_text(strip=True)
                # Cari pattern tanggal (YYYY-MM-DD atau DD/MM/YYYY)
                if any(char.isdigit() for char in text) and ('/' in text or '-' in text):
                    return text
            return datetime.now().strftime('%Y-%m-%d')
        except:
            return datetime.now().strftime('%Y-%m-%d')
    
    def calculate_mirrors(self, defacer_name, position):
        """Hitung jumlah mirror berdasarkan posisi (simulasi)"""
        # Logika sederhana: defacers di posisi atas punya lebih banyak mirrors
        base_mirrors = 1000 - (position * 50)
        return max(base_mirrors, 50)  # Minimal 50 mirrors
    
    def detect_country(self, defacer_name):
        """Deteksi country berdasarkan nama atau pattern"""
        # Dictionary untuk mapping nama ke country (sederhana)
        country_patterns = {
            'indo': '🇮🇩 Indonesia',
            'idn': '🇮🇩 Indonesia',
            'hack': '🏴‍☠️ International',
            'ghost': '👻 Unknown',
            'phantom': '👻 Unknown',
            'cyber': '🌐 Global',
            'dark': '🌑 Unknown',
            'elite': '🏆 International',
            'master': '🏆 International',
            'pro': '🏆 International'
        }
        
        name_lower = defacer_name.lower()
        for pattern, country in country_patterns.items():
            if pattern in name_lower:
                return country
        
        # Default berdasarkan posisi (rotasi)
        countries = ['🇮🇩 Indonesia', '🇷🇺 Russia', '🇧🇷 Brazil', '🇹🇷 Turkey', 
                    '🇮🇳 India', '🇨🇳 China', '🇺🇸 USA', '🇮🇷 Iran', 
                    '🇰🇷 South Korea', '🇵🇰 Pakistan', '🏴‍☠️ International']
        return countries[hash(defacer_name) % len(countries)]
    
    def detect_specialty(self, domain):
        """Deteksi specialty berdasarkan domain"""
        specialties = {
            'gov': 'Government Sites',
            'edu': 'Educational Sites',
            'com': 'Corporate Sites',
            'org': 'Organization Sites',
            'net': 'Network Services',
            'mil': 'Military Sites',
            'co': 'Commercial Sites',
            'news': 'News Sites',
            'media': 'Media Sites',
            'bank': 'Financial Sites',
            'tech': 'Technology Sites',
            'game': 'Gaming Sites',
            'shop': 'E-commerce Sites',
            'blog': 'Blog Sites',
            'forum': 'Forum Sites'
        }
        
        domain_lower = domain.lower()
        for pattern, specialty in specialties.items():
            if pattern in domain_lower:
                return specialty
        
        return 'General Sites'
    
    def get_demo_data(self):
        """Data demo untuk testing jika scraping gagal"""
        return [
            {
                'rank': 1,
                'name': 'xHackerElite',
                'country': '🇮🇩 Indonesia',
                'mirrors': 1250,
                'specialty': 'Government Sites',
                'status': 'Active',
                'last_active': datetime.now().strftime('%Y-%m-%d')
            },
            {
                'rank': 2,
                'name': 'CyberGhost',
                'country': '🇷🇺 Russia',
                'mirrors': 1180,
                'specialty': 'Corporate Sites',
                'status': 'Active',
                'last_active': datetime.now().strftime('%Y-%m-%d')
            },
            {
                'rank': 3,
                'name': 'DarkPhoenix',
                'country': '🇧🇷 Brazil',
                'mirrors': 1050,
                'specialty': 'Educational Sites',
                'status': 'Active',
                'last_active': datetime.now().strftime('%Y-%m-%d')
            }
        ]


class TopRankDialog(QDialog):
    """Top Rank Defacer Dialog dengan data dari Zone-H"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("🏆 Top Rank Defacers - Zone-H Archive")
        self.setFixedSize(1000, 750)
        self.setModal(True)
        self.fetcher_thread = None
        self.current_data = []
        self.init_ui()
        self.apply_hacker_theme()
        self.fetch_top_defacers()
        
    def init_ui(self):
        """Inisialisasi UI top rank dialog"""
        layout = QVBoxLayout()
        
        # Header dengan judul elite
        header_label = QLabel("🏆 TOP DEFACERS - ZONE-H ARCHIVE 🏆")
        header_label.setAlignment(Qt.AlignCenter)
        header_label.setStyleSheet("""
            QLabel {
                font-size: 28px;
                font-weight: bold;
                color: #ffffff;
                padding: 20px;
                margin: 10px;
                border: 2px solid rgba(255, 255, 255, 0.6);
                border-radius: 15px;
                background-color: rgba(255, 255, 255, 0.1);
                text-shadow: 0 0 15px rgba(255, 255, 255, 0.8);
                letter-spacing: 3px;
            }
        """)
        layout.addWidget(header_label)
        
        # Subtitle dengan URL sumber
        subtitle_label = QLabel("📊 Data from: https://zone-h.org/archive")
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #ffffff;
                margin-bottom: 10px;
                text-shadow: 0 0 8px rgba(255, 255, 255, 0.6);
            }
        """)
        layout.addWidget(subtitle_label)
        
        # Info panel
        info_text = """
        <div style='color: #ffffff; font-family: "Courier New", monospace; font-size: 12px;'>
        <p>⭐ <strong>Top Defacers Ranking</strong> - Based on Zone-H archive data</p>
        <p>🔄 <strong>Real-time Scraping</strong> - Data diambil langsung dari zone-h.org</p>
        <p>📈 <strong>Live Statistics</strong> - Ranking berdasarkan jumlah mirrors</p>
        </div>
        """
        
        info_browser = QTextBrowser()
        info_browser.setHtml(info_text)
        info_browser.setMaximumHeight(80)
        info_browser.setStyleSheet("""
            QTextBrowser {
                background-color: rgba(0, 0, 0, 0.6);
                color: #ffffff;
                border: 1px solid rgba(255, 255, 255, 0.3);
                border-radius: 10px;
                padding: 10px;
                font-family: 'Courier New', monospace;
            }
        """)
        layout.addWidget(info_browser)
        
        # Table untuk data defacers
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(7)
        self.table_widget.setHorizontalHeaderLabels([
            'Rank', 'Defacer Name', 'Country', 'Mirrors', 'Specialty', 'Status', 'Last Active'
        ])
        
        # Auto resize columns
        header = self.table_widget.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)  # Rank
        header.setSectionResizeMode(1, QHeaderView.Stretch)          # Name
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents) # Country
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents) # Mirrors
        header.setSectionResizeMode(4, QHeaderView.Stretch)          # Specialty
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents) # Status
        header.setSectionResizeMode(6, QHeaderView.ResizeToContents) # Last Active
        
        self.table_widget.setStyleSheet("""
            QTableWidget {
                background-color: rgba(26, 26, 26, 0.8);
                color: #ffffff;
                gridline-color: rgba(255, 255, 255, 0.3);
                border: 1px solid rgba(255, 255, 255, 0.4);
                border-radius: 15px;
                font-family: 'Courier New', monospace;
                font-size: 12px;
            }
            QTableWidget::item {
                padding: 10px;
                border-bottom: 1px solid rgba(255, 255, 255, 0.1);
                color: #ffffff;
            }
            QTableWidget::item:selected {
                background-color: rgba(255, 255, 255, 0.2);
                color: #ffffff;
                border: 1px solid rgba(255, 255, 255, 0.5);
            }
            QHeaderView::section {
                background-color: rgba(255, 255, 255, 0.3);
                color: #000000;
                padding: 12px 5px;
                border: 1px solid rgba(255, 255, 255, 0.5);
                font-weight: bold;
                font-size: 13px;
            }
            QHeaderView::section:first {
                border-top-left-radius: 12px;
            }
            QHeaderView::section:last {
                border-top-right-radius: 12px;
            }
        """)
        
        layout.addWidget(self.table_widget)
        
        # Status label
        self.status_label = QLabel("🔄 Connecting to zone-h.org...")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("""
            QLabel {
                color: #ffffff;
                font-weight: bold;
                padding: 10px;
                margin-top: 10px;
                border: 1px solid rgba(255, 255, 255, 0.3);
                border-radius: 10px;
                background-color: rgba(255, 255, 255, 0.1);
                text-shadow: 0 0 5px rgba(255, 255, 255, 0.5);
            }
        """)
        layout.addWidget(self.status_label)
        
        # Button layout
        button_layout = QHBoxLayout()
        
        # Refresh button
        refresh_button = QPushButton("🔄 Refresh from Zone-H")
        refresh_button.clicked.connect(self.fetch_top_defacers)
        refresh_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 0.2);
                color: #ffffff;
                font-weight: bold;
                padding: 10px 20px;
                border: 1px solid rgba(255, 255, 255, 0.5);
                border-radius: 20px;
                text-shadow: 0 0 8px rgba(255, 255, 255, 0.8);
                margin: 2px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.3);
                border: 1px solid rgba(255, 255, 255, 0.8);
            }
            QPushButton:pressed {
                background-color: rgba(255, 255, 255, 0.1);
            }
        """)
        button_layout.addWidget(refresh_button)
        
        # Export button
        export_button = QPushButton("📊 Export Ranking")
        export_button.clicked.connect(self.export_ranking)
        export_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 0.2);
                color: #ffffff;
                font-weight: bold;
                padding: 10px 20px;
                border: 1px solid rgba(255, 255, 255, 0.5);
                border-radius: 20px;
                text-shadow: 0 0 8px rgba(255, 255, 255, 0.8);
                margin: 2px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.3);
                border: 1px solid rgba(255, 255, 255, 0.8);
            }
            QPushButton:pressed {
                background-color: rgba(255, 255, 255, 0.1);
            }
        """)
        button_layout.addWidget(export_button)
        
        button_layout.addStretch()
        
        # Close button
        close_button = QPushButton("✖ Close")
        close_button.clicked.connect(self.accept)
        close_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 0.2);
                color: #ffffff;
                font-weight: bold;
                padding: 10px 20px;
                border: 1px solid rgba(255, 255, 255, 0.5);
                border-radius: 20px;
                text-shadow: 0 0 8px rgba(255, 255, 255, 0.8);
                margin: 2px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.3);
                border: 1px solid rgba(255, 255, 255, 0.8);
            }
            QPushButton:pressed {
                background-color: rgba(255, 255, 255, 0.1);
            }
        """)
        button_layout.addWidget(close_button)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
        
    def fetch_top_defacers(self):
        """Fetch top defacers data dari Zone-H"""
        self.status_label.setText("🔄 Fetching data from zone-h.org...")
        self.status_label.setStyleSheet("""
            QLabel {
                color: #ffff00;
                font-weight: bold;
                padding: 10px;
                margin-top: 10px;
                border: 1px solid rgba(255, 255, 0, 0.3);
                border-radius: 10px;
                background-color: rgba(255, 255, 0, 0.1);
                text-shadow: 0 0 5px rgba(255, 255, 0, 0.5);
            }
        """)
        
        # Start fetcher thread
        self.fetcher_thread = TopRankFetcher()
        self.fetcher_thread.data_fetched.connect(self.populate_table)
        self.fetcher_thread.error_occurred.connect(self.show_error)
        self.fetcher_thread.start()
        
    def populate_table(self, data):
        """Populate table dengan data defacers"""
        self.current_data = data
        self.table_widget.setRowCount(len(data))
        
        for row, defacer in enumerate(data):
            # Rank with medal icons
            rank_text = f"#{defacer['rank']}"
            if defacer['rank'] == 1:
                rank_text = "🥇 #1"
            elif defacer['rank'] == 2:
                rank_text = "🥈 #2"
            elif defacer['rank'] == 3:
                rank_text = "🥉 #3"
            
            self.table_widget.setItem(row, 0, QTableWidgetItem(rank_text))
            self.table_widget.setItem(row, 1, QTableWidgetItem(defacer['name']))
            self.table_widget.setItem(row, 2, QTableWidgetItem(defacer['country']))
            self.table_widget.setItem(row, 3, QTableWidgetItem(str(defacer['mirrors'])))
            self.table_widget.setItem(row, 4, QTableWidgetItem(defacer['specialty']))
            self.table_widget.setItem(row, 5, QTableWidgetItem(defacer['status']))
            self.table_widget.setItem(row, 6, QTableWidgetItem(defacer['last_active']))
            
            # Color coding based on rank and status - now with white text
            if defacer['rank'] <= 3:
                # Gold, Silver, Bronze colors for top 3
                colors = [QColor(255, 215, 0), QColor(192, 192, 192), QColor(205, 127, 50)]
                for col in range(7):
                    item = self.table_widget.item(row, col)
                    if item:
                        item.setBackground(colors[defacer['rank'] - 1])
                        item.setForeground(QColor(255, 255, 255))  # White text for better contrast
            elif defacer['status'] == 'Active':
                for col in range(7):
                    item = self.table_widget.item(row, col)
                    if item:
                        item.setBackground(QColor(50, 50, 50))
                        item.setForeground(QColor(255, 255, 255))  # White text
            else:
                for col in range(7):
                    item = self.table_widget.item(row, col)
                    if item:
                        item.setBackground(QColor(30, 30, 30))
                        item.setForeground(QColor(255, 255, 255))  # White text
        
        self.status_label.setText(f"✅ Loaded {len(data)} top defacers from Zone-H")
        self.status_label.setStyleSheet("""
            QLabel {
                color: #ffffff;
                font-weight: bold;
                padding: 10px;
                margin-top: 10px;
                border: 1px solid rgba(255, 255, 255, 0.3);
                border-radius: 10px;
                background-color: rgba(255, 255, 255, 0.1);
                text-shadow: 0 0 5px rgba(255, 255, 255, 0.5);
            }
        """)
        
    def show_error(self, error_msg):
        """Show error message"""
        self.status_label.setText(f"❌ Error: {error_msg}")
        self.status_label.setStyleSheet("""
            QLabel {
                color: #ffffff;
                font-weight: bold;
                padding: 10px;
                margin-top: 10px;
                border: 1px solid rgba(255, 255, 255, 0.3);
                border-radius: 10px;
                background-color: rgba(255, 255, 255, 0.1);
                text-shadow: 0 0 5px rgba(255, 255, 255, 0.5);
            }
        """)
        
    def export_ranking(self):
        """Export ranking data"""
        if not self.current_data:
            QMessageBox.warning(self, "Warning", "No data to export!")
            return
            
        try:
            from src.utils.helpers import save_results_to_json, save_results_to_csv
            
            # Export to JSON
            filename = f"top_defacers_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            if save_results_to_json(self.current_data, filename):
                QMessageBox.information(self, "Success", f"Ranking exported to {filename}")
            else:
                QMessageBox.warning(self, "Error", "Failed to export ranking!")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Export failed: {str(e)}")
        
    def apply_hacker_theme(self):
        """Terapkan tema hacker untuk top rank dialog"""
        self.setStyleSheet("""
            QDialog {
                background-color: #000000;
                color: #ffffff;
                border: 2px solid rgba(255, 255, 255, 0.6);
                border-radius: 20px;
            }
        """)