# Zone-H Mass Mirror Tool

![Zone-H Mass Mirror Tool Screenshot](src/assets/screenshot.png)

Aplikasi desktop elegan untuk melakukan mass mirror terhadap notifikasi Zone-H dengan desain hacker ala-ala (hitam & biru).
=======
Aplikasi desktop untuk melakukan mass mirror terhadap notifikasi Zone-H dengan desain hacker.
>>>>>>> b8d624e681cde9a4b4a3616b5f6da035de9cb788

## Fitur Utama

- 🎯 **Mass Mirror**: Mirror multiple URLs secara bersamaan
- 🎨 **Desain Hacker**: Interface elegan dengan tema hitam dan hijau neon
- 📊 **Real-time Progress**: Monitor progress mirror secara real-time
- 📈 **Statistik**: Lihat hasil mirror dengan detail statistik
- ⚙️ **Customizable Settings**: Atur delay, timeout, dan user agent
- 🛡️ **Error Handling**: Penanganan error yang robust
- 📝 **Logging**: Console log untuk debugging
- 🔄 **Thread-safe**: Proses mirror berjalan di background thread
- 🏆 **Top Rank Defacers**: Lihat ranking defacers teratas dari Zone-H

## 📁 Project Structure

```
zone-h-mass-mirror/
│
├── src/                          # Source code utama
│   ├── ui/                       # User Interface components
│   │   ├── about_dialog.py       # About dialog dengan tema hacker
│   │   └── top_rank_dialog.py    # Top Rank Defacers dialog
│   ├── utils/                    # Utility functions & helpers
│   │   ├── mirror_thread.py      # Mirror thread implementation
│   │   ├── helpers.py            # Helper functions (validasi, export, dll)
│   │   └── top_rank_fetcher.py   # Top rank data fetching
│   ├── config/                   # Configuration & settings
│   │   └── config.py             # Configuration constants
│   └── assets/                   # Assets (images, icons, etc.)
│       └── screenshot.png        # Application screenshot
│
├── main.py                       # Main application entry point
├── requirements.txt              # Python dependencies
├── setup.py                      # Setup/installation script
├── README.md                     # Project documentation
├── .gitignore                    # Git ignore rules
├── run.bat                       # Windows launcher
├── run.sh                        # Unix/Linux launcher
└── sample_urls.txt              # Sample URLs for testing
```

## Persyaratan Sistem

- Python 3.6 atau lebih baru
- PyQt5
- requests
- beautifulsoup4
- lxml

## Instalasi

1. Clone repository ini atau download file-filenya
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Cara Penggunaan

### Metode 1: Command Line
```bash
python main.py
```

### Metode 2: Launcher Script
```bash
# Linux/Mac
./run.sh

# Windows
run.bat
```

## Cara Menggunakan Aplikasi

1. **Buka Aplikasi**: Jalankan file `main.py`
2. **Masukkan URLs**: Masukkan URLs target di area input (satu URL per baris)
3. **Atur Settings** (Opsional):
   - **Delay**: Waktu tunggu antar request (1-10 detik)
   - **Timeout**: Batas waktu request (5-60 detik)
   - **User Agent**: Pilih user agent yang digunakan
4. **Start Mirror**: Klik tombol "START MIRROR" untuk memulai
5. **Monitor Progress**: Lihat progress di progress bar dan console log
6. **Lihat Hasil**: Hasil mirror akan muncul di tabel kanan
7. **Statistik**: Lihat ringkasan hasil di bagian bawah tabel

## Contoh URLs

```
http://example-site1.com
https://example-site2.com
http://192.168.1.100
https://vulnerable-site.com/admin
```

## Tampilan Aplikasi

Aplikasi ini memiliki desain hacker dengan tema:
- **Background**: Hitam pekat
- **Text**: Putih cerah (mirip terminal hacker modern)
- **Accent**: Putih terang untuk elemen aktif
- **Font**: Monospace untuk nuansa terminal
- **Border**: Garis putih untuk elemen-elemen UI

## About App

Aplikasi ini dilengkapi dengan halaman **About** yang komprehensif yang dapat diakses melalui:

### Cara Akses About:
1. **Menu Bar**: Klik `Help` → `About`
2. **Tombol About**: Klik tombol `ABOUT` di UI utama
3. **Status Bar**: Klik label `🛡️ About` di status bar

