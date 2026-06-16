import streamlit as st
import pandas as pd
import Google.generativeai as genai

# 1. 페이지 설정 및 테마
st.set_page_config(
    page_title="스마트 고교 생활 & 대입 매니저",
    page_icon="🎓",
    layout="wide"
)

# 2. 고유한 스타일 적용 (CSS)
st.markdown("""
    <style>
    .main-title { font-size: 2.5rem; font-weight: bold; color: #1E3A8A; margin-bottom: 20px; }
    .sub-title { font-size: 1.2rem; color: #4B5563; margin-bottom: 30px; }
    .stTabs [data-baseweb="tab"] { font-size: 1.1rem; font-weight: 600; }
    </style>
""", unsafe_allow_html=True)

# 3. 사이드바 - 학생 정보 및 API 설정
st.sidebar.title("🎓 학생 프로필 설정")
st.sidebar.markdown("---")

# 학년 및 진로 설정
grade = st.sidebar.selectbox("학년", ["1학년", "2학년", "3학년"])
major_focus = st.sidebar.selectbox("관심 계열", ["인문계열", "사회계열", "자연계열", "공학계열", "의학계열", "예체능계열"])
desired_admission = st.sidebar.selectbox("희망 대입 전형", ["학생부종합", "학생부교과", "정시(수능)", "논술"])

st.sidebar.markdown("---")
st.sidebar.markdown("💡 **AI 컨설팅 기능**을 사용하려면 Streamlit Secrets에 `GEMINI_API_KEY`를 등록하거나 아래에 입력하세요.")

# Secrets 또는 사이드바 직접 입력에서 API 키 로드
api_key = ""
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = st.sidebar.text_input("Gemini API Key 입력", type="password")

# API 키 인증 상태 표시
if api_key:
    st.sidebar.success("🔑 API 키가 연결되었습니다.")
    genai.configure(api_key=api_key)
else:
    st.sidebar.warning("⚠️ AI 기능을 쓰려면 API 키가 필요합니다.")

# 메인 화면 타이틀
st.markdown('<p class="main-title">🎓 스마트 고교 생활 & 대입 매니저</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">나의 주간 시간표를 관리하고 최신 대입 정보와 AI 맞춤형 전략을 받아보세요.</p>', unsafe_allow_html=True)

# 4. 메인 기능 탭 구성
tab1, tab2, tab3 = st.tabs(["📅 나의 시간표", "🎓 대입 핵심 정보", "🤖 AI 대입 전략 컨설턴트"])

# ----------------------------------------------------
# 탭 1: 나의 시간표 관리
# ----------------------------------------------------
with tab1:
    st.header("📅 주간 시간표 관리")
    st.write("나의 일주일 시간표를 확인하고 필요에 따라 수정해보세요.")
    
    # 기본 시간표 데이터 생성
    default_timetable = {
        "교시": [f"{i}교시" for i in range(1, 8)],
        "월요일": ["국어", "수학", "영어", "사회", "과학", "체육", "자율"],
        "화요일": ["수학", "과학", "국어", "영어", "역사", "음악", "동아리"],
        "수요일": ["영어", "국어", "수학", "진로", "사회", "정보기술", "보충"],
        "목요일": ["과학", "사회", "수학", "국어", "영어", "미술", "자치"],
        "금요일": ["국어", "영어", "과학", "사회", "수학", "체육", "종합"]
    }
    df_default = pd.DataFrame(default_timetable)
    
    # 세션 상태를 활용해 시간표 저장 및 편집 가능하게 구현
    if "timetable" not in st.session_state:
        st.session_state.timetable = df_default
        
    # 데이터 편집기 활용 (오류 없는 직관적 수정 가능)
    edited_df = st.data_editor(
        st.session_state.timetable, 
        use_container_width=True, 
        num_rows="fixed"
    )
    st.session_state.timetable = edited_df
    st.success("✨ 시간표는 브라우저 세션에 실시간으로 반영됩니다.")

# ----------------------------------------------------
# 탭 2: 대입 핵심 정보 열람
# ----------------------------------------------------
with tab2:
    st.header("🎓 주요 대입 전형 핵심 요약")
    st.write("목표하는 전형의 핵심 포인트와 준비 전략을 확인하세요.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        with st.expander("📝 1. 학생부교과전형 (내신 중심)", expanded=True):
            st.markdown("""
            * **핵심 요소:** 정량평가된 학교 생활기록부 교과 성적 (내신)
            * **주요 특징
