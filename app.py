import streamlit as st
import time

# 페이지 설정
st.set_page_config(
    page_title="공부도우미",
    page_icon="📚",
    layout="wide"
)

# 세션 상태 초기화
if "page" not in st.session_state:
    st.session_state.page = "홈"

if "timer_running" not in st.session_state:
    st.session_state.timer_running = False


# 사이드바 (좌측 상단 페이지 이동)
st.sidebar.title("🤖 공부도우미")
st.sidebar.write("공부가 힘들 때 도와주는 친구!")

page = st.sidebar.radio(
    "페이지 이동",
    ["홈", "공부 팁", "학습 계획", "집중 타이머", "학습 체크"]
)

st.session_state.page = page


# 홈 화면
if st.session_state.page == "홈":
    st.title("📚 공부도우미")

    st.markdown("""
    ### 🤖 공부도우미 등장!

    안녕! 나는 **공부도우미**야.

    공부가 어렵고 집중이 안 될 때,
    내가 공부 팁과 계획 세우기를 도와줄게!
    """)

    st.info("💡 작은 목표부터 시작하면 공부가 훨씬 쉬워져요.")

    goal = st.text_input("오늘 이루고 싶은 목표를 적어보세요")

    if goal:
        st.success(f"좋아요! 오늘의 목표는 '{goal}' 입니다. 화이팅! 🔥")


# 공부 팁 페이지
elif st.session_state.page == "공부 팁":

    st.title("💡 공부 팁")

    tips = [
        "25분 공부 + 5분 휴식(포모도로 기법)을 활용해보세요.",
        "어려운 과목은 가장 집중이 잘 되는 시간에 공부하세요.",
        "암기는 소리 내어 읽거나 직접 써보는 것이 효과적입니다.",
        "핸드폰 알림을 끄면 집중력이 크게 향상됩니다.",
        "공부 후에는 배운 내용을 스스로 설명해보세요.",
        "잠을 충분히 자는 것도 공부의 일부입니다."
    ]

    for i, tip in enumerate(tips, start=1):
        st.write(f"{i}. {tip}")

    st.success("꾸준함이 최고의 공부 비법입니다! 😊")


# 학습 계획 페이지
elif st.session_state.page == "학습 계획":

    st.title("📝 학습 계획")

    try:
        subject = st.selectbox(
            "과목 선택",
            ["국어", "영어", "수학", "과학", "사회", "기타"]
        )

        study_time = st.slider(
            "공부 시간(분)",
            min_value=10,
            max_value=300,
            value=60
        )

        memo = st.text_area("학습 내용")

        if st.button("계획 저장"):
            st.success(
                f"""
                저장 완료!

                과목: {subject}
                공부 시간: {study_time}분
                내용: {memo}
                """
            )

    except Exception as e:
        st.error(f"오류가 발생했습니다: {e}")


# 집중 타이머 페이지
elif st.session_state.page == "집중 타이머":

    st.title("⏱️ 집중 타이머")

    try:
        minutes = st.number_input(
            "집중할 시간(분)",
            min_value=1,
            max_value=120,
            value=25
        )

        if st.button("타이머 시작"):
            progress = st.progress(0)
            status = st.empty()

            total_seconds = int(minutes * 60)

            for i in range(total_seconds):
                percent = (i + 1) / total_seconds
                progress.progress(percent)

                remain = total_seconds - i - 1
                mins = remain // 60
                secs = remain % 60

                status.write(
                    f"남은 시간: {mins:02d}:{secs:02d}"
                )

                time.sleep(1)

            st.success("🎉 집중 시간 완료! 수고했어요!")

    except Exception as e:
        st.error(f"오류가 발생했습니다: {e}")


# 학습 체크 페이지
elif st.session_state.page == "학습 체크":

    st.title("📈 오늘의 학습 상태")

    try:
        concentration = st.slider(
            "오늘 집중도",
            1,
            10,
            5
        )

        understanding = st.slider(
            "오늘 이해도",
            1,
            10,
            5
        )

        effort = st.slider(
            "오늘 노력도",
            1,
            10,
            5
        )

        avg = round(
            (concentration + understanding + effort) / 3,
            1
        )

        st.metric(
            label="오늘의 학습 점수",
            value=f"{avg}/10"
        )

        if avg >= 8:
            st.success("훌륭해요! 아주 좋은 학습 상태입니다. 🌟")

        elif avg >= 5:
            st.info("잘하고 있어요! 조금만 더 힘내봐요. 😊")

        else:
            st.warning("괜찮아요. 내일은 더 나아질 수 있어요! 💪")

    except Exception as e:
        st.error(f"오류가 발생했습니다: {e}")
