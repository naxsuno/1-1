import streamlit as st
import google.generativeai as genai
import pandas as pd

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="메타노트 AI | 스마트 AI 오답노트",
    page_icon="📝",
    layout="wide",
)

# 2. API 키 설정 및 예외 처리
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
else:
    st.error("❌ Streamlit Secrets에 'GEMINI_API_KEY'가 설정되지 않았습니다.")
    st.stop()

try:
    model = genai.GenerativeModel("gemini-2.5-flash-lite")
except Exception as e:
    st.error(f"모델 초기화 중 오류 발생: {e}")
    st.stop()

# 3. 세션 상태(Session State) 초기화 - 누적 통계용
if "wrong_history" not in st.session_state:
    st.session_state["wrong_history"] = []

# 4. 사이드바 - 누적 데이터 시각화
with st.sidebar:
    st.title("📝 메타노트 AI")
    st.subheader("실수를 실력으로 바꾸는 시간")
    st.write("---")
    
    # 누적 통계 보여주기
    st.markdown("### 📊 나의 오답 누적 통계")
    if len(st.session_state["wrong_history"]) == 0:
        st.info("아직 분석한 오답이 없습니다. 메인 창에서 첫 오답을 분석해 보세요!")
    else:
        # 데이터프레임 변환 후 그래프 그리기
        df = pd.DataFrame(st.session_state["wrong_history"], columns=["과목"])
        subject_counts = df["과목"].value_counts()
        st.bar_chart(subject_counts)
        if st.button("통계 초기화"):
            st.session_state["wrong_history"] = []
            st.rerun()
            
    st.write("---")
    st.caption("Powered by Gemini 2.5 Flash Lite")

# 5. 메인 화면 타이틀
st.title("🔍 AI 오답 유형 및 취약점 분석기")
st.write("틀린 과목, 실수 유형 태그, 세부 내용을 입력하시면 AI가 맞춤형 처방전을 발행해 드립니다.")
st.markdown("---")

# 6. 오답 입력 폼
with st.form("wrong_answer_form_v3"):
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # 과목 선택지에 '기타'를 확실히 추가했습니다.
        wrong_subject = st.selectbox(
            "🎯 과목을 선택하세요",
            ["국어", "수학", "영어", "한국사", "사회탐구", "과학탐구", "기타"]
        )
        
        # 실수 태그 선택
        error_tags = st.multiselect(
            "🏷️ 이번 실수의 원인 태그 (중복 선택 가능)",