### Fitur About Page:
- 📋 **Informasi Aplikasi**: Nama, versi, author, dan deskripsi lengkap
- ✨ **Daftar Fitur**: Semua fitur utama aplikasi dengan ikon
- 🔧 **Technical Details**: Teknologi yang digunakan (Python, PyQt5, dll)
- ⚠️ **Disclaimer**: Peringatan penggunaan yang bertanggung jawab
- 🐙 **Tombol GitHub**: Akses ke repository (coming soon)
- 📚 **Tombol Documentation**: Panduan penggunaan lengkap
- 📧 **Tombol Contact**: Informasi kontak dan support
- ✖ **Tombol Close**: Menutup dialog

### Desain About:
Halaman About mengikuti tema hacker yang konsisten dengan:
- Background hitam dengan border putih
- Teks putih dengan font monospace
- Tombol-tombol dengan efek glow
- Layout yang rapi dan profesional
- Informasi yang terstruktur dan mudah dibaca

### Informasi yang Ditampilkan:
- **Version**: 1.0.0
- **Author**: Hadi Ramdhani
- **License**: MIT License
- **Description**: Penjelasan lengkap tentang aplikasi
- **Features**: 8 fitur utama dengan ikon emoji
- **Technical Details**: Teknologi dan library yang digunakan
- **Disclaimer**: Peringatan penggunaan yang bertanggung jawab
- **Copyright**: © 2024 Hadi Ramdhani - Elite Hacker Tools

## Top Rank Defacers

Aplikasi ini dilengkapi dengan fitur **Top Rank Defacers** yang menampilkan ranking defacers teratas dari Zone-H archive.

### Cara Akses Top Rank:
1. **Menu Bar**: Klik `Tools` → `Top Rank Defacers`
2. **Tombol TOP RANK**: Klik tombol `TOP RANK` di UI utama

### Fitur Top Rank Dialog:
- 🏆 **Real-time Scraping**: Mengambil data ranking langsung dari Zone-H
- 📊 **Tabel Ranking**: Menampilkan rank, nama defacer, negara, jumlah mirror, dan status
- 🎨 **Color Coding**:
  - 🥇 **Rank 1**: Warna gold (emas)
  - 🥈 **Rank 2**: Warna silver (perak)
  - 🥉 **Rank 3**: Warna bronze (perunggu)
- 🌍 **Country Detection**: Menampilkan negara asal defacer
- 🎯 **Specialty Classification**: Mengkategorikan keahlian defacer
- 💾 **Export Data**: Menyimpan data ranking ke file
- 🔄 **Refresh Button**: Memperbarui data terbaru

### Desain Top Rank:
Dialog Top Rank mengikuti tema hacker yang konsisten dengan:
- Background hitam dengan border putih
- Teks putih dengan font monospace
- Tombol-tombol dengan efek glow putih
- Tabel dengan styling khusus untuk top 3 ranks
- Header yang mencolok dengan gradasi warna

### Data yang Ditampilkan:
- **Rank**: Peringkat defacer (1-50)
- **Defacer Name**: Nama alias defacer
- **Country**: Negara asal dengan icon bendera
- **Mirror Count**: Jumlah mirror yang berhasil
- **Specialty**: Kategori keahlian (SQLi, XSS, LFI, RFI, dll)
- **Status**: Status aktifitas defacer (Active/Inactive)

## Fitur Keamanan

- Validasi URL otomatis
- Penanganan timeout untuk mencegah hanging
- Thread-safe operation
- User agent rotation
- Error handling comprehensive

## Troubleshooting

### Aplikasi tidak bisa dibuka
- Pastikan Python 3 terinstall
- Install semua dependencies dengan `pip install -r requirements.txt`

### Mirror gagal terus
- Cek koneksi internet
- Periksa apakah URLs valid
- Coba tambahkan delay antar request
- Cek firewall/antivirus

### Aplikasi freeze
- Proses mirror berjalan di background thread
- Jangan tutup aplikasi saat mirror berlangsung
- Gunakan tombol STOP untuk menghentikan proses

## Update & Maintenance

Aplikasi ini dikembangkan untuk keperluan edukasi dan testing. Gunakan dengan bijak dan sesuai dengan hukum yang berlaku.

## Lisensi

MIT License - Bebas digunakan dan dimodifikasi.

## Author

Hadi Ramdhani - Elite Hacker Tools

---
**⚠️ Disclaimer**: Aplikasi ini dibuat untuk keperluan edukasi dan testing keamanan. Pengguna bertanggung jawab atas penggunaannya.
