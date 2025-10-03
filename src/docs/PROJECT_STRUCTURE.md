# Zone-H Mass Mirror Tool - Project Structure

## 📁 Directory Structure

```
zone-h-mass-mirror/
│
├── src/                          # Source code utama
│   ├── __init__.py              # Package initializer
│   │
│   ├── ui/                      # User Interface components
│   │   ├── __init__.py         # UI package exports
│   │   ├── about_dialog.py     # About dialog component
│   │   └── top_rank_dialog.py  # Top Rank Defacers dialog
│   │
│   ├── utils/                   # Utility functions & helpers
│   │   ├── __init__.py         # Utils package exports
│   │   ├── mirror_thread.py    # Mirror thread implementation
│   │   ├── helpers.py          # Helper functions
│   │   └── top_rank_fetcher.py # Top rank data fetching
│   │
│   ├── config/                  # Configuration & settings
│   │   ├── __init__.py         # Config package exports
│   │   └── config.py           # Configuration constants
│   │
│   └── assets/                  # Assets (images, icons, etc.)
│       └── screenshot.png      # Application screenshot
│
├── main.py                      # Main application entry point
├── requirements.txt             # Python dependencies
├── setup.py                     # Setup/installation script
├── README.md                    # Project documentation
├── .gitignore                   # Git ignore rules
├── run.bat                      # Windows launcher
├── run.sh                       # Unix/Linux launcher
└── sample_urls.txt             # Sample URLs for testing
```

## 📋 File Descriptions

### 🏠 Root Files
- **`main.py`** - Entry point aplikasi utama, mengandung class `ZoneHApp`
- **`requirements.txt`** - Daftar dependencies Python yang dibutuhkan
- **`setup.py`** - Script untuk instalasi dan setup aplikasi
- **`README.md`** - Dokumentasi utama proyek
- **`.gitignore`** - Konfigurasi file yang diignore oleh Git
- **`run.bat`** - Script launcher untuk Windows
- **`run.sh`** - Script launcher untuk Unix/Linux
- **`sample_urls.txt`** - File contoh URLs untuk testing

### 📦 Source Code (`src/`)

#### UI Components (`src/ui/`)
- **`about_dialog.py`** - About dialog dengan tema hacker
  - Class `AboutDialog` untuk menampilkan informasi aplikasi
  - Tombol GitHub, Documentation, Contact
  - Styling konsisten dengan tema hacker

- **`top_rank_dialog.py`** - Top Rank Defacers dialog
  - Class `TopRankDialog` untuk menampilkan ranking defacers
  - Class `TopRankFetcher` untuk scraping data dari Zone-H
  - Tabel ranking dengan color coding untuk top 3
  - Fitur export data dan refresh
  - Styling hacker theme dengan warna putih

#### Utilities (`src/utils/`)
- **`mirror_thread.py`** - Thread implementation
  - Class `ZoneHMirror` untuk proses mass mirror
  - Signal handling untuk progress update
  - Error handling yang robust
  
- **`helpers.py`** - Helper functions
  - `validate_url()` - Validasi format URL
  - `sanitize_url()` - Sanitasi input URL
  - `extract_domain()` - Ekstrak domain dari URL
  - `save_results_to_json()` - Export ke JSON
  - `save_results_to_csv()` - Export ke CSV
  - `load_urls_from_file()` - Load URLs dari file
  - `calculate_success_rate()` - Hitung tingkat keberhasilan
  - `generate_report()` - Generate laporan lengkap

- **`top_rank_fetcher.py`** - Top rank data fetching
  - Class `TopRankFetcher` untuk scraping Zone-H
  - Method `extract_defacer_name()` - Ekstrak nama defacer
  - Method `detect_country()` - Deteksi negara defacer
  - Method `detect_specialty()` - Klasifikasi keahlian
  - Method `calculate_mirrors()` - Hitung jumlah mirror

#### Configuration (`src/config/`)
- **`config.py`** - Configuration constants
  - `DEFAULT_SETTINGS` - Pengaturan default aplikasi
  - `USER_AGENTS` - Daftar user agents
  - `ERROR_MESSAGES` - Pesan error
  - `SUCCESS_MESSAGES` - Pesan sukses
  - `WARNING_MESSAGES` - Pesan peringatan

#### Assets (`src/assets/`)
- **`screenshot.png`** - Screenshot aplikasi untuk dokumentasi

## 🔄 Import Structure

```python
# Main imports
from src.config import DEFAULT_SETTINGS, USER_AGENTS, ERROR_MESSAGES
from src.utils import (validate_url, sanitize_url, ZoneHMirror, 
                      save_results_to_json, save_results_to_csv)
from src.ui import AboutDialog, TopRankDialog
```

## 🎯 Best Practices

1. **Separation of Concerns**: Setiap module memiliki tanggung jawab yang jelas
2. **Reusability**: Komponen dapat digunakan kembali di project lain
3. **Maintainability**: Struktur yang terorganisir memudahkan maintenance
4. **Scalability**: Mudah untuk menambahkan fitur baru
5. **Consistency**: Konsisten dalam penamaan dan struktur

## 🚀 How to Add New Features

1. **UI Components**: Tambahkan di `src/ui/`
2. **Business Logic**: Tambahkan di `src/utils/`
3. **Configuration**: Update di `src/config/`
4. **Main Integration**: Update `main.py` untuk integrasi

## 📊 Package Dependencies

```
src/
├── ui/          # PyQt5 GUI components
├── utils/       # Core logic & helpers
├── config/      # Configuration constants
└── assets/      # Static resources
```

Struktur ini membuat kode lebih terorganisir, mudah dimaintain, dan scalable untuk pengembangan lebih lanjut.