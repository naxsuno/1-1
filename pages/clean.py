import streamlit as st
import google.generativeai as genai

# 페이지 설정
st.set_page_config(
    page_title="Study Mate AI",
    page_icon="📚",
    layout="wide"
)

# 제목
st.title("📚 Study Mate AI")
st.caption("과제, 문제풀이, 강의자료 요약, 개념 설명까지 한 번에!")

# API 설정
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.5-flash-lite")
except Exception:
    st.error("GEMINI_API_KEY가 설정되지 않았습니다.")
    st.stop()


def ask_gemini(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"오류가 발생했습니다.\n\n{str(e)}"


# 메뉴
menu = st.sidebar.radio(
    "기능 선택",
    [
        "문제 풀이",
        "과제 도우미",
        "강의 자료 요약",
        "개념 설명",
        "암기 퀴즈 생성"
    ]
)

# 문제 풀이
if menu == "문제 풀이":
    st.header("📝 문제 풀이 도우미")

    question = st.text_area(
        "문제를 입력하세요",
        height=200
    )

    if st.button("풀이 보기"):
        if question.strip():
            prompt = f"""
            다음 문제를 단계별로 설명하며 풀어줘.

            문제:
            {question}
            """
            with st.spinner("풀이 생성 중..."):
                result = ask_gemini(prompt)

            st.markdown(result)
        else:
            st.warning("문제를 입력해주세요.")

# 과제 도우미
elif menu == "과제 도우미":
    st.header("📄 과제 도우미")

    topic = st.text_input("과제 주제")

    if st.button("과제 방향 제안"):
        if topic.strip():
            prompt = f"""
            다음 과제의 작성 방향을 알려줘.

            주제:
            {topic}

            아래 형식으로 작성:
            1. 과제 개요
            2. 핵심 내용
            3. 목차 예시
            4. 참고하면 좋은 키워드
            """
            with st.spinner("생성 중..."):
                result = ask_gemini(prompt)

            st.markdown(result)
        else:
            st.warning("주제를 입력해주세요.")

# 강의자료 요약
elif menu == "강의 자료 요약":
    st.header("📚 강의 자료 요약")

    lecture = st.text_area(
        "강의 자료 또는 긴 내용을 붙여넣으세요",
        height=300
    )

    if st.button("요약하기"):
        if lecture.strip():
            prompt = f"""
            아래 내용을 공부용으로 요약해줘.

            내용:
            {lecture}

            형식:
            - 핵심 요약
            - 중요 개념
            - 시험 대비 포인트
            """
            with st.spinner("요약 중..."):
                result = ask_gemini(prompt)

            st.markdown(result)
        else:
            st.warning("내용을 입력해주세요.")

# 개념 설명
elif menu == "개념 설명":
    st.header("💡 개념 설명")

    concept = st.text_input("설명받고 싶은 개념")

    level = st.selectbox(
        "설명 수준",
        ["중학생", "고등학생", "대학생"]
    )

    if st.button("설명 받기"):
        if concept.strip():
            prompt = f"""
            '{concept}' 개념을 {level} 수준으로 쉽게 설명해줘.

            포함:
            - 정의
            - 쉬운 설명
            - 예시
            - 시험 포인트
            """
            with st.spinner("설명 생성 중..."):
                result = ask_gemini(prompt)

            st.markdown(result)
        else:
            st.warning("개념을 입력해주세요.")

# 퀴즈 생성
elif menu == "암기 퀴즈 생성":
    st.header("🎯 암기 퀴즈 생성")

    content = st.text_area(
        "공부 내용을 입력하세요",
        height=250
    )

    if st.button("퀴즈 만들기"):
        if content.strip():
            prompt = f"""
            아래 학습 내용으로 퀴즈 5개를 만들어줘.

            내용:
            {content}

            형식:
            문제
            정답
            해설
            """
            with st.spinner("퀴즈 생성 중..."):
                result = ask_gemini(prompt)

            st.markdown(result)
        else:
            st.warning("내용을 입력해주세요.")

# 하단 안내
st.divider()
st.info(
    "📚 과제 작성, 문제 풀이, 개념 학습, 강의 자료 요약, 암기 퀴즈 생성을 지원합니다."
)
