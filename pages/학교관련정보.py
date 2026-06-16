import streamlit as st
import pandas as pd

# 1. 페이지 설정
st.set_page_config(
    page_title="고교 생활 & 대입 매니저",
    page_icon="🎓",
    layout="wide"
)

# 2. 사이드바 설정 (오류 가능성 원천 차단)
st.sidebar.title("🎓 학생 프로필")
grade = st.sidebar.selectbox("학년", ["1학년", "2학년", "3학년"])
major_focus = st.sidebar.selectbox("관심 계열", ["인문사회", "자연공학", "의학생명", "예체능"])
desired_admission = st.sidebar.selectbox("희망 전형", ["학생부종합", "학생부교과", "정시(수능)", "논술"])

# API 키 확인 (오류가 나지 않도록 안전하게 가져오기)
api_key = st.sidebar.text_input("Gemini API Key (선택사항)", type="password", help="AI 기능을 쓰려면 입력하세요.")
if not api_key and "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]

# 3. 메인 타이틀
st.title("🎓 고교 생활 & 대입 매니저")
st.caption("안정적으로 작동하는 학업 관리 및 입시 정보 대시보드입니다.")

# 4. 탭 구성
tab1, tab2, tab3 = st.tabs(["📅 나의 시간표", "🎓 대입 핵심 정보", "🤖 AI 간단 컨설팅"])

# ----------------------------------------------------
# 탭 1: 나의 시간표 (가장 안정적인 Pandas 데이터프레임 구조)
# ----------------------------------------------------
with tab1:
    st.header("📅 주간 시간표 관리")
    st.write("아래 표의 셀을 더블클릭하여 시간표를 자유롭게 수정할 수 있습니다.")
    
    # 고정된 형태의 데이터프레임 생성
    if "timetable_df" not in st.session_state:
        st.session_state.timetable_df = pd.DataFrame({
            "교시": [f"{i}교시" for i in range(1, 8)],
            "월요일": ["국어", "수학", "영어", "사회", "과학", "체육", "자율"],
            "화요일": ["수학", "과학", "국어", "영어", "역사", "음악", "동아리"],
            "수요일": ["영어", "국어", "수학", "진로", "사회", "정보", "보충"],
            "목요일": ["과학", "사회", "수학", "국어", "영어", "미술", "자치"],
            "금요일": ["국어", "영어", "과학", "사회", "수학", "체육", "종합"]
        })
    
    # st.data_editor를 사용하여 오류 없는 편집 환경 제공
    edited_df = st.data_editor(st.session_state.timetable_df, use_container_width=True, hide_index=True)
    st.session_state.timetable_df = edited_df

# ----------------------------------------------------
# 탭 2: 대입 핵심 정보 (100% 텍스트 기반으로 오류 제로)
# ----------------------------------------------------
with tab2:
    st.header("🎓 주요 대입 전형 요약")
    
    col1, col2 = st.columns(2)
    with col1:
        with st.expander("📝 학생부교과전형", expanded=True):
            st.markdown("- **중심 요소:** 내신 성적 (정량평가)\n- **핵심 포인트:** 수능 최저학력기준 충족 여부가 합격의 열쇠입니다.")
        with st.expander("🎯 학생부종합전형", expanded=True):
            st.markdown("- **중심 요소:** 내신 + 학생부 기록 (세특, 창체 등)\n- **핵심 포인트:** 지원 학과와 관련된 주도적인 탐구 활동이 필요합니다.")
            
    with col2:
        with st.expander("✍️ 논술전형", expanded=True):
            st.markdown("- **중심 요소:** 대학별 논술고사\n- **핵심 포인트:** 내신 영향력은 적지만 경쟁률이 매우 높고 수능 최저가 있는 경우가 많습니다.")
        with st.expander("✏️ 정시전형 (수능 위주)", expanded=True):
            st.markdown("- **중심 요소:** 수능 성적 100%\n- **핵심 포인트:** 영역별 반영 비율(가중치)을 확인하여 전략적으로 취약점을 보완해야 합니다.")

# ----------------------------------------------------
# 탭 3: AI 간단 컨설팅 (완벽한 예외처리 적용)
# ----------------------------------------------------
with tab3:
    st.header("🤖 AI 대입 전략 컨설팅")
    
    current_gpa = st.text_input("현재 내신 등급 (예: 2.5)", placeholder="2.5")
    dream_major = st.text_input("희망 학과 (예: 컴퓨터공학과)", placeholder="컴퓨터공학과")
    
    if st.button("🚀 AI 분석 요청하기"):
        if not api_key:
            st.error("⚠️ 사이드바에 Gemini API Key를 입력하거나 Streamlit Secrets에 등록해주세요. (키가 없으면 AI 기능을 사용할 수 없습니다.)")
        elif not current_gpa or not dream_major:
            st.warning("⚠️ 내신 등급과 희망 학과를 모두 입력해주세요.")
        else:
            with st.spinner("AI 분석 중... (라이브러리 로딩 및 연결 중)"):
                try:
                    # 패키지 임포트 오류를 원천 차단하기 위해 함수 내부에서 안전하게 로드
                    import google.generativeai as genai
                    
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel("gemini-2.5-flash-lite")
                    
                    prompt = f"""
                    고등학교 {grade} {major_focus} 계열 학생입니다. 희망 전형은 {desired_admission}입니다.
                    현재 내신 등급은 {current_gpa} 이며, 희망 학과는 {dream_major}입니다.
                    이 학생에게 딱 맞는 입시 조언을 3줄로 요약해서 친절하게 제공해주세요.
                    """
                    
                    response = model.generate_content(prompt)
                    
                    st.success("📋 AI 분석 완료!")
                    st.info(response.text)
                    
                except ImportError:
                    st.error("❌ 시스템 오류: `google-generativeai` 라이브러리가 정상적으로 설치되지 않았습니다. requirements.txt를 확인해주세요.")
                except Exception as e:
                    st.error(f"❌ API 호출 실패: 입력하신 API Key가 잘못되었거나 서버 통신에 실패했습니다. (원인: {e})")
