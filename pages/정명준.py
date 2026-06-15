import streamlit as tf  # Streamlit 라이브러리 가져오기

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="공부 상담소 (Study Counseling)",
    page_icon="📚",
    layout="centered"
)

# 2. 사이드바 - 향후 2, 3페이지 이동을 위한 네비게이션 틀
st.sidebar.title("📱 메뉴")
page = st.sidebar.radio("이동할 페이지를 선택하세요:", ["1페이지: 공부 상담소", "2페이지: 준비 중", "3페이지: 준비 중"])

# --- 1페이지: 공부 상담소 기능 구현 ---
if page == "1페이지: 공부 상담소":
    
    # 헤더 구역
    st.title("📚 나만의 AI 공부 상담소")
    st.write("학업 스트레스, 성적 고민, 공부 방법 등 무엇이든 이야기해보세요. 당신의 학습 메이트가 되어드릴게요!")
    st.markdown("---")
    
    # 사용자 입력 구역
    st.subheader("🔍 나의 고민 접수하기")
    
    # 과목 선택
    subject = st.selectbox(
        "어떤 과목이 가장 고민이신가요?",
        ["국어", "수학", "영어", "탐구(상경/자연)", "기타/전반적인 공부 습관"]
    )
    
    # 현재 상태/성적대 선택
    current_level = st.select_slider(
        "현재 본인의 대략적인 성적 위치를 선택해주세요.",
        options=["기초 부족", "중하위권", "중위권", "상위권", "최상위권"]
    )
    
    # 구체적인 고민 작성
    user_concern = st.text_area(
        "구체적인 고민을 적어주세요. (예: 수학 문제 풀 때 시간이 너무 부족해요, 영어 단어가 안 외워져요 등)",
        placeholder="여기에 내용을 입력하세요..."
    )
    
    # 상담 신청 버튼
    if st.button("🚀 맞춤형 상담 받기"):
        if user_concern.strip() == "":
            st.warning("⚠️ 구체적인 고민 내용을 입력해주셔야 정확한 상담이 가능해요!")
        else:
            with st.spinner("당신의 고민을 분석하여 맞춤 솔루션을 생성 중입니다..."):
                # 실제 AI API(OpenAI 등)를 연동하기 전까지 사용할 임시 피드백 로직입니다.
                st.success("🎉 상담 분석이 완료되었습니다!")
                
                st.markdown("### 💡 추천 학습 솔루션")
                st.write(f"**📍 분석 대상 과목:** {subject} ({current_level} 수준)")
                
                # 간단한 조건문 기반 피드백 예시
                st.info(f"**🤔 작성하신 고민:** {user_concern}")
                
                st.markdown("---")
                st.markdown("#### 🛠️ 행동 가이드라인")
                if current_level in ["기초 부족", "중하위권"]:
                    st.write("1. **개념 위주의 학습:** 문제 풀이보다는 교과서나 기본서의 개념을 완벽히 이해하는 것이 먼저입니다.")
                    st.write("2. **작은 목표 설정:** 하루에 핵심 개념 2개씩 확실하게 마스터하는 습관을 들여보세요.")
                else:
                    st.write("1. **취약 유형 분석:** 오답 노트를 활용해 자주 틀리는 패턴을 파악하고 집중 공략하세요.")
                    st.write("2. **실전 감각 기르기:** 타이머를 맞춰두고 실제 시험처럼 시간을 배분하는 연습이 필요합니다.")

# --- 2, 3페이지 임시 화면 ---
elif page == "2페이지: 준비 중":
    st.title("🚧 2페이지 준비 중")
    st.write("여기에 두 번째 기능을 구현할 예정입니다. (예: 스케줄러, 오답노트 등)")

elif page == "3페이지: 준비 중":
    st.title("🚧 3페이지 준비 중")
    st.write("여기에 세 번째 기능을 구현할 예정입니다. (예: 커뮤니티, 성적 통계 등)")
