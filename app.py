import streamlit as st
import random
import time
import base64
import os

# Cấu hình trang vừa gọn trong màn hình máy tính
st.set_page_config(
    page_title="Oẳn Tù Tì Cùng An Nhi",
    page_icon="💖",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- CSS TÙY CHỈNH GIAO DIỆN HỒNG & VỪA KHUNG MÀN HÌNH ---
st.markdown("""
<style>
    /* Ẩn header và footer mặc định của Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Cố định khung container vừa màn hình desktop */
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 1rem !important;
        max-width: 800px !important;
    }
    
    /* Background màu hồng gradient */
    .stApp {
        background: linear-gradient(135deg, #ff75ac 0%, #ffa6c9 100%);
    }

    /* Tiêu đề */
    .title-text {
        text-align: center;
        color: white;
        font-size: 28px;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        margin-bottom: 10px;
    }

    /* Thẻ hiển thị hình ảnh avatar */
    .card {
        background: white;
        border-radius: 15px;
        padding: 10px;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.15);
        text-align: center;
    }
    .card img {
        width: 100%;
        height: 220px;
        object-fit: cover;
        border-radius: 10px;
    }

    /* Thanh máu HP */
    .hp-bar-container {
        background-color: #ddd;
        border-radius: 10px;
        height: 16px;
        width: 100%;
        margin-top: 8px;
        overflow: hidden;
    }
    .hp-bar-fill {
        background-color: #2ed573;
        height: 100%;
        transition: width 0.3s ease;
    }

    /* Chữ VS */
    .vs-text {
        font-size: 32px;
        font-weight: 900;
        color: #ffeb3b;
        text-align: center;
        margin-top: 90px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    /* Chữ đếm ngược */
    .countdown-text {
        font-size: 45px;
        font-weight: bold;
        color: #ffff00;
        text-align: center;
        animation: pulse 0.5s infinite alternate;
    }
</style>
""", unsafe_allow_html=True)

# --- KHỞI TẠO TẠO TRẠNG THÁI GAME (SESSION STATE) ---
if 'player_hp' not in st.session_state:
    st.session_state.player_hp = 100
if 'bot_hp' not in st.session_state:
    st.session_state.bot_hp = 100
if 'game_status' not in st.session_state:
    st.session_state.game_status = "idle" # idle, counting, result
if 'audio_to_play' not in st.session_state:
    st.session_state.audio_to_play = "bg_sound.mp3"

# --- HÀM TẢI ÂM THANH TỰ ĐỘNG PHÁT ---
def play_audio(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            md = f"""
                <audio autoplay style="display:none;">
                <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
                </audio>
                """
            st.markdown(md, unsafe_allow_html=True)

# Tải âm thanh tương ứng
play_audio(f"assets/{st.session_state.audio_to_play}")

# --- TIÊU ĐỀ GAME ---
st.markdown("<div class='title-text'>💖 OẮN TÙ TÌ CÙNG AN NHI 💖</div>", unsafe_allow_html=True)

# --- KHUNG HIỂN THỊ 2 NHÂN VẬT & MÁU ---
col1, col2, col3 = st.columns([4, 1.5, 4])

with col1:
    st.markdown("<h4 style='text-align: center; color: white;'>🐶 BẠN</h4>", unsafe_allow_html=True)
    st.markdown("""
    <div class='card'>
        <img src='app/static/assets/dog.jpg' err-src='assets/dog.jpg'>
    </div>
    """, unsafe_allow_html=True)
    # Hiển thị thanh máu Bạn
    st.markdown(f"""
    <div class='hp-bar-container'>
        <div class='hp-bar-fill' style='width: {st.session_state.player_hp}%;'></div>
    </div>
    <p style='text-align:center; color:white; font-weight:bold; margin-top:3px;'>HP: {st.session_state.player_hp}/100</p>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("<div class='vs-text'>VS</div>", unsafe_allow_html=True)

with col3:
    st.markdown("<h4 style='text-align: center; color: white;'>👶 AN NHI</h4>", unsafe_allow_html=True)
    st.markdown("""
    <div class='card'>
        <img src='app/static/assets/annhi.jpg' err-src='assets/annhi.jpg'>
    </div>
    """, unsafe_allow_html=True)
    # Hiển thị thanh máu An Nhi
    st.markdown(f"""
    <div class='hp-bar-container'>
        <div class='hp-bar-fill' style='width: {st.session_state.bot_hp}%;'></div>
    </div>
    <p style='text-align:center; color:white; font-weight:bold; margin-top:3px;'>HP: {st.session_state.bot_hp}/100</p>
    """, unsafe_allow_html=True)

st.divider()

# --- XỬ LÝ NÚT CHỌN ĐÒN VÀ ĐẾM NGƯỢC ---
choices = ["✌️ Kéo", "✊ Búa", "🖐️ Bao"]

# Kiểm tra hết máu
if st.session_state.player_hp <= 0 or st.session_state.bot_hp <= 0:
    if st.session_state.player_hp <= 0:
        st.error("😭 Bạn đã cạn máu và thua cuộc!")
    else:
        st.balloons()
        st.success("🎉 Bạn đã chiến thắng An Nhi!")
    
    if st.button("🔄 Chơi lại trận mới"):
        st.session_state.player_hp = 100
        st.session_state.bot_hp = 100
        st.session_state.audio_to_play = "bg_sound.mp3"
        st.rerun()

else:
    st.write("### 🎯 Chọn nước đi của bạn:")
    btn_col1, btn_col2, btn_col3 = st.columns(3)
    
    user_choice = None
    if btn_col1.button("✌️ Kéo", use_container_width=True):
        user_choice = "✌️ Kéo"
    if btn_col2.button("✊ Búa", use_container_width=True):
        user_choice = "✊ Búa"
    if btn_col3.button("🖐️ Bao", use_container_width=True):
        user_choice = "🖐️ Bao"

    # Nếu người dùng bấm chọn đòn
    if user_choice:
        countdown_placeholder = st.empty()
        
        # Đếm ngược 3.. 2.. 1..
        for i in range(3, 0, -1):
            countdown_placeholder.markdown(f"<div class='countdown-text'>{i}</div>", unsafe_allow_html=True)
            time.sleep(0.7)
        
        countdown_placeholder.markdown("<div class='countdown-text'>🔥 RA ĐÒN!</div>", unsafe_allow_html=True)
        time.sleep(0.4)
        countdown_placeholder.empty()

        # An Nhi chọn ngẫu nhiên
        bot_choice = random.choice(choices)
        
        st.info(f"👉 Bạn ra: **{user_choice}**  |  👶 An Nhi ra: **{bot_choice}**")

        # Xử lý kết quả thắng/thua/hòa
        if user_choice == bot_choice:
            st.warning("🤝 Hòa nhau rồi!")
            st.session_state.audio_to_play = "bg_sound.mp3"
        elif (user_choice == "✌️ Kéo" and bot_choice == "🖐️ Bao") or \
             (user_choice == "✊ Búa" and bot_choice == "✌️ Kéo") or \
             (user_choice == "🖐️ Bao" and bot_choice == "✊ Búa"):
            st.success("🎉 Bạn thắng lượt này! An Nhi bị trừ 20 HP!")
            st.session_state.bot_hp = max(0, st.session_state.bot_hp - 20)
            st.session_state.audio_to_play = "win_sound.mp3"
        else:
            st.error("💔 Bạn thua lượt này! Bạn bị trừ 20 HP!")
            st.session_state.player_hp = max(0, st.session_state.player_hp - 20)
            st.session_state.audio_to_play = "lose_sound.mp3"
            
        st.rerun()