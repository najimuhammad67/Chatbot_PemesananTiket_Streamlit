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
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* ── Global ── */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #1a1a2e 50%, #16213e 100%);
        min-height: 100vh;
    }

    /* ── Hide default streamlit chrome ── */
    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding-top: 1.5rem; padding-bottom: 2rem; }

    /* ── Header ── */
    .header {
        text-align: center;
        padding: 28px 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 60%, #f64f59 100%);
        border-radius: 18px;
        margin-bottom: 18px;
        color: white;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.4);
        position: relative;
        overflow: hidden;
    }
    .header::before {
        content: '';
        position: absolute;
        top: -50%; left: -50%;
        width: 200%; height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.08) 0%, transparent 60%);
        animation: shimmer 4s infinite linear;
    }
    @keyframes shimmer {
        0%   { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    .header h1 {
        font-size: 2rem;
        font-weight: 700;
        margin: 0 0 6px 0;
        letter-spacing: -0.5px;
        text-shadow: 0 2px 8px rgba(0,0,0,0.3);
    }
    .header p {
        font-size: 0.9rem;
        font-weight: 300;
        margin: 0;
        opacity: 0.88;
    }

    /* ── Chat container ── */
    .chat-container {
        background: rgba(255, 255, 255, 0.04);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 18px;
        padding: 22px 18px;
        margin-bottom: 16px;
        max-height: 520px;
        overflow-y: auto;
        scroll-behavior: smooth;
    }
    /* Custom scrollbar */
    .chat-container::-webkit-scrollbar { width: 5px; }
    .chat-container::-webkit-scrollbar-track { background: transparent; }
    .chat-container::-webkit-scrollbar-thumb {
        background: rgba(255,255,255,0.15);
        border-radius: 10px;
    }

    /* ── Pesan user ── */
    .user-message {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: white;
        padding: 12px 18px;
        border-radius: 18px 18px 4px 18px;
        margin: 8px 0 8px auto;
        max-width: 78%;
        width: fit-content;
        text-align: left;
        font-size: 0.92rem;
        line-height: 1.55;
        box-shadow: 0 4px 15px rgba(17, 153, 142, 0.35);
        animation: slideInRight 0.25s ease-out;
        white-space: pre-wrap;
        word-break: break-word;
    }
    @keyframes slideInRight {
        from { opacity: 0; transform: translateX(16px); }
        to   { opacity: 1; transform: translateX(0); }
    }

    /* ── Pesan bot ── */
    .bot-message {
        background: rgba(255, 255, 255, 0.07);
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: #e8eaf0;
        padding: 12px 18px;
        border-radius: 18px 18px 18px 4px;
        margin: 8px auto 8px 0;
        max-width: 82%;
        width: fit-content;
        font-size: 0.92rem;
        line-height: 1.6;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        animation: slideInLeft 0.25s ease-out;
        white-space: pre-wrap;
        word-break: break-word;
    }
    @keyframes slideInLeft {
        from { opacity: 0; transform: translateX(-16px); }
        to   { opacity: 1; transform: translateX(0); }
    }

    /* ── Avatar label ── */
    .user-label {
        text-align: right;
        font-size: 0.72rem;
        color: rgba(255,255,255,0.4);
        margin-bottom: 2px;
        margin-right: 4px;
        font-weight: 500;
        letter-spacing: 0.3px;
    }
    .bot-label {
        text-align: left;
        font-size: 0.72rem;
        color: rgba(255,255,255,0.4);
        margin-bottom: 2px;
        margin-left: 4px;
        font-weight: 500;
        letter-spacing: 0.3px;
    }

    /* ── State badge ── */
    .state-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(255,255,255,0.07);
        border: 1px solid rgba(255,255,255,0.12);
        color: #c9d1e0;
        padding: 5px 14px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.5px;
        margin-bottom: 12px;
        text-transform: uppercase;
        backdrop-filter: blur(8px);
    }
    .state-dot {
        width: 8px; height: 8px;
        border-radius: 50%;
        background: #38ef7d;
        box-shadow: 0 0 6px #38ef7d;
        animation: pulse 1.8s infinite;
    }
    @keyframes pulse {
        0%, 100% { opacity: 1; transform: scale(1); }
        50%       { opacity: 0.5; transform: scale(0.75); }
    }

    /* ── Input container ── */
    .input-container {
        background: rgba(255,255,255,0.04);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 18px;
        padding: 20px 22px;
        margin-top: 14px;
    }

    /* ── Streamlit text input override ── */
    .stTextInput > div > div > input {
        background: rgba(255,255,255,0.06) !important;
        border: 1.5px solid rgba(255,255,255,0.12) !important;
        border-radius: 12px !important;
        color: #e8eaf0 !important;
        font-size: 0.93rem !important;
        padding: 10px 16px !important;
        transition: border-color 0.2s;
    }
    .stTextInput > div > div > input:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102,126,234,0.2) !important;
    }
    .stTextInput > div > div > input::placeholder {
        color: rgba(200,200,220,0.35) !important;
    }

    /* ── Tombol Kirim (primary) ── */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        font-size: 0.88rem !important;
        padding: 10px 0 !important;
        box-shadow: 0 4px 15px rgba(102,126,234,0.4) !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button[kind="primary"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(102,126,234,0.55) !important;
    }

    /* ── Tombol Reset (secondary) ── */
    .stButton > button[kind="secondary"] {
        background: rgba(255,255,255,0.06) !important;
        color: #c9d1e0 !important;
        border: 1.5px solid rgba(255,255,255,0.12) !important;
        border-radius: 12px !important;
        font-weight: 500 !important;
        font-size: 0.88rem !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button[kind="secondary"]:hover {
        background: rgba(255,255,255,0.12) !important;
        border-color: rgba(255,255,255,0.25) !important;
    }

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%) !important;
        border-right: 1px solid rgba(255,255,255,0.07) !important;
    }
    [data-testid="stSidebar"] h3 {
        color: #e8eaf0;
        font-size: 0.95rem;
        font-weight: 700;
        letter-spacing: 0.3px;
    }
    [data-testid="stSidebar"] h4 {
        color: #a0aec0;
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin-top: 14px;
    }
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] li {
        color: #c9d1e0;
        font-size: 0.87rem;
    }
    [data-testid="stSidebar"] hr {
        border-color: rgba(255,255,255,0.08) !important;
    }

    /* ── Film card di sidebar ── */
    .film-card {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 10px;
        padding: 7px 12px;
        margin-bottom: 6px;
        color: #e8eaf0;
        font-size: 0.86rem;
        font-weight: 500;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    /* ── Harga badge ── */
    .price-badge {
        background: linear-gradient(135deg, #f6d365 0%, #fda085 100%);
        color: #1a1a2e;
        padding: 6px 14px;
        border-radius: 10px;
        font-weight: 700;
        font-size: 0.88rem;
        display: inline-block;
        margin-top: 4px;
    }

    /* ── Footer ── */
    .footer {
        text-align: center;
        color: rgba(255,255,255,0.25);
        font-size: 0.78rem;
        margin-top: 24px;
        padding-top: 16px;
        border-top: 1px solid rgba(255,255,255,0.06);
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
                st.markdown(f'<div class="user-label">Kamu 👤</div><div class="user-message">{message["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="bot-label">🎬 Bioskop Bot</div><div class="bot-message">{message["content"]}</div>', unsafe_allow_html=True)
        
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
    st.markdown(f'<div class="state-badge"><span class="state-dot"></span> State: {current_state.value}</div>', unsafe_allow_html=True)


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
    # Baca katalog film dari engine agar selalu sinkron
    nlp = NLPEngine()
    
    with st.sidebar:
        st.markdown("### 📋 Informasi")
        
        st.markdown("#### Film Tersedia")
        movie_icons = ["🦸", "🦇", "🕷️", "🃏"]
        for i, (name, price) in enumerate(nlp.movie_catalog.items()):
            icon = movie_icons[i] if i < len(movie_icons) else "🎬"
            st.markdown(
                f'<div class="film-card">'
                f'{icon} <span style="flex:1">{name}</span>'
                f'<span class="price-badge" style="font-size:0.75rem;padding:3px 9px;margin:0">Rp {price:,}</span>'
                f'</div>',
                unsafe_allow_html=True
            )
        
        st.markdown("#### Jam Tayang")
        times = ["10:00", "13:00", "16:00", "19:00", "22:00"]
        for time in times:
            st.markdown(f"- {time}")
        
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
    <div class="footer">
        🎬 Chatbot Bioskop &nbsp;|&nbsp; Dibuat dengan Python &amp; Streamlit &nbsp;|&nbsp; FSM + NLP Regex
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
