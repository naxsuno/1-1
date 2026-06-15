import streamlit as st
from datetime import datetime

# -----------------------------
# 기본 설정
# -----------------------------
st.set_page_config(
    page_title="공부 도우미 선배",
    page_icon="📚",
    layout="wide"
)

# -----------------------------
# 스타일
# -----------------------------
st.markdown("""
<style>

.main {
    background-color: #f7f9fc;
}

.character-box{
    background: linear-gradient(135deg,#4F8BF9,#6FA8FF);
    padding:25px;
    border-radius:20px;
    color:white;
    margin-bottom:15px;
}

.card{
    background:white;
    padding:20px;
    border-radius:15px;
    box-shadow:0px 2px 10px rgba(0,0,0,0.08);
    margin-bottom:15px;
}

.tip-box{
    background:#eef5ff;
    padding:15px;
    border-radius:12px;
    border-left:5px solid #4F8BF9;
}

.big-title{
    font-size:32px;
    font-weight:700;
}

.small-text{
    color:#666;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# 캐릭터
# -----------------------------
CHARACTER_NAME = "민준 선배"

tips = [
    "완벽하게 하려고 하지 말고 10분만 시작해봐.",
    "암기보다 이해를 먼저 하면 기억이 오래가.",
    "공부 계획은 작게 쪼갤수록 성공 확률이 높아.",
    "집중이 안 되면 25분 공부 + 5분 휴식을 시도해봐.",
    "어제의 나보다 조금만 성장하면 충분해."
]

# -----------------------------
# 사이드바
# -----------------------------
st.sidebar.title("📚 공부 도우미")

page = st.sidebar.radio(
    "어떤 도움이 필요해?",
    [
        "홈",
        "공부 계획 세우기",
        "집중 타이머",
        "오늘의 공부 체크",
        "동기부여 메시지",
        "학습 팁 모음"
    ]
)

# -----------------------------
# 홈
# -----------------------------
if page == "홈":

    st.markdown(f"""
    <div class="character-box">
        <div class="big-title">👨‍🎓 {CHARACTER_NAME}</div>
        <br>
        공부가 어렵게 느껴질 때가 있지?
        <br><br>
        <b>어떤 걸 도와줄까?</b>
        <br>
        왼쪽 메뉴에서 필요한 기능을 선택해봐!
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="card">
        <h3>📝 공부 계획 세우기</h3>
        해야 할 일을 정리하고 우선순위를 정해보자.
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="card">
        <h3>⏰ 집중 타이머</h3>
        25분 집중, 5분 휴식 방식으로 공부해보자.
        </div>
        """, unsafe_allow_html=True)

    col3, col4 = st.columns(2)

    with col3:
        st.markdown("""
        <div class="card">
        <h3>✅ 공부 체크</h3>
        오늘 얼마나 해냈는지 확인해보자.
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
        <div class="card">
        <h3>💪 동기부여</h3>
        공부가 지칠 때 응원을 받아보자.
        </div>
        """, unsafe_allow_html=True)

# -----------------------------
# 공부 계획
# -----------------------------
elif page == "공부 계획 세우기":

    st.title("📝 공부 계획 세우기")

    st.write("오늘 해야 할 공부를 정리해보자.")

    task = st.text_input("할 일")

    priority = st.selectbox(
        "우선순위",
        ["높음", "보통", "낮음"]
    )

    if st.button("추가하기"):

        if task.strip():

            st.success("계획이 추가되었어!")

            st.markdown(f"""
            <div class="card">
            <b>할 일:</b> {task}<br>
            <b>우선순위:</b> {priority}
            </div>
            """, unsafe_allow_html=True)

        else:
            st.warning("할 일을 입력해줘.")

# -----------------------------
# 집중 타이머
# -----------------------------
elif page == "집중 타이머":

    st.title("⏰ 집중 타이머")

    st.markdown("""
    <div class="tip-box">
    추천: 25분 집중 + 5분 휴식
    </div>
    """, unsafe_allow_html=True)

    focus = st.slider(
        "집중 시간(분)",
        5,
        60,
        25
    )

    st.info(
        f"📚 {focus}분 동안 한 가지 과목에만 집중해보자!"
    )

    st.progress(100)

# -----------------------------
# 공부 체크
# -----------------------------
elif page == "오늘의 공부 체크":

    st.title("✅ 오늘의 공부 체크")

    study = st.checkbox("공부 시작하기")
    phone = st.checkbox("공부 중 휴대폰 멀리 두기")
    review = st.checkbox("복습하기")
    finish = st.checkbox("계획한 공부 마치기")

    score = sum([study, phone, review, finish])

    st.markdown(f"""
    <div class="card">
    <h3>오늘의 달성도</h3>
    {score} / 4 완료
    </div>
    """, unsafe_allow_html=True)

    st.progress(score / 4)

# -----------------------------
# 동기부여
# -----------------------------
elif page == "동기부여 메시지":

    st.title("💪 동기부여 메시지")

    messages = [
        "지금 하는 10분이 미래의 큰 차이를 만든다.",
        "공부는 재능보다 꾸준함이 더 중요해.",
        "오늘 조금이라도 했다면 이미 전진한 거야.",
        "완벽하지 않아도 괜찮아. 계속하는 게 중요해.",
        "성장은 눈에 안 보여도 분명히 쌓이고 있어."
    ]

    if st.button("응원받기"):

        import random

        st.success(random.choice(messages))

# -----------------------------
# 학습 팁
# -----------------------------
elif page == "학습 팁 모음":

    st.title("📖 학습 팁")

    for tip in tips:
        st.markdown(f"""
        <div class="tip-box">
        {tip}
        </div>
        <br>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
    <h3>📌 추천 공부 순서</h3>

    1. 오늘 할 일 정하기<br>
    2. 25분 집중 공부<br>
    3. 5분 휴식<br>
    4. 간단한 복습<br>
    5. 체크리스트 확인
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# 하단
# -----------------------------
st.markdown("---")
st.caption(
    f"📚 {CHARACTER_NAME} | 공부가 막막할 때 옆에서 도와주는 선배 컨셉"
)
