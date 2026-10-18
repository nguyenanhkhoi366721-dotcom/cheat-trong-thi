import random
import streamlit as st

st.set_page_config(
    page_title="Cheat Trong Thi",
    page_icon="🎓",
    layout="centered",
)

MAX_TURNS = 8


def new_game():
    st.session_state.score = 0
    st.session_state.suspicion = 0
    st.session_state.turns = MAX_TURNS
    st.session_state.playing = True
    st.session_state.caught = False
    st.session_state.log = ["🔔 Bắt đầu bài kiểm tra!"]
    st.session_state.message = "Hãy lựa chọn chiến thuật của bạn."


def take_action(action):
    if not st.session_state.playing:
        return

    score = st.session_state.score
    suspicion = st.session_state.suspicion
    message = ""

    if action == "study":
        score += 10
        suspicion = max(0, suspicion - 5)
        message = "📘 Bạn tập trung làm bài. +10 điểm."

    elif action == "risk":
        score += 20
        suspicion += 20
        message = "🎲 Bạn chọn hành động mạo hiểm. +20 điểm."

        # Rủi ro tăng theo mức nghi ngờ hiện tại.
        chance = min(0.65, 0.15 + suspicion / 200)

        if random.random() < chance:
            st.session_state.caught = True
            message += " 🚨 Giáo viên phát hiện bạn!"

    elif action == "observe":
        suspicion = max(0, suspicion - 15)
        score += 2
        message = "👀 Bạn bình tĩnh quan sát. +2 điểm."

    st.session_state.score = score
    st.session_state.suspicion = min(100, suspicion)
    st.session_state.turns -= 1
    st.session_state.message = message
    st.session_state.log.insert(0, message)

    if st.session_state.suspicion >= 100:
        st.session_state.caught = True

    if st.session_state.caught:
        st.session_state.playing = False
        st.session_state.log.insert(
            0, "❌ Ván chơi kết thúc: bạn đã bị phát hiện."
        )
    elif st.session_state.turns <= 0:
        st.session_state.playing = False
        st.session_state.log.insert(
            0, "🏁 Hết giờ! Bài kiểm tra đã kết thúc."
        )


# Khởi tạo trạng thái khi người chơi truy cập lần đầu.
if "playing" not in st.session_state:
    new_game()

st.title("🎓 Cheat Trong Thi")
st.caption("Game chiến thuật học đường — phiên bản thử nghiệm")

st.info(
    "Mục tiêu: tích lũy điểm, quản lý mức nghi ngờ "
    "và hoàn thành 8 lượt chơi."
)

# Bảng trạng thái.
col1, col2, col3 = st.columns(3)

col1.metric("🏆 Điểm", st.session_state.score)
col2.metric("👁️ Nghi ngờ", f"{st.session_state.suspicion}%")
col3.metric("⏳ Lượt còn", st.session_state.turns)

st.progress(st.session_state.suspicion / 100)

if st.session_state.playing:
    st.subheader("Bạn sẽ làm gì?")

    col_a, col_b, col_c = st.columns(3)

    with col_a:
        st.button(
            "📘 Làm bài",
            on_click=take_action,
            args=("study",),
            use_container_width=True,
        )
        st.caption("+10 điểm, giảm nghi ngờ")

    with col_b:
        st.button(
            "🎲 Mạo hiểm",
            on_click=take_action,
            args=("risk",),
            use_container_width=True,
        )
        st.caption("+20 điểm, rủi ro bị phát hiện")

    with col_c:
        st.button(
            "👀 Quan sát",
            on_click=take_action,
            args=("observe",),
            use_container_width=True,
        )
        st.caption("+2 điểm, giảm nghi ngờ")

    st.write(st.session_state.message)

else:
    st.subheader("📋 Kết quả ván chơi")

    if st.session_state.caught:
        st.error("Bạn đã bị giáo viên phát hiện!")
    else:
        st.success("Bạn đã hoàn thành bài kiểm tra!")

    st.write(f"Điểm cuối cùng: **{st.session_state.score}**")

    if st.session_state.score >= 100:
        st.write("🏆 Xếp hạng: Xuất sắc")
    elif st.session_state.score >= 60:
        st.write("🥈 Xếp hạng: Khá")
    else:
        st.write("📚 Xếp hạng: Cần cố gắng")

    st.button("🔄 Chơi lại", on_click=new_game)

with st.expander("📜 Nhật ký ván chơi"):
    for item in st.session_state.log:
        st.write(item)

st.divider()
st.caption("Cheat Trong Thi • Prototype v0.1")
