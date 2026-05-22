import re
from enum import Enum
from typing import Dict, Optional, List
from engine import NLPEngine


class State(Enum):
    """Enum untuk mendefinisikan state chatbot"""
    START = "START"
    LIHAT_FILM = "LIHAT_FILM"
    PESAN_TIKET = "PESAN_TIKET"
    PILIH_KURSI = "PILIH_KURSI"
    KONFIRMASI = "KONFIRMASI"
    BAYAR = "BAYAR"
    SELESAI = "SELESAI"
    MENUNGGU_LANJUT = "MENUNGGU_LANJUT"


class ChatbotFSM:
    """
    Finite State Machine untuk chatbot pemesanan tiket bioskop.
    Mengelola transisi state dan logika percakapan.
    """
    
    def __init__(self):
        self.current_state = State.START
        self.nlp_engine = NLPEngine()
        
        # Data pesanan sementara
        self.order_data = {
            'ticket_count': None,
            'movie_name': None,
            'show_time': None,
            'seats': [],
            'total_price': 0
        }
        
        # Harga tiket
        self.ticket_price = 50000
        
        # Daftar kursi yang tersedia
        self.available_seats = self._generate_seats()
    
    def _generate_seats(self) -> List[str]:
        """Generate daftar kursi bioskop (A-F, 1-8)"""
        seats = []
        rows = ['A', 'B', 'C', 'D', 'E', 'F']
        for row in rows:
            for num in range(1, 9):
                seats.append(f"{row}{num}")
        return seats
    
    def reset_order(self):
        """Reset data pesanan ke awal"""
        self.order_data = {
            'ticket_count': None,
            'movie_name': None,
            'show_time': None,
            'seats': [],
            'total_price': 0
        }
        self.available_seats = self._generate_seats()
    
    def process_input(self, user_input: str) -> str:
        """
        Proses input user dan berikan respons berdasarkan state saat ini.
        
        Args:
            user_input: Input teks dari user
            
        Returns:
            Respons dari chatbot
        """
        # Deteksi intent dari input
        intent = self.nlp_engine.detect_intent(user_input)
        
        # Handle intent batal di semua state
        if intent == 'batal':
            return self._handle_cancel()
        
        # Proses berdasarkan state saat ini
        if self.current_state == State.START:
            return self._handle_start(user_input, intent)
        elif self.current_state == State.LIHAT_FILM:
            return self._handle_lihat_film(user_input, intent)
        elif self.current_state == State.PESAN_TIKET:
            return self._handle_pesan_tiket(user_input, intent)
        elif self.current_state == State.PILIH_KURSI:
            return self._handle_pilih_kursi(user_input, intent)
        elif self.current_state == State.KONFIRMASI:
            return self._handle_konfirmasi(user_input, intent)
        elif self.current_state == State.BAYAR:
            return self._handle_bayar(user_input, intent)
        elif self.current_state == State.SELESAI:
            return self._handle_selesai(user_input, intent)
        elif self.current_state == State.MENUNGGU_LANJUT:
            return self._handle_menunggu_lanjut(user_input, intent)
        
        return "Maaf, terjadi kesalahan. Silakan coba lagi."
    
    def _handle_start(self, user_input: str, intent: Optional[str]) -> str:
        """Handle state START"""
        if intent == 'lihat_film':
            self.current_state = State.LIHAT_FILM
            return self._show_movies()
        elif intent == 'pesan_tiket':
            self.current_state = State.PESAN_TIKET
            return self._handle_pesan_tiket(user_input, intent)
        else:
            return f"👋 Selamat datang di Chatbot Bioskop!\n\n{self.nlp_engine.print_menu()}\n\nSilakan pilih menu atau ketik perintah Anda."
    
    def _handle_lihat_film(self, user_input: str, intent: Optional[str]) -> str:
        """Handle state LIHAT_FILM"""
        if intent == 'pesan_tiket':
            self.current_state = State.PESAN_TIKET
            return self._handle_pesan_tiket(user_input, intent)
        else:
            return f"{self._show_movies()}\n\nKetik 'pesan [jumlah] tiket [nama film] jam [waktu]' untuk memesan tiket."
    
    def _handle_pesan_tiket(self, user_input: str, intent: Optional[str]) -> str:
        """Handle state PESAN_TIKET"""
        # Parse informasi pesanan
        order_info = self.nlp_engine.parse_orders(user_input)
        
        # Update data pesanan
        if 'ticket_count' in order_info:
            self.order_data['ticket_count'] = int(order_info['ticket_count'])
        if 'movie_name' in order_info:
            self.order_data['movie_name'] = order_info['movie_name']
        if 'show_time' in order_info:
            self.order_data['show_time'] = order_info['show_time']
        
        # Validasi data pesanan
        missing_info = []
        if not self.order_data['ticket_count']:
            missing_info.append("jumlah tiket")
        if not self.order_data['movie_name']:
            missing_info.append("nama film")
        if not self.order_data['show_time']:
            missing_info.append("jam tayang")
        
        if missing_info:
            return f"❌ Informasi belum lengkap. Mohon lengkapi: {', '.join(missing_info)}\n\nContoh: 'pesan 2 tiket Avenger jam 7 malam'"
        
        # Validasi film dan jam
        if not self.nlp_engine.validate_movie(self.order_data['movie_name']):
            return f"❌ Film '{self.order_data['movie_name']}' tidak tersedia.\n\nFilm yang tersedia: {', '.join(self.nlp_engine.movies)}"
        
        if not self.nlp_engine.validate_time(self.order_data['show_time']):
            return f"❌ Jam tayang '{self.order_data['show_time']}' tidak tersedia.\n\nJam yang tersedia: 10:00, 13:00, 16:00, 19:00, 22:00"
        
        # Data lengkap, lanjut ke pemilihan kursi
        self.current_state = State.PILIH_KURSI
        return self._show_seat_selection()
    
    def _handle_pilih_kursi(self, user_input: str, intent: Optional[str]) -> str:
        """Handle state PILIH_KURSI"""
        # Ekstrak nomor kursi dari input
        seat_pattern = r'([A-F][1-8](?:,\s*[A-F][1-8])*)'
        seat_match = re.search(seat_pattern, user_input, re.IGNORECASE)
        
        if seat_match:
            seats_input = seat_match.group(1)
            selected_seats = [s.strip().upper() for s in seats_input.split(',')]
            
            # Validasi jumlah kursi
            if len(selected_seats) != self.order_data['ticket_count']:
                return f"❌ Jumlah kursi yang dipilih ({len(selected_seats)}) tidak sesuai dengan jumlah tiket ({self.order_data['ticket_count']}).\n\n{self._show_seat_selection()}"
            
            # Validasi ketersediaan kursi
            invalid_seats = [s for s in selected_seats if s not in self.available_seats]
            if invalid_seats:
                return f"❌ Kursi {', '.join(invalid_seats)} tidak tersedia atau sudah dipesan.\n\n{self._show_seat_selection()}"
            
            # Simpan kursi yang dipilih
            self.order_data['seats'] = selected_seats
            
            # Hapus kursi dari daftar tersedia
            for seat in selected_seats:
                if seat in self.available_seats:
                    self.available_seats.remove(seat)
            
            # Hitung total harga
            self.order_data['total_price'] = self.order_data['ticket_count'] * self.ticket_price
            
            # Lanjut ke konfirmasi
            self.current_state = State.KONFIRMASI
            return self._show_confirmation()
        
        return f"❌ Format kursi tidak valid. Gunakan format: A1, A2, B1, dll.\n\n{self._show_seat_selection()}"
    
    def _handle_konfirmasi(self, user_input: str, intent: Optional[str]) -> str:
        """Handle state KONFIRMASI"""
        user_input_lower = user_input.lower()
        
        if 'ya' in user_input_lower or 'yes' in user_input_lower or 'ok' in user_input_lower:
            self.current_state = State.BAYAR
            return self._show_payment()
        elif 'tidak' in user_input_lower or 'no' in user_input_lower:
            # Kembalikan kursi ke daftar tersedia
            for seat in self.order_data['seats']:
                self.available_seats.append(seat)
            self.order_data['seats'] = []
            
            self.current_state = State.PILIH_KURSI
            return "🔄 Pesanan dibatalkan. Silakan pilih kursi lagi.\n\n" + self._show_seat_selection()
        else:
            return self._show_confirmation() + "\n\nKetik 'ya' untuk konfirmasi atau 'tidak' untuk membatalkan."
    
    def _handle_bayar(self, user_input: str, intent: Optional[str]) -> str:
        """Handle state BAYAR"""
        user_input_lower = user_input.lower()
        
        if 'bayar' in user_input_lower or 'transfer' in user_input_lower or 'lanjut' in user_input_lower:
            self.current_state = State.MENUNGGU_LANJUT
            return self._show_completion()
        else:
            return self._show_payment() + "\n\nKetik 'bayar' untuk melanjutkan pembayaran."
    
    def _handle_selesai(self, user_input: str, intent: Optional[str]) -> str:
        """Handle state SELESAI — dipanggil langsung setelah bayar confirmed"""
        self.current_state = State.MENUNGGU_LANJUT
        return self._show_completion()

    def _handle_menunggu_lanjut(self, user_input: str, intent: Optional[str]) -> str:
        """Handle state MENUNGGU_LANJUT — reset setelah user memberi input apapun"""
        # Reset pesanan untuk sesi baru
        self.reset_order()
        self.current_state = State.START
        return "✅ Terima kasih telah menggunakan layanan kami!\n\n" + self.nlp_engine.print_menu()
    
    def _handle_cancel(self) -> str:
        """Handle pembatalan pesanan"""
        # Kembalikan kursi ke daftar tersedia
        for seat in self.order_data['seats']:
            self.available_seats.append(seat)
        
        # Reset pesanan
        self.reset_order()
        self.current_state = State.START
        
        return "🚫 Pesanan dibatalkan.\n\n" + self.nlp_engine.print_menu()
    
    def _show_movies(self) -> str:
        """Tampilkan daftar film yang tersedia"""
        movies_list = "\n".join([f"  • {movie}" for movie in self.nlp_engine.movies])
        return f"📽️ **Daftar Film yang Tersedia:**\n{movies_list}\n\n⏰ Jam tayang: 10:00, 13:00, 16:00, 19:00, 22:00"
    
    def _show_seat_selection(self) -> str:
        """Tampilkan pilihan kursi"""
        # Format kursi dalam grid
        seat_grid = ""
        rows = ['A', 'B', 'C', 'D', 'E', 'F']
        for row in rows:
            row_seats = [f"{row}{num}" for num in range(1, 9)]
            available_row = [f"[{seat}]" if seat in self.available_seats else f"[X]" for seat in row_seats]
            seat_grid += f"  {row}  {' '.join(available_row)}\n"
        
        estimasi_total = self.order_data['ticket_count'] * self.ticket_price
        return f"🎫 **Pemilihan Kursi**\n\nFilm: {self.order_data['movie_name']}\nJam: {self.order_data['show_time']}\nJumlah tiket: {self.order_data['ticket_count']}\nHarga per tiket: Rp {self.ticket_price:,}\nEstimasi Total: Rp {estimasi_total:,}\n\nLayout Kursi:\n{seat_grid}\n[Kursi] = Tersedia, [X] = Terpesan\n\nKetik kursi yang dipilih (contoh: 'pilih kursi A1, A2')"
    
    def _show_confirmation(self) -> str:
        """Tampilkan konfirmasi pesanan"""
        return f"""📋 **Konfirmasi Pesanan**

Film: {self.order_data['movie_name']}
Jam Tayang: {self.order_data['show_time']}
Jumlah Tiket: {self.order_data['ticket_count']}
Kursi: {', '.join(self.order_data['seats'])}
Total Harga: Rp {self.order_data['total_price']:,}

Apakah pesanan sudah benar? (ya/tidak)"""
    
    def _show_payment(self) -> str:
        """Tampilkan instruksi pembayaran"""
        return f"""💳 **Pembayaran**

Total yang harus dibayar: Rp {self.order_data['total_price']:,}

Silakan transfer ke:
• Bank BCA: 123-456-7890
• Atas nama: Bioskop XXI

Setelah transfer, ketik 'bayar' untuk konfirmasi."""
    
    def _show_completion(self) -> str:
        """Tampilkan pesan selesai"""
        return f"""🎉 **Pemesanan Berhasil!**

Detail Tiket:
• Film: {self.order_data['movie_name']}
• Jam Tayang: {self.order_data['show_time']}
• Kursi: {', '.join(self.order_data['seats'])}
• Jumlah: {self.order_data['ticket_count']} tiket
• Total: Rp {self.order_data['total_price']:,}

Simpan bukti pembayaran Anda. Tiket akan dikirim ke email Anda.

Terima kasih dan selamat menonton! 🍿"""
    
    def get_current_state(self) -> State:
        """Mengembalikan state saat ini"""
        return self.current_state
    
    def get_order_data(self) -> Dict:
        """Mengembalikan data pesanan saat ini"""
        return self.order_data.copy()
