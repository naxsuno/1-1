import streamlit as st

# 1. 페이지 기본 설정 및 디자인 테마 적용
st.set_page_config(
    page_title="공부 상담 & 정보 포털",
    page_icon="🎓",
    layout="centered"
)

# 커스텀 스타일 적용 (가독성 향상)
st.markdown("""
<style>
    .main-title {
        font-size: 32px;
        font-weight: bold;
        color: #1E3A8A;
        margin-bottom: 5px;
    }
    .sub-title {
        font-size: 16px;
        color: #4B5563;
        margin-bottom: 25px;
    }
    .info-card {
        background-color: #F3F4F6;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #3B82F6;
        margin-bottom: 15px;
    }
    .highlight {
        color: #1D4ED8;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# 2. 사이드바 내비게이션
st.sidebar.title("📱 공부 도우미 메뉴")
page = st.sidebar.radio(
    "이동할 페이지를 선택하세요:", 
    [
        "1페이지: 공부 상담소 💬", 
        "2페이지: 학습 스케줄러 📅 (준비 중)", 
        "3페이지: 오답 노트 📝 (준비 중)",
        "4페이지: 학습 꿀팁 & 공부 정보 💡"
    ]
)

# --- 1페이지: 공부 상담소 ---
if page == "1페이지: 공부 상담소 💬":
    st.markdown('<div class="main-title">📚 나만의 AI 공부 상담소</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">학업 스트레스, 성적 고민, 공부 방법 등 무엇이든 적어주세요.</div>', unsafe_allow_html=True)
    
    st.subheader("🔍 나의 고민 접수하기")
    subject = st.selectbox(
        "어떤 과목이 가장 고민이신가요?",
        ["국어", "수학", "영어", "탐구(상경/자연)", "기타/전반적인 공부 습관"]
    )
    
    current_level = st.select_slider(
        "현재 본인의 대략적인 성적 위치를 선택해주세요.",
        options=["기초 부족", "중하위권", "중위권", "상위권", "최상위권"]
    )
    
    user_concern = st.text_area(
        "구체적인 고민을 적어주세요.",
        placeholder="예: 수학 문제 풀 때 시간이 너무 부족해요, 영어 단어가 잘 안 외워져요 등..."
    )
    
    if st.button("🚀 맞춤형 상담 받기"):
        if user_concern.strip() == "":
            st.warning("⚠️ 구체적인 고민 내용을 입력해주셔야 정확한 상담이 가능해요!")
        else:
            with st.spinner("당신의 고민을 분석하여 맞춤 솔루션을 생성 중입니다..."):
                st.success("🎉 상담 분석이 완료되었습니다!")
                st.markdown("### 💡 추천 학습 솔루션")
                st.write(f"**📍 분석 대상 과목:** {subject} ({current_level} 수준)")
                st.info(f"**🤔 작성하신 고민:** {user_concern}")
                st.markdown("---")
                st.markdown("#### 🛠️ 행동 가이드라인")
                if current_level in ["기초 부족", "중하위권"]:
                    st.write("1. **개념 위주의 학습:** 문제 풀이보다는 교과서나 기본서의 개념을 완벽히 이해하는 것이 먼저입니다.")
                    st.write("2. **작은 목표 설정:** 하루에 핵심 개념 2개씩 확실하게 마스터하는 습관을 들여보세요.")
                else:
                    st.write("1. **취약 유형 분석:** 오답 노트를 활용해 자주 틀리는 패턴을 파악하고 집중 공략하세요.")
                    st.write("2. **실전 감각 기르기:** 타이머를 맞춰두고 실제 시험처럼 시간을 배분하는 연습이 필요합니다.")

# --- 2페이지, 3페이지 임시 화면 ---
elif page == "2페이지: 학습 스케줄러 📅 (준비 중)":
    st.title("📅 학습 스케줄러")
    st.info("이 페이지는 현재 준비 중입니다. 매일의 공부 계획을 세우고 타이머를 돌려 공부 시간을 기록하는 공간이 될 예정입니다.")

elif page == "3페이지: 오답 노트 📝 (준비 중)":
    st.title("📝 오답 노트")
    st.info("이 페이지는 현재 준비 중입니다. 틀린 문제를 사진으로 올리거나 텍스트로 적어두고 주기적으로 복습할 수 있는 기능이 제공됩니다.")

# --- 4페이지: 학습 꿀팁 & 공부 정보 ---
elif page == "4페이지: 학습 꿀팁 & 공부 정보 💡":
    st.markdown('<div class="main-title">💡 학습 꿀팁 & 공부 정보</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">뇌과학이 증명한 공부법부터 과목별 팁까지 유용한 학습 정보를 탐색해보세요.</div>', unsafe_allow_html=True)

    # 탭(Tab) 구조를 사용하여 카테고리별 깔끔한 정보 제공
    tab1, tab2, tab3 = st.tabs(["🧠 뇌과학적 공부법", "📚 과목별 핵심 공략", "🎯 내 성향 매칭 공부법"])

    with tab1:
        st.subheader("인간의 뇌가 가장 선호하는 4가지 학습 이론")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            <div class="info-card">
                <span class="highlight">1. 액티브 리콜 (Active Recall)</span><br>
                단순히 책을 눈으로 여러 번 읽는 것은 '아는 것 같은 착각'을 줍니다. 책을 덮고 흰 종이에 기억나는 내용을 직접 써보거나, 자신에게 질문을 던져 머릿속에서 강제로 인출(Recall)해내는 과정이 기억을 장기화하는 가장 빠른 지름길입니다.
            </div>
            <div class="info-card">
                <span class="highlight">2. 간격 반복 (Spaced Repetition)</span><br>
                에빙하우스의 망각곡선에 따르면 인간은 학습 후 하루만 지나도 절반 이상의 정보를 잊어버립니다. 이를 방지하기 위해 <b>1일 뒤, 3일 뒤, 7일 뒤, 14일 뒤</b>로 복습 주기를 점진적으로 넓혀가며 반복하는 방법이 효율적입니다.
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.markdown("""
            <div class="info-card">
                <span class="highlight">3. 파인만 기법 (Feynman Technique)</span><br>
                노벨 물리학상 수상자 리처드 파인만이 고안한 방법입니다. 자신이 공부한 핵심 개념을 <b>아무것도 모르는 초등학생에게 설명하듯이 아주 쉬운 언어로 설명</b>해 보는 것입니다. 막히는 부분이 생긴다면 그 부분이 바로 내가 아직 정확히 이해하지 못한 공백입니다.
            </div>
            <div class="info-card">
                <span class="highlight">4. 뽀모도로 기법 (Pomodoro Technique)</span><br>
                집중력이 지속되지 않을 때는 시간관리가 핵심입니다. <b>25분 동안 휴대폰을 멀리하고 극도로 집중해서 공부한 뒤, 5분 동안 완전히 쉬는 것</b>을 한 세트로 삼으세요. 이 과정을 4번 반복한 후에는 15~20분 동안 깊은 휴식을 취합니다.
            </div>
            """, unsafe_allow_html=True)

    with tab2:
        st.subheader("과목별 성적 향상을 위한 핵심 한마디")
        
        subject_tabs = st.radio("과목을 선택하세요:", ["국어", "수학", "영어", "탐구"], horizontal=True)
        
        if subject_tabs == "국어":
            st.success("✍️ **국어 공략법: 문해력과 메타인지**")
            st.write("- **비문학(독서):** 양치기식 풀이보다는 지문 한 개를 풀더라도 문장 간의 유기적 흐름과 단락별 핵심 주제를 완벽히 요약하는 연습이 필요합니다.")
            st.write("- **문학:** 주관적인 감상을 철저히 배제하고, 철저히 지문 내의 단어와 객관적인 근거만을 토대로 선지를 골라내야 오류를 줄일 수 있습니다.")
        
        elif subject_tabs == "수학":
            st.success("📐 **수학 공략법: 유기적인 단원 연결과 오답 정복**")
            st.write("- **개념의 시각화:** 공식만 외우기보다는 '왜 이 공식이 도출되었는가?'에 집중하여 유도 과정을 손으로 직접 증명해 보세요.")
            st.write("- **집요한 오답노트:** 똑같은 실수를 반복하지 않는 것이 수학 점수를 올리는 지름길입니다. 틀린 문항은 3일 후에 아무 도움 없이 처음부터 끝까지 혼자 힘으로 풀어낼 수 있을 때까지 반복하세요.")
            
        elif subject_tabs == "영어":
            st.success("🔤 **영어 공략법: 문맥적 단어 암기와 구조 독해**")
            st.write("- **문맥 암기:** 영어 단어를 한글 1:1 매칭으로 외우기보다, 예문 속에서 이 단어가 어떤 느낌과 뉘앙스로 쓰이는지 문맥적으로 습득해야 실전 독해에서 막히지 않습니다.")
            st.write("- **구문 분석:** 하루에 5문장이라도 복잡한 3~4줄짜리 긴 문장을 완벽히 구문 분석(주어, 동사, 목적어, 수식어 수식 관계 파악)하는 훈련을 하세요.")
            
        elif subject_tabs == "탐구":
            st.success("🧪 **탐구 공략법: 단원별 마인드맵과 키워드 정리**")
            st.write("- **개념 단권화:** 백지에 대단원과 소단원의 뼈대를 그리고, 그에 따른 핵심 키워드들을 마인드맵 형태로 채워나가는 단권화 작업을 시도해보세요.")
            st.write("- **기출 선택지 분석:** 탐구 영역은 자주 출제되는 기출의 오답 선지와 정답 선지 패턴이 명확합니다. 선지별 키워드 정리를 철저히 해 두세요.")

    with tab3:
        st.subheader("🎯 간단 자가 테스트: 내게 맞는 최적의 공부법은?")
        
        st.write("요즘 나의 공부 습관에 대한 상태를 체크하고 어울리는 솔루션을 받아보세요.")
        
        state_q = st.selectbox(
            "요즘 공부할 때 가장 가깝게 느끼는 상태를 골라주세요.",
            [
                "공부하려고 책상에 앉아도 10분 만에 집중이 흐트러지고 딴짓을 해요.",
                "열심히 공부해서 외운 것 같은데 시험지만 보면 백지가 돼요.",
                "내가 이 개념을 완벽하게 알고 있는 건지 아닌지 불안해요."
            ]
        )
        
        if st.button("추천 처방전 보기"):
            if "10분 만에 집중" in state_q:
                st.info("💡 **추천 처방전: 뽀모도로 기법**\n\n한 번에 길게 공부하려다 보니 뇌가 거부감을 느끼는 상태입니다. 타이머를 켜고 딱 25분만 스마트폰을 비행기 모드로 해 둔 뒤 초집중해 보세요! 5분의 꿀맛 같은 휴식이 뇌에 성취감을 주어 하루 집중 시간을 극대화할 수 있습니다.")
            elif "시험지만 보면 백지" in state_q:
                st.info("💡 **추천 처방전: 간격 반복 & 인출 연습**\n\n눈으로만 훑어보거나 밑줄만 치는 공부는 뇌에 장기 기억으로 남지 않습니다. 매일 전날 공부한 내용을 백지에 5분간 핵심만 적어보는 '백지 복습'을 실천하시고, 1일, 3일, 7일 주기로 다시 들여다보세요.")
            elif "개념을 완벽하게 알고 있는 건지" in state_q:
                st.info("💡 **추천 처방전: 파인만 기법**\n\n내가 아는지 모르는지 헷갈릴 때는 가상의 학생이나 인형을 앞에 두고 내가 방금 배운 개념을 칠판에 적으며 소리 내어 가르치듯 설명해 보세요. 말문이 막히거나 막연하게 뭉뚱그려 설명하는 부분이 바로 '내가 모르는 취약한 지점'입니다.")
