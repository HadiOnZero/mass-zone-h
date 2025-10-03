#!/usr/bin/env python3
"""
About Dialog untuk Zone-H Mass Mirror Tool
UI component untuk menampilkan informasi aplikasi
Author: Hadi Ramdhani
"""

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QTextBrowser, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


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
                color: #ffffff;
                padding: 20px;
                margin: 10px;
                border: 2px solid rgba(255, 255, 255, 0.6);
                border-radius: 15px;
                background-color: rgba(255, 255, 255, 0.1);
                text-shadow: 0 0 10px rgba(255, 255, 255, 0.8);
                letter-spacing: 3px;
            }
        """)
        layout.addWidget(header_label)
        
        # Informasi aplikasi
        info_text = f"""
        <div style='color: #ffffff; font-family: "Courier New", monospace;'>
        <h3 style='color: #ffffff; text-align: center;'>🛡️ Zone-H Mass Mirror Tool 🛡️</h3>
        
        <p><strong>Version:</strong> 1.0.0</p>
        <p><strong>Author:</strong> Hadi Ramdhani</p>
        <p><strong>License:</strong> MIT License</p>
        
        <h4 style='color: #ffffff;'>📋 Description:</h4>
        <p>Aplikasi desktop elegan untuk melakukan mass mirror terhadap notifikasi Zone-H
        dengan desain hacker ala-ala (hitam & putih).</p>
        
        <h4 style='color: #ffffff;'>✨ Features:</h4>
        <ul>
            <li>🎯 Mass Mirror multiple URLs secara bersamaan</li>
            <li>🎨 Desain Hacker dengan tema hitam dan putih</li>
            <li>📊 Real-time Progress monitoring</li>
            <li>📈 Statistik hasil mirror yang detail</li>
            <li>⚙️ Customizable Settings (delay, timeout, user agent)</li>
            <li>🛡️ Robust Error Handling</li>
            <li>📝 Console log untuk debugging</li>
            <li>🔄 Thread-safe operation</li>
        </ul>
        
        <h4 style='color: #ffffff;'>🔧 Technical Details:</h4>
        <ul>
            <li>Built with Python 3.6+</li>
            <li>GUI Framework: PyQt5</li>
            <li>HTTP Library: requests</li>
            <li>HTML Parser: BeautifulSoup4</li>
            <li>Multi-threading support</li>
        </ul>
        
        <h4 style='color: #ffffff;'>⚠️ Disclaimer:</h4>
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
                color: #ffffff;
                border: 1px solid rgba(255, 255, 255, 0.4);
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
                background-color: rgba(255, 255, 255, 0.2);
                color: #ffffff;
                font-weight: bold;
                padding: 8px 15px;
                border: 1px solid rgba(255, 255, 255, 0.5);
                border-radius: 15px;
                text-shadow: 0 0 5px rgba(255, 255, 255, 0.8);
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
        button_layout.addWidget(github_button)
        
        # Documentation button
        docs_button = QPushButton("📚 Documentation")
        docs_button.clicked.connect(self.open_documentation)
        docs_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 0.2);
                color: #ffffff;
                font-weight: bold;
                padding: 8px 15px;
                border: 1px solid rgba(255, 255, 255, 0.5);
                border-radius: 15px;
                text-shadow: 0 0 5px rgba(255, 255, 255, 0.8);
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
        button_layout.addWidget(docs_button)
        
        # Contact button
        contact_button = QPushButton("📧 Contact")
        contact_button.clicked.connect(self.open_contact)
        contact_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 0.2);
                color: #ffffff;
                font-weight: bold;
                padding: 8px 15px;
                border: 1px solid rgba(255, 255, 255, 0.5);
                border-radius: 15px;
                text-shadow: 0 0 5px rgba(255, 255, 255, 0.8);
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
        button_layout.addWidget(contact_button)
        
        button_layout.addStretch()
        
        # Close button
        close_button = QPushButton("✖ Close")
        close_button.clicked.connect(self.accept)
        close_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 0.2);
                color: #ffffff;
                font-weight: bold;
                padding: 8px 20px;
                border: 1px solid rgba(255, 255, 255, 0.5);
                border-radius: 15px;
                text-shadow: 0 0 5px rgba(255, 255, 255, 0.8);
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
                color: #ffffff;
                border: 2px solid rgba(255, 255, 255, 0.6);
                border-radius: 20px;
            }
        """)