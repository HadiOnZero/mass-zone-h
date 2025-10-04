# 📱 Zone-H Mobile Mirror Tool

Aplikasi mobile untuk melakukan mass mirror terhadap notifikasi Zone-H dengan desain hacker dan interface yang dioptimalkan untuk perangkat mobile.

## 🌟 Fitur Utama Mobile

- **📱 Mobile-Optimized**: Interface yang dioptimalkan untuk layar sentuh
- **🚀 Touch-Friendly**: Tombol dan kontrol yang mudah digunakan di mobile
- **📊 Real-time Progress**: Monitor progress mirror secara real-time
- **🔋 Battery-Aware**: Operasi yang hemat baterai
- **🌐 Network Monitoring**: Pemantauan status jaringan
- **💾 Mobile Export**: Export hasil ke penyimpanan perangkat
- **📲 Responsive Design**: Tampilan yang adaptif untuk berbagai ukuran layar
- **🎨 Hacker Theme**: Desain hacker dengan tema hitam dan hijau neon

## 📁 Struktur Project Mobile

```
mobile/
│
├── src/                          # Source code utama mobile
│   ├── config/                   # Konfigurasi mobile
│   │   ├── __init__.py
│   │   └── mobile_config.py      # Pengaturan dan konfigurasi mobile
│   ├── utils/                    # Utility functions mobile
│   │   ├── __init__.py
│   │   ├── mobile_helpers.py     # Helper functions untuk mobile
│   │   └── mobile_mirror_thread.py # Thread untuk proses mirror mobile
│   ├── ui/                       # UI components mobile
│   │   ├── __init__.py
│   │   ├── mobile_dialogs.py     # Dialog-dialog mobile
│   │   └── mobile_widgets.py     # Widget-widget kustom mobile
│   └── assets/                   # Assets untuk mobile
│
├── main_mobile.py                # Main application entry point
├── run_mobile.py                 # Mobile launcher script
├── requirements_mobile.txt       # Dependencies untuk mobile
└── README_MOBILE.md             # Dokumentasi mobile
```

## 🔧 Persyaratan Sistem Mobile

### Minimum Requirements:
- **Python**: 3.7 atau lebih baru
- **Operating System**: Android 5.0+ / iOS 11.0+ / Windows / Linux / Mac
- **RAM**: 2GB atau lebih
- **Storage**: 100MB free space

### Dependencies:
- **Kivy**: 2.2.1 - Framework UI mobile
- **KivyMD**: 1.1.1 - Material Design components
- **requests**: 2.31.0 - HTTP library
- **beautifulsoup4**: 4.12.2 - HTML parsing
- **lxml**: 4.9.3 - XML/HTML parser
- **Pillow**: 10.0.1 - Image processing

## 🚀 Instalasi Mobile

### 1. Install Python
Pastikan Python 3.7+ terinstall di perangkat Anda.

### 2. Install Dependencies
```bash
cd mobile/
pip install -r requirements_mobile.txt
```

### 3. Jalankan Aplikasi
```bash
# Metode 1: Direct
python main_mobile.py

# Metode 2: Launcher
python run_mobile.py
```

## 📱 Cara Penggunaan Mobile

### 1. **Buka Aplikasi**
Jalankan file `main_mobile.py` atau `run_mobile.py`

### 2. **Masukkan URLs**
- Tap pada area input URLs
- Masukkan URLs target (satu per baris)
- Contoh:
```
http://site1.com
https://site2.com
http://192.168.1.100
```

### 3. **Atur Pengaturan**
- **Delay**: Waktu tunggu antar request (2-5 detik direkomendasikan)
- **Timeout**: Batas waktu request (15-30 detik untuk mobile)

### 4. **Start Mirror**
- Tap tombol "🚀 START MIRROR"
- Monitor progress di progress bar
- Lihat log di console area

### 5. **Lihat Hasil**
- Hasil mirror akan muncul di daftar bawah
- Tap pada hasil untuk melihat detail
- Gunakan tombol "💾 EXPORT" untuk menyimpan hasil

### 6. **Export Hasil**
- Tap tombol "💾 EXPORT" setelah selesai
- Pilih format: JSON atau CSV
- Hasil akan disimpan di penyimpanan perangkat

## 🎨 Fitur Interface Mobile

### **Header Section**
- 📱 Logo dan judul aplikasi
- 🔥 Efek glow hijau hacker
- 📋 Informasi versi

### **URL Input Section**
- 📝 Text input dengan tema hacker
- 💡 Hint text untuk panduan
- 🛡️ Validasi URL otomatis

### **Settings Section**
- ⚙️ Delay configuration
- ⏱️ Timeout settings
- 🎨 Mobile-optimized controls

### **Control Section**
- 🚀 Start mirror button dengan efek glow
- ⏹️ Stop button untuk menghentikan proses
- 🗑️ Clear button untuk membersihkan data

### **Progress Section**
- 📊 Progress bar dengan tema hacker
- 📈 Real-time statistics (Total, Success, Failed)
- 🔄 Status updates

### **Results Section**
- 📋 Scrollable list of results
- ✅❌ Color-coded status indicators
- 📝 Detail information for each result
- 👆 Tap to view detailed result

### **Log Section**
- 📱 Console log dengan font monospace
- 🟢 Hijau untuk nuansa terminal hacker
- 📜 Auto-scroll ke pesan terbaru

### **Toolbar**
- 🌐 Network status indicator
- ❓ Help button
- ℹ️ About button

## 🌟 Fitur Khusus Mobile

### **📱 Touch-Optimized Interface**
- Tombol besar untuk mudah di-tap
- Scroll yang smooth
- Keyboard-friendly input

### **🔋 Battery-Aware Operation**
- Optimasi penggunaan CPU
- Delay yang disesuaikan untuk mobile
- Pemberitahuan saat baterai rendah

### **🌐 Network Monitoring**
- Status koneksi real-time
- Peringatan saat offline
- Adaptasi untuk jaringan mobile

### **💾 Mobile Export**
- Export ke penyimpanan internal
- Format JSON dan CSV
- Nama file otomatis dengan timestamp

### **📲 Responsive Design**
- Adaptasi untuk berbagai ukuran layar
- Portrait mode optimization
- Scalable UI elements

### **🎨 Hacker Theme Mobile**
- Background hitam dengan aksen hijau
- Font monospace untuk nuansa terminal
- Efek glow pada elemen aktif
- Border hijau pada komponen

## ⚙️ Pengaturan Mobile

### **Network Settings**
- Timeout yang lebih lama untuk mobile (15-30 detik)
- Retry attempts yang disesuaikan
- Mobile-optimized user agents

### **Performance Settings**
- Max threads yang lebih rendah (3 threads)
- Delay antar request yang optimal (2-5 detik)
- Memory usage yang efisien

### **UI Settings**
- Font size yang readable di mobile
- Touch target yang cukup besar (min 40px)
- Contrast ratio yang baik

## 🛡️ Keamanan Mobile

### **URL Validation**
- Validasi format URL sebelum mirror
- Sanitasi input untuk mencegah injection
- Filter karakter berbahaya

### **Network Security**
- SSL certificate verification
- Timeout untuk mencegah hanging
- User agent rotation untuk mobile

### **Data Protection**
- Tidak menyimpan data sensitif
- Export yang aman ke penyimpanan
- Permission yang minimal

## 🔧 Troubleshooting Mobile

### **Aplikasi tidak bisa dibuka**
```bash
# Pastikan semua dependencies terinstall
pip install -r requirements_mobile.txt

# Check Python version
python --version  # Harus 3.7+
```

### **Kivy error saat startup**
```bash
# Install dependencies Kivy
pip install kivy[base] kivymd

# Untuk Windows, install SDL2
pip install kivy.deps.sdl2 kivy.deps.glew
```

### **Mirror gagal terus**
- ✅ Cek status network di toolbar
- ✅ Pastikan URLs valid
- ✅ Gunakan delay yang cukup (2-5 detik)
- ✅ Cek koneksi internet
- ✅ Periksa firewall/antivirus

### **Aplikasi freeze atau crash**
- 🔋 Pastikan baterai cukup
- 📱 Tutup aplikasi lain yang tidak digunakan
- 🔄 Restart aplikasi
- 📊 Monitor memory usage

### **Export tidak berfungsi**
- ✅ Pastikan hasil mirror ada
- ✅ Cek permission penyimpanan
- ✅ Pastikan storage tidak penuh
- ✅ Gunakan nama file yang valid

## 📊 Performance Tips

### **Untuk Hasil Optimal:**
1. **Gunakan WiFi** untuk koneksi yang stabil
2. **Tutup aplikasi lain** untuk menghemat memory
3. **Charge perangkat** saat mirror berlangsung
4. **Gunakan delay 2-3 detik** untuk hasil terbaik
5. **Limit URLs** (max 50 URLs per session di mobile)

### **Hemat Baterai:**
- Gunakan delay yang lebih lama
- Kurangi jumlah URLs
- Turunkan brightness screen
- Matikan fitur yang tidak perlu

## 🔄 Update & Maintenance

### **Check for Updates:**
```bash
cd mobile/
pip install --upgrade -r requirements_mobile.txt
```

### **Clear Cache:**
```bash
# Hapus file hasil export lama
rm mobile_mirror_results_*.json
rm mobile_mirror_results_*.csv
```

### **Backup Data:**
Export hasil mirror secara berkala untuk backup.

## ⚖️ Lisensi & Disclaimer

### **Lisensi:**
MIT License - Bebas digunakan dan dimodifikasi.

### **Disclaimer:**
⚠️ **Peringatan**: Aplikasi ini dibuat untuk keperluan edukasi dan testing keamanan. Pengguna bertanggung jawab atas penggunaannya. Gunakan dengan bijak dan sesuai dengan hukum yang berlaku.

### **Author:**
📧 **Hadi Ramdhani** - Elite Hacker Tools  
© 2024 - Zone-H Mobile Mirror Tool

---

**💡 Tips**: Untuk performa terbaik, gunakan perangkat dengan RAM minimal 2GB dan pastikan koneksi internet stabil. Selalu backup data penting sebelum melakukan testing.

**🆘 Butuh Bantuan?** 
- Cek bagian Troubleshooting di atas
- Pastikan semua dependencies terinstall dengan benar
- Hubungi developer untuk support lebih lanjut