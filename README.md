# 🎬 Chatbot Bioskop

Project chatbot pemesanan tiket bioskop menggunakan Python dan Streamlit dengan konsep Finite State Machine (FSM) dan Natural Language Processing sederhana menggunakan Regular Expression (re).

## 📁 Struktur Project

```
chatbot/
├── app.py           # Frontend Streamlit - antarmuka chatbot
├── FSM.py           # Finite State Machine - logika state dan transisi
├── engine.py        # NLP Engine - pemrosesan bahasa natural dengan regex
├── promt.md         # Dokumentasi requirements
├── README.md        # Dokumentasi project
└── requirements.txt # Dependencies Python
```

### Penjelasan Setiap File

#### 1. `app.py` - Frontend Streamlit
- **Fungsi**: Antarmuka pengguna berbasis web menggunakan Streamlit
- **Fitur**:
  - Tampilan chat modern dengan UI yang responsif
  - Menyimpan riwayat percakapan menggunakan `session_state`
  - Menampilkan state saat ini
  - Sidebar dengan informasi film, jam tayang, dan tips
  - Tombol reset untuk memulai percakapan baru
- **Komponen Utama**:
  - `initialize_session_state()`: Inisialisasi state Streamlit
  - `display_chat_history()`: Menampilkan riwayat percakapan
  - `handle_user_input()`: Memproses input user
  - Custom CSS untuk tampilan modern

#### 2. `FSM.py` - Finite State Machine
- **Fungsi**: Mengelola logika percakapan dan transisi state
- **State yang digunakan**:
  - `START`: State awal percakapan
  - `LIHAT_FILM`: Menampilkan daftar film
  - `PESAN_TIKET`: Memproses pemesanan tiket
  - `PILIH_KURSI`: Memilih kursi
  - `KONFIRMASI`: Konfirmasi pesanan
  - `BAYAR`: Proses pembayaran
  - `SELESAI`: Pesanan selesai
- **Komponen Utama**:
  - `ChatbotFSM`: Class utama FSM
  - `process_input()`: Memproses input berdasarkan state
  - Handler untuk setiap state (`_handle_start`, `_handle_pesan_tiket`, dll)
  - Validasi data pesanan
  - Manajemen kursi tersedia

#### 3. `engine.py` - NLP Engine
- **Fungsi**: Pemrosesan bahasa natural menggunakan regex
- **Class**: `NLPEngine`
- **Method Utama**:
  - `parse_single_segment(text)`: Parse satu segmen teks untuk ekstrak entitas
  - `parse_orders(text)`: Parse pesanan lengkap dari teks
  - `detect_intent(text)`: Mendeteksi intent dari teks user
  - `print_menu()`: Menampilkan menu yang tersedia
  - `validate_movie(movie_name)`: Validasi nama film
  - `validate_time(time_str)`: Validasi jam tayang

## 🔍 Penjelasan Regex yang Digunakan

### Pattern Regex di `engine.py`

#### 1. Deteksi Jumlah Tiket
```python
'ticket_count': r'(\d+)\s*(?:tiket|ticket)'
```
- **Penjelasan**: Mencari angka diikuti oleh kata "tiket" atau "ticket"
- **Contoh Match**:
  - "2 tiket" → 2
  - "3 ticket" → 3
  - "5tiket" → 5

#### 2. Deteksi Nama Film
```python
'movie_name': r'(?:film|movie|nonton|tayang)\s*([A-Za-z]+)'
```
- **Penjelasan**: Mencari kata kunci film/movie/nonton/tayang diikuti nama film
- **Contoh Match**:
  - "film Avenger" → Avenger
  - "nonton Batman" → Batman
- **Catatan**: Juga menggunakan pencarian langsung di daftar film

#### 3. Deteksi Jam Tayang
```python
'show_time': r'(?:jam|pukul|at)\s*(\d{1,2})(?::\d{2})?\s*(?:malam|siang|pagi|sore)?'
```
- **Penjelasan**: Mencari jam dengan format fleksibel
- **Contoh Match**:
  - "jam 7 malam" → 19:00
  - "pukul 13:00" → 13:00
  - "at 10" → 10:00
- **Konversi**: Otomatis mengkonversi ke format 24 jam

#### 4. Deteksi Intent

##### Intent Pesan Tiket
```python
'intent_order': r'(?:pesan|booking|beli|order)\s*(?:\d+\s*tiket)?'
```
- **Contoh**: "pesan tiket", "booking 2 tiket", "beli"

##### Intent Lihat Film
```python
'intent_view': r'(?:lihat|tampil|show|list)\s*(?:film|movie|jadwal)'
```
- **Contoh**: "lihat film", "tampilkan jadwal", "list movie"

##### Intent Bayar
```python
'intent_pay': r'(?:bayar|pay|pembayaran)'
```
- **Contoh**: "bayar", "pay", "pembayaran"

##### Intent Batal
```python
'intent_cancel': r'(?:batal|cancel|batalkan)'
```
- **Contoh**: "batal", "cancel", "batalkan"

##### Intent Pilih Kursi
```python
'intent_seat': r'(?:kursi|seat|pilih\s*kursi)'
```
- **Contoh**: "kursi", "seat", "pilih kursi"

## 💬 Contoh Alur Percakapan Chatbot

### Contoh 1: Pemesanan Tiket Lengkap

```
User: 👋 Selamat datang di Chatbot Bioskop!

Bot: 🎬 Menu Chatbot Bioskop

1. Lihat Film - Ketik "lihat film" atau "tampilkan jadwal"
2. Pesan Tiket - Ketik "pesan [jumlah] tiket [nama film] jam [waktu]"
   Contoh: "pesan 2 tiket Avenger jam 7 malam"
3. Pilih Kursi - Ketik "pilih kursi [nomor kursi]"
   Contoh: "pilih kursi A1, A2"
4. Bayar - Ketik "bayar" untuk konfirmasi pembayaran
5. Batal - Ketik "batal" untuk membatalkan pesanan

📽️ Film yang Tersedia:
- Avenger
- Batman
- Spiderman
- Joker

⏰ Jam Tayang:
- 10:00, 13:00, 16:00, 19:00, 22:00

User: pesan 2 tiket Avenger jam 7 malam

Bot: 🎫 Pemilihan Kursi

Jumlah tiket: 2
Film: Avenger
Jam: 19:00

Layout Kursi:
  A  [A1] [A2] [A3] [A4] [A5] [A6] [A7] [A8]
  B  [B1] [B2] [B3] [B4] [B5] [B6] [B7] [B8]
  C  [C1] [C2] [C3] [C4] [C5] [C6] [C7] [C8]
  D  [D1] [D2] [D3] [D4] [D5] [D6] [D7] [D8]
  E  [E1] [E2] [E3] [E4] [E5] [E6] [E7] [E8]
  F  [F1] [F2] [F3] [F4] [F5] [F6] [F7] [F8]

[Kursi] = Tersedia, [X] = Terpesan

Ketik kursi yang dipilih (contoh: 'pilih kursi A1, A2')

User: pilih kursi A1, A2

Bot: 📋 Konfirmasi Pesanan

Film: Avenger
Jam Tayang: 19:00
Jumlah Tiket: 2
Kursi: A1, A2
Total Harga: Rp 100,000

Apakah pesanan sudah benar? (ya/tidak)

User: ya

Bot: 💳 Pembayaran

Total yang harus dibayar: Rp 100,000

Silakan transfer ke:
• Bank BCA: 123-456-7890
• Atas nama: Bioskop XXI

Setelah transfer, ketik 'bayar' untuk konfirmasi.

User: bayar

Bot: 🎉 Pemesanan Berhasil!

Detail Tiket:
• Film: Avenger
• Jam Tayang: 19:00
• Kursi: A1, A2
• Jumlah: 2 tiket
• Total: Rp 100,000

Simpan bukti pembayaran Anda. Tiket akan dikirim ke email Anda.

Terima kasih dan selamat menonton! 🍿
```

### Contoh 2: Lihat Film

```
User: lihat film

Bot: 📽️ Daftar Film yang Tersedia:
  • Avenger
  • Batman
  • Spiderman
  • Joker

⏰ Jam tayang: 10:00, 13:00, 16:00, 19:00, 22:00

Ketik 'pesan [jumlah] tiket [nama film] jam [waktu]' untuk memesan tiket.
```

### Contoh 3: Pembatalan

```
User: batal

Bot: 🚫 Pesanan dibatalkan.

🎬 Menu Chatbot Bioskop
...
```

## 🚀 Cara Menjalankan Project

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Jalankan Aplikasi
```bash
streamlit run app.py
```

### 3. Buka Browser
Aplikasi akan otomatis terbuka di browser pada `http://localhost:8501`

## 📦 Dependencies

- `streamlit`: Framework untuk web app
- `python`: 3.7+

## 🎯 Fitur Chatbot

- **lihat_film**: Menampilkan daftar film yang tersedia
- **pesan_tiket**: Memulai proses pemesanan tiket
- **pilih_kursi**: Memilih kursi yang diinginkan
- **bayar**: Konfirmasi pembayaran
- **batal**: Membatalkan pesanan

## 🔧 Teknologi yang Digunakan

- **Python**: Bahasa pemrograman utama
- **Streamlit**: Framework untuk frontend web
- **Regex (re)**: Natural Language Processing sederhana
- **Finite State Machine**: Pattern untuk manajemen state

## 📝 Catatan

- Project menggunakan Python murni tanpa database
- Data pesanan disimpan sementara di memory
- Kursi yang dipesan akan dihapus dari daftar tersedia
- Validasi input untuk memastikan data yang dimasukkan benar

## 👨‍💻 Pengembang

Project ini dibuat sebagai contoh implementasi chatbot dengan FSM dan NLP sederhana menggunakan regex.
