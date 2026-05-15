import re
from typing import Dict, Optional, List


class NLPEngine:
    """
    Natural Language Processing Engine untuk chatbot bioskop.
    Menggunakan regex untuk mendeteksi intent dan mengekstrak entitas.
    """
    
    def __init__(self):
        # Daftar film yang tersedia
        self.movies = ["Avenger", "Batman", "Spiderman", "Joker"]
        
        # Pattern regex untuk mendeteksi berbagai entitas
        self.patterns = {
            # Deteksi jumlah tiket (angka)
            'ticket_count': r'(\d+)\s*(?:tiket|ticket)',
            
            # Deteksi nama film
            'movie_name': r'(?:film|movie|nonton|tayang)\s*([A-Za-z]+)',
            
            # Deteksi jam tayang (format: 7 malam, 19:00, jam 7, dll)
            'show_time': r'(?:jam|pukul|at)\s*(\d{1,2})(?::\d{2})?\s*(?:malam|siang|pagi|sore)?',
            
            # Deteksi intent pesan tiket
            'intent_order': r'(?:pesan|booking|beli|order)\s*(?:\d+\s*tiket)?',
            
            # Deteksi intent lihat film
            'intent_view': r'(?:lihat|tampil|show|list)\s*(?:film|movie|jadwal)',
            
            # Deteksi intent bayar
            'intent_pay': r'(?:bayar|pay|pembayaran)',
            
            # Deteksi intent batal
            'intent_cancel': r'(?:batal|cancel|batalkan)',
            
            # Deteksi intent pilih kursi
            'intent_seat': r'(?:kursi|seat|pilih\s*kursi)',
        }
    
    def parse_single_segment(self, text: str) -> Dict[str, str]:
        """
        Parse satu segmen teks untuk mengekstrak entitas.
        
        Args:
            text: Teks input dari user
            
        Returns:
            Dictionary berisi entitas yang terdeteksi
        """
        entities = {}
        
        # Deteksi jumlah tiket
        ticket_match = re.search(self.patterns['ticket_count'], text, re.IGNORECASE)
        if ticket_match:
            entities['ticket_count'] = ticket_match.group(1)
        
        # Deteksi nama film
        for movie in self.movies:
            if movie.lower() in text.lower():
                entities['movie_name'] = movie
                break
        
        # Deteksi jam tayang
        time_match = re.search(self.patterns['show_time'], text, re.IGNORECASE)
        if time_match:
            hour = int(time_match.group(1))
            # Konversi ke format 24 jam
            if hour < 12 and 'malam' in text.lower():
                hour += 12
            entities['show_time'] = f"{hour:02d}:00"
        
        return entities
    
    def parse_orders(self, text: str) -> Dict[str, str]:
        """
        Parse pesanan lengkap dari teks user.
        
        Args:
            text: Teks input dari user
            
        Returns:
            Dictionary berisi semua informasi pesanan
        """
        order_info = self.parse_single_segment(text)
        
        # Tambahkan intent detection
        intent = self.detect_intent(text)
        if intent:
            order_info['intent'] = intent
        
        return order_info
    
    def detect_intent(self, text: str) -> Optional[str]:
        """
        Mendeteksi intent dari teks user.
        
        Args:
            text: Teks input dari user
            
        Returns:
            Intent yang terdeteksi atau None
        """
        text_lower = text.lower()
        
        # Cek setiap intent pattern
        if re.search(self.patterns['intent_order'], text_lower):
            return 'pesan_tiket'
        elif re.search(self.patterns['intent_view'], text_lower):
            return 'lihat_film'
        elif re.search(self.patterns['intent_pay'], text_lower):
            return 'bayar'
        elif re.search(self.patterns['intent_cancel'], text_lower):
            return 'batal'
        elif re.search(self.patterns['intent_seat'], text_lower):
            return 'pilih_kursi'
        
        # Cek jika user menyebutkan film tanpa kata khusus
        for movie in self.movies:
            if movie.lower() in text_lower:
                return 'pesan_tiket'
        
        return None
    
    def print_menu(self) -> str:
        """
        Menampilkan menu yang tersedia.
        
        Returns:
            String berisi menu yang diformat
        """
        menu = """
🎬 **Menu Chatbot Bioskop**

1. **Lihat Film** - Ketik "lihat film" atau "tampilkan jadwal"
2. **Pesan Tiket** - Ketik "pesan [jumlah] tiket [nama film] jam [waktu]"
   Contoh: "pesan 2 tiket Avenger jam 7 malam"
3. **Pilih Kursi** - Ketik "pilih kursi [nomor kursi]"
   Contoh: "pilih kursi A1, A2"
4. **Bayar** - Ketik "bayar" untuk konfirmasi pembayaran
5. **Batal** - Ketik "batal" untuk membatalkan pesanan

📽️ **Film yang Tersedia:**
- Avenger
- Batman
- Spiderman
- Joker

⏰ **Jam Tayang:**
- 10:00, 13:00, 16:00, 19:00, 22:00
        """
        return menu
    
    def validate_movie(self, movie_name: str) -> bool:
        """
        Validasi nama film.
        
        Args:
            movie_name: Nama film yang akan divalidasi
            
        Returns:
            True jika film valid, False jika tidak
        """
        return movie_name in self.movies
    
    def validate_time(self, time_str: str) -> bool:
        """
        Validasi jam tayang.
        
        Args:
            time_str: Jam tayang yang akan divalidasi
            
        Returns:
            True jika jam valid, False jika tidak
        """
        valid_times = ["10:00", "13:00", "16:00", "19:00", "22:00"]
        return time_str in valid_times
