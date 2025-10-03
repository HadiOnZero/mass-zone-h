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
from src.config import DEFAULT_SETTINGS, USER_AGENTS, ERROR_MESSAGES, SUCCESS_MESSAGES, WARNING_MESSAGES
from src.utils import (validate_url, sanitize_url, extract_domain, get_url_info,
                      save_results_to_json, save_results_to_csv, load_urls_from_file,
                      calculate_success_rate, generate_report, ZoneHMirror)
from src.ui import AboutDialog, TopRankDialog

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
                color: #ffffff;
                padding: 15px;
                border: 1px solid rgba(255, 255, 255, 0.4);
                border-radius: 20px;
                background-color: rgba(255, 255, 255, 0.08);
                backdrop-filter: blur(10px);
                box-shadow:
                    0 0 30px rgba(255, 255, 255, 0.3),
                    inset 0 0 20px rgba(255, 255, 255, 0.1);
                text-shadow: 0 0 15px rgba(255, 255, 255, 0.8);
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
                background-color: rgba(255, 255, 255, 0.15);
                color: #ffffff;
                font-weight: bold;
                font-size: 11px;
                padding: 10px 15px;
                border: 1px solid rgba(255, 255, 255, 0.3);
                border-radius: 25px;
                backdrop-filter: blur(10px);
                box-shadow:
                    0 0 15px rgba(255, 255, 255, 0.3),
                    inset 0 0 15px rgba(255, 255, 255, 0.1),
                    0 3px 10px rgba(0, 0, 0, 0.3);
                transition: all 0.3s ease;
                text-shadow: 0 0 8px rgba(255, 255, 255, 0.8);
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.25);
                border: 1px solid rgba(255, 255, 255, 0.6);
                box-shadow:
                    0 0 25px rgba(255, 255, 255, 0.5),
                    inset 0 0 25px rgba(255, 255, 255, 0.2),
                    0 5px 15px rgba(0, 0, 0, 0.4);
                transform: translateY(-1px);
            }
            QPushButton:pressed {
                background-color: rgba(255, 255, 255, 0.1);
                box-shadow:
                    0 0 8px rgba(255, 255, 255, 0.4),
                    inset 0 0 12px rgba(255, 255, 255, 0.3),
                    0 2px 6px rgba(0, 0, 0, 0.5);
                transform: translateY(1px);
            }
        """)
        file_layout.addWidget(self.load_button)
        
        self.export_json_button = QPushButton("EXPORT JSON")
        self.export_json_button.clicked.connect(self.export_results_json)
        self.export_json_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 0.15);
                color: #ffffff;
                font-weight: bold;
                font-size: 11px;
                padding: 10px 15px;
                border: 1px solid rgba(255, 255, 255, 0.3);
                border-radius: 25px;
                backdrop-filter: blur(10px);
                box-shadow:
                    0 0 15px rgba(255, 255, 255, 0.3),
                    inset 0 0 15px rgba(255, 255, 255, 0.1),
                    0 3px 10px rgba(0, 0, 0, 0.3);
                transition: all 0.3s ease;
                text-shadow: 0 0 8px rgba(255, 255, 255, 0.8);
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.25);
                border: 1px solid rgba(255, 255, 255, 0.6);
                box-shadow:
                    0 0 25px rgba(255, 255, 255, 0.5),
                    inset 0 0 25px rgba(255, 255, 255, 0.2),
                    0 5px 15px rgba(0, 0, 0, 0.4);
                transform: translateY(-1px);
            }
            QPushButton:pressed {
                background-color: rgba(255, 255, 255, 0.1);
                box-shadow:
                    0 0 8px rgba(255, 255, 255, 0.4),
                    inset 0 0 12px rgba(255, 255, 255, 0.3),
                    0 2px 6px rgba(0, 0, 0, 0.5);
                transform: translateY(1px);
            }
        """)
        file_layout.addWidget(self.export_json_button)
        
        self.export_csv_button = QPushButton("EXPORT CSV")
        self.export_csv_button.clicked.connect(self.export_results_csv)
        self.export_csv_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 0.15);
                color: #ffffff;
                font-weight: bold;
                font-size: 11px;
                padding: 10px 15px;
                border: 1px solid rgba(255, 255, 255, 0.3);
                border-radius: 25px;
                backdrop-filter: blur(10px);
                box-shadow:
                    0 0 15px rgba(255, 255, 255, 0.3),
                    inset 0 0 15px rgba(255, 255, 255, 0.1),
                    0 3px 10px rgba(0, 0, 0, 0.3);
                transition: all 0.3s ease;
                text-shadow: 0 0 8px rgba(255, 255, 255, 0.8);
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.25);
                border: 1px solid rgba(255, 255, 255, 0.6);
                box-shadow:
                    0 0 25px rgba(255, 255, 255, 0.5),
                    inset 0 0 25px rgba(255, 255, 255, 0.2),
                    0 5px 15px rgba(0, 0, 0, 0.4);
                transform: translateY(-1px);
            }
            QPushButton:pressed {
                background-color: rgba(255, 255, 255, 0.1);
                box-shadow:
                    0 0 8px rgba(255, 255, 255, 0.4),
                    inset 0 0 12px rgba(255, 255, 255, 0.3),
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
                background-color: rgba(255, 255, 255, 0.15);
                color: #ffffff;
                font-weight: bold;
                font-size: 12px;
                padding: 12px 20px;
                border: 1px solid rgba(255, 255, 255, 0.3);
                border-radius: 30px;
                backdrop-filter: blur(10px);
                box-shadow:
                    0 0 20px rgba(255, 255, 255, 0.3),
                    inset 0 0 20px rgba(255, 255, 255, 0.1),
                    0 4px 15px rgba(0, 0, 0, 0.3);
                transition: all 0.3s ease;
                text-shadow: 0 0 10px rgba(255, 255, 255, 0.8);
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.25);
                border: 1px solid rgba(255, 255, 255, 0.6);
                box-shadow:
                    0 0 30px rgba(255, 255, 255, 0.6),
                    inset 0 0 30px rgba(255, 255, 255, 0.2),
                    0 6px 20px rgba(0, 0, 0, 0.4);
                transform: translateY(-2px);
            }
            QPushButton:pressed {
                background-color: rgba(255, 255, 255, 0.1);
                box-shadow:
                    0 0 10px rgba(255, 255, 255, 0.4),
                    inset 0 0 15px rgba(255, 255, 255, 0.3),
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
                background-color: rgba(255, 255, 255, 0.15);
                color: #ffffff;
                font-weight: bold;
                font-size: 12px;
                padding: 12px 20px;
                border: 1px solid rgba(255, 255, 255, 0.3);
                border-radius: 30px;
                backdrop-filter: blur(10px);
                box-shadow:
                    0 0 20px rgba(255, 255, 255, 0.3),
                    inset 0 0 20px rgba(255, 255, 255, 0.1),
                    0 4px 15px rgba(0, 0, 0, 0.3);
                transition: all 0.3s ease;
                text-shadow: 0 0 10px rgba(255, 255, 255, 0.8);
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.25);
                border: 1px solid rgba(255, 255, 255, 0.6);
                box-shadow:
                    0 0 30px rgba(255, 255, 255, 0.6),
                    inset 0 0 30px rgba(255, 255, 255, 0.2),
                    0 6px 20px rgba(0, 0, 0, 0.4);
                transform: translateY(-2px);
            }
            QPushButton:pressed {
                background-color: rgba(255, 255, 255, 0.1);
                box-shadow:
                    0 0 10px rgba(255, 255, 255, 0.4),
                    inset 0 0 15px rgba(255, 255, 255, 0.3),
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
                background-color: rgba(255, 255, 255, 0.15);
                color: #ffffff;
                font-weight: bold;
                font-size: 12px;
                padding: 12px 20px;
                border: 1px solid rgba(255, 255, 255, 0.3);
                border-radius: 30px;
                backdrop-filter: blur(10px);
                box-shadow:
                    0 0 20px rgba(255, 255, 255, 0.3),
                    inset 0 0 20px rgba(255, 255, 255, 0.1),
                    0 4px 15px rgba(0, 0, 0, 0.3);
                transition: all 0.3s ease;
                text-shadow: 0 0 10px rgba(255, 255, 255, 0.8);
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.25);
                border: 1px solid rgba(255, 255, 255, 0.6);
                box-shadow:
                    0 0 30px rgba(255, 255, 255, 0.6),
                    inset 0 0 30px rgba(255, 255, 255, 0.2),
                    0 6px 20px rgba(0, 0, 0, 0.4);
                transform: translateY(-2px);
            }
            QPushButton:pressed {
                background-color: rgba(255, 255, 255, 0.1);
                box-shadow:
                    0 0 10px rgba(255, 255, 255, 0.4),
                    inset 0 0 15px rgba(255, 255, 255, 0.3),
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
                background-color: rgba(255, 255, 255, 0.15);
                color: #ffffff;
                font-weight: bold;
                font-size: 12px;
                padding: 12px 20px;
                border: 1px solid rgba(255, 255, 255, 0.3);
                border-radius: 30px;
                backdrop-filter: blur(10px);
                box-shadow:
                    0 0 20px rgba(255, 255, 255, 0.3),
                    inset 0 0 20px rgba(255, 255, 255, 0.1),
                    0 4px 15px rgba(0, 0, 0, 0.3);
                transition: all 0.3s ease;
                text-shadow: 0 0 10px rgba(255, 255, 255, 0.8);
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.25);
                border: 1px solid rgba(255, 255, 255, 0.6);
                box-shadow:
                    0 0 30px rgba(255, 255, 255, 0.6),
                    inset 0 0 30px rgba(255, 255, 255, 0.2),
                    0 6px 20px rgba(0, 0, 0, 0.4);
                transform: translateY(-2px);
            }
            QPushButton:pressed {
                background-color: rgba(255, 255, 255, 0.1);
                box-shadow:
                    0 0 10px rgba(255, 255, 255, 0.4),
                    inset 0 0 15px rgba(255, 255, 255, 0.3),
                    0 2px 8px rgba(0, 0, 0, 0.5);
                transform: translateY(1px);
            }
        """)
        button_layout.addWidget(self.about_button)
        
        # Top Rank button
        self.top_rank_button = QPushButton("TOP RANK")
        self.top_rank_button.clicked.connect(self.show_top_rank)
        self.top_rank_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 0.15);
                color: #ffffff;
                font-weight: bold;
                font-size: 12px;
                padding: 12px 20px;
                border: 1px solid rgba(255, 255, 255, 0.3);
                border-radius: 30px;
                backdrop-filter: blur(10px);
                box-shadow:
                    0 0 20px rgba(255, 255, 255, 0.3),
                    inset 0 0 20px rgba(255, 255, 255, 0.1),
                    0 4px 15px rgba(0, 0, 0, 0.3);
                transition: all 0.3s ease;
                text-shadow: 0 0 10px rgba(255, 255, 255, 0.8);
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.25);
                border: 1px solid rgba(255, 255, 255, 0.6);
                box-shadow:
                    0 0 30px rgba(255, 255, 255, 0.6),
                    inset 0 0 30px rgba(255, 255, 255, 0.2),
                    0 6px 20px rgba(0, 0, 0, 0.4);
                transform: translateY(-2px);
            }
            QPushButton:pressed {
                background-color: rgba(255, 255, 255, 0.1);
                box-shadow:
                    0 0 10px rgba(255, 255, 255, 0.4),
                    inset 0 0 15px rgba(255, 255, 255, 0.3),
                    0 2px 8px rgba(0, 0, 0, 0.5);
                transform: translateY(1px);
            }
        """)
        button_layout.addWidget(self.top_rank_button)
        
        left_layout.addLayout(button_layout)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid rgba(255, 255, 255, 0.4);
                border-radius: 20px;
                text-align: center;
                background-color: rgba(0, 0, 0, 0.3);
                color: #ffffff;
                font-weight: bold;
                font-size: 11px;
                padding: 3px;
                backdrop-filter: blur(5px);
                box-shadow:
                    inset 0 0 10px rgba(255, 255, 255, 0.2),
                    0 2px 8px rgba(0, 0, 0, 0.5);
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(255, 255, 255, 0.6),
                    stop:0.5 rgba(255, 255, 255, 0.8),
                    stop:1 rgba(255, 255, 255, 1));
                border-radius: 13px;
                box-shadow: 0 0 10px rgba(255, 255, 255, 0.5);
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
                color: #ffffff;
                font-family: 'Courier New', monospace;
                border: 1px solid rgba(255, 255, 255, 0.3);
                border-radius: 15px;
                backdrop-filter: blur(5px);
                box-shadow:
                    inset 0 0 20px rgba(255, 255, 255, 0.1),
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
                background-color: rgba(255, 255, 255, 0.4);
                border-radius: 6px;
                min-height: 20px;
            }
            QTextEdit QScrollBar::handle:vertical:hover {
                background-color: rgba(255, 255, 255, 0.6);
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
                color: #ffffff;
                gridline-color: rgba(255, 255, 255, 0.2);
                border: 1px solid rgba(255, 255, 255, 0.3);
                border-radius: 18px;
                backdrop-filter: blur(5px);
                box-shadow:
                    inset 0 0 15px rgba(255, 255, 255, 0.1),
                    0 3px 10px rgba(0, 0, 0, 0.3);
            }
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            }
            QTableWidget::item:selected {
                background-color: rgba(100, 100, 100, 0.4);
                color: #ffffff;
                border: 1px solid rgba(255, 255, 255, 0.5);
            }
            QHeaderView::section {
                background-color: rgba(80, 80, 80, 0.6);
                color: #ffffff;
                padding: 10px 5px;
                border: 1px solid rgba(255, 255, 255, 0.3);
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
                    color: #ffffff;
                    font-weight: bold;
                    padding: 8px 12px;
                    border: 1px solid rgba(255, 255, 255, 0.3);
                    border-radius: 20px;
                    background-color: rgba(255, 255, 255, 0.08);
                    backdrop-filter: blur(5px);
                    box-shadow:
                        0 0 10px rgba(255, 255, 255, 0.2),
                        inset 0 0 8px rgba(255, 255, 255, 0.1);
                    text-shadow: 0 0 5px rgba(255, 255, 255, 0.5);
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
                color: #ffffff;
                border-top: 1px solid rgba(255, 255, 255, 0.3);
                font-family: 'Courier New', monospace;
                font-size: 11px;
                padding: 5px;
                backdrop-filter: blur(5px);
                box-shadow: 0 -2px 10px rgba(255, 255, 255, 0.1);
            }
        """)
        
    def apply_hacker_theme(self):
        """Terapkan tema hacker (hitam dan putih)"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #000000;
                color: #ffffff;
            }
            QWidget {
                background-color: #000000;
                color: #ffffff;
            }
            QGroupBox {
                color: #ffffff;
                border: 1px solid rgba(255, 255, 255, 0.4);
                border-radius: 15px;
                margin-top: 10px;
                font-weight: bold;
                padding-top: 10px;
                background-color: rgba(255, 255, 255, 0.05);
                backdrop-filter: blur(5px);
                box-shadow:
                    0 0 15px rgba(255, 255, 255, 0.2),
                    inset 0 0 10px rgba(255, 255, 255, 0.1);
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
            QTextEdit {
                background-color: rgba(10, 10, 10, 0.7);
                color: #ffffff;
                border: 1px solid rgba(255, 255, 255, 0.4);
                border-radius: 10px;
                font-family: 'Courier New', monospace;
                backdrop-filter: blur(5px);
                box-shadow:
                    inset 0 0 15px rgba(255, 255, 255, 0.1),
                    0 2px 8px rgba(0, 0, 0, 0.3);
            }
            QLineEdit {
                background-color: rgba(10, 10, 10, 0.7);
                color: #ffffff;
                border: 1px solid rgba(255, 255, 255, 0.4);
                border-radius: 12px;
                padding: 8px;
                backdrop-filter: blur(5px);
                box-shadow:
                    inset 0 0 10px rgba(255, 255, 255, 0.1),
                    0 2px 5px rgba(0, 0, 0, 0.3);
            }
            QSpinBox {
                background-color: rgba(10, 10, 10, 0.7);
                color: #ffffff;
                border: 1px solid rgba(255, 255, 255, 0.4);
                border-radius: 12px;
                padding: 5px;
                backdrop-filter: blur(5px);
                box-shadow:
                    inset 0 0 8px rgba(255, 255, 255, 0.1),
                    0 2px 5px rgba(0, 0, 0, 0.3);
            }
            QComboBox {
                background-color: rgba(10, 10, 10, 0.7);
                color: #ffffff;
                border: 1px solid rgba(255, 255, 255, 0.4);
                border-radius: 12px;
                padding: 5px;
                backdrop-filter: blur(5px);
                box-shadow:
                    inset 0 0 8px rgba(255, 255, 255, 0.1),
                    0 2px 5px rgba(0, 0, 0, 0.3);
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #ffffff;
            }
        """)
        
        # Menu bar
        self.create_menu_bar()
        
    def create_menu_bar(self):
        """Buat menu bar dengan opsi About"""
        menubar = self.menuBar()
        
        # Tools menu
        tools_menu = menubar.addMenu('Tools')
        
        # Top Rank action
        top_rank_action = tools_menu.addAction('Top Rank Defacers')
        top_rank_action.triggered.connect(self.show_top_rank)
        
        # Help menu
        help_menu = menubar.addMenu('Help')
        
        # About action
        about_action = help_menu.addAction('About')
        about_action.triggered.connect(self.show_about)
        
        # Style the menu bar
        menubar.setStyleSheet("""
            QMenuBar {
                background-color: rgba(0, 0, 0, 0.9);
                color: #ffffff;
                border-bottom: 1px solid rgba(255, 255, 255, 0.3);
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
                background-color: rgba(255, 255, 255, 0.2);
                border: 1px solid rgba(255, 255, 255, 0.4);
            }
            QMenu {
                background-color: rgba(0, 0, 0, 0.95);
                color: #ffffff;
                border: 1px solid rgba(255, 255, 255, 0.4);
                border-radius: 8px;
                font-family: 'Courier New', monospace;
                font-size: 11px;
            }
            QMenu::item {
                padding: 8px 20px;
                border-radius: 5px;
            }
            QMenu::item:selected {
                background-color: rgba(255, 255, 255, 0.3);
                border: 1px solid rgba(255, 255, 255, 0.6);
            }
        """)
        
    def show_about(self):
        """Tampilkan about dialog"""
        about_dialog = AboutDialog(self)
        about_dialog.exec_()
        
    def show_top_rank(self):
        """Tampilkan top rank defacers dialog"""
        top_rank_dialog = TopRankDialog(self)
        top_rank_dialog.exec_()
        
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
                self.results_table.item(row_position, col).setBackground(QColor(50, 50, 50))
        else:
            for col in range(5):
                self.results_table.item(row_position, col).setBackground(QColor(30, 30, 30))
                
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
        help_label.setStyleSheet("color: #ffffff; font-weight: bold;")
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
            glow_color = f"rgba(255, 255, 255, {glow_strength})"
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