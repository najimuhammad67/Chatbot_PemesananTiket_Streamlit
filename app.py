import streamlit as st
from FSM import ChatbotFSM, State
from engine import NLPEngine


# Konfigurasi halaman Streamlit
st.set_page_config(
    page_title="Chatbot Bioskop",
    page_icon="🎬",
    layout="centered",
    initial_sidebar_state="collapsed"
)


# Custom CSS untuk tampilan modern
st.markdown("""
<style>
    .stApp {
        background-color: #0E1117;
    }
    
    .chat-container {
        background-color: #1E2127;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        max-height: 500px;
        overflow-y: auto;
    }
    
    .user-message {
        background-color: #4CAF50;
        color: white;
        padding: 10px 15px;
        border-radius: 20px 20px 5px 20px;
        margin-bottom: 10px;
        max-width: 80%;
        margin-left: auto;
        text-align: right;
    }
    
    .bot-message {
        background-color: #2196F3;
        color: white;
        padding: 10px 15px;
        border-radius: 20px 20px 20px 5px;
        margin-bottom: 10px;
        max-width: 80%;
    }
    
    .header {
        text-align: center;
        padding: 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        margin-bottom: 20px;
        color: white;
    }
    
    .input-container {
        background-color: #1E2127;
        padding: 20px;
        border-radius: 10px;
        margin-top: 20px;
    }
    
    .state-badge {
        background-color: #FF9800;
        color: white;
        padding: 5px 10px;
        border-radius: 15px;
        font-size: 12px;
        display: inline-block;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Inisialisasi session_state Streamlit"""
    if 'chatbot' not in st.session_state:
        st.session_state.chatbot = ChatbotFSM()
    
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    if 'current_state' not in st.session_state:
        st.session_state.current_state = State.START
    
    if 'input_counter' not in st.session_state:
        st.session_state.input_counter = 0


def display_header():
    """Tampilkan header aplikasi"""
    st.markdown("""
    <div class="header">
        <h1>🎬 Chatbot Bioskop</h1>
        <p>Sistem pemesanan tiket bioskop dengan NLP sederhana</p>
    </div>
    """, unsafe_allow_html=True)


def display_chat_history():
    """Tampilkan riwayat percakapan"""
    if not st.session_state.messages:
        # Pesan awal dari bot
        initial_message = st.session_state.chatbot.process_input("")
        st.session_state.messages.append({
            "role": "assistant",
            "content": initial_message
        })
    
    chat_container = st.container()
    with chat_container:
        st.markdown('<div class="chat-container" id="chat-box">', unsafe_allow_html=True)
        
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.markdown(f'<div class="user-message">{message["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="bot-message">{message["content"]}</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Auto-scroll ke pesan terbaru
    st.markdown("""
    <script>
        const chatBox = document.getElementById('chat-box');
        if (chatBox) { chatBox.scrollTop = chatBox.scrollHeight; }
    </script>
    """, unsafe_allow_html=True)


def display_current_state():
    """Tampilkan state saat ini"""
    current_state = st.session_state.chatbot.get_current_state()
    st.markdown(f'<div class="state-badge">State: {current_state.value}</div>', unsafe_allow_html=True)


def handle_user_input(user_input: str):
    """Proses input user"""
    if not user_input.strip():
        return
    
    # Tambahkan pesan user ke riwayat
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })
    
    # Proses input dengan chatbot
    bot_response = st.session_state.chatbot.process_input(user_input)
    
    # Tambahkan respons bot ke riwayat
    st.session_state.messages.append({
        "role": "assistant",
        "content": bot_response
    })
    
    # Update state saat ini
    st.session_state.current_state = st.session_state.chatbot.get_current_state()


def display_input_area():
    """Tampilkan area input user"""
    st.markdown('<div class="input-container">', unsafe_allow_html=True)
    
    # Input text dengan key dinamis agar ter-clear setelah kirim
    input_key = f"user_input_{st.session_state.input_counter}"
    user_input = st.text_input(
        "Ketik pesan Anda...",
        placeholder="Contoh: pesan 2 tiket Avenger jam 7 malam",
        key=input_key,
        label_visibility="collapsed"
    )
    
    # Tombol kirim
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("Kirim 📤", use_container_width=True, type="primary"):
            handle_user_input(user_input)
            st.session_state.input_counter += 1  # ganti key → input ter-clear
            st.rerun()
    
    # Tombol reset
    with col3:
        if st.button("Reset 🔄", use_container_width=True):
            st.session_state.chatbot = ChatbotFSM()
            st.session_state.messages = []
            st.session_state.current_state = State.START
            st.session_state.input_counter = 0
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)


def display_sidebar():
    """Tampilkan sidebar dengan informasi tambahan"""
    # Baca film dari engine agar selalu sinkron
    nlp = NLPEngine()
    
    with st.sidebar:
        st.markdown("### 📋 Informasi")
        
        st.markdown("#### Film Tersedia")
        for movie in nlp.movies:
            st.markdown(f"- {movie}")
        
        st.markdown("#### Jam Tayang")
        times = ["10:00", "13:00", "16:00", "19:00", "22:00"]
        for time in times:
            st.markdown(f"- {time}")
        
        st.markdown("#### Harga Tiket")
        st.markdown("Rp 50.000 per tiket")
        
        st.markdown("---")
        st.markdown("### 💡 Tips")
        st.markdown("""
- Gunakan format: "pesan [jumlah] tiket [nama film] jam [waktu]"
- Contoh: "pesan 2 tiket Avenger jam 7 malam"
- Ketik "batal" untuk membatalkan pesanan
- Ketik "lihat film" untuk melihat daftar film
        """)


def main():
    """Fungsi utama aplikasi"""
    # Inisialisasi session state
    initialize_session_state()
    
    # Tampilkan header
    display_header()
    
    # Tampilkan sidebar
    display_sidebar()
    
    # Tampilkan state saat ini
    display_current_state()
    
    # Tampilkan riwayat percakapan
    display_chat_history()
    
    # Tampilkan area input
    display_input_area()
    
    # Footer
    st.markdown("""
    <div style='text-align: center; color: #888; margin-top: 30px;'>
        <p>🎬 Chatbot Bioskop © 2024 | Dibuat dengan Python & Streamlit</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
