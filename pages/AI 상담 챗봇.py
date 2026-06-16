import streamlit as st
import google.generativeai as genai

# 1. 페이지 기본 설정 및 테마
st.set_page_config(
    page_title="에듀케어 AI | 맞춤형 학습 컨설턴트",
    page_icon="📚",
    layout="wide",
)

# 2. API 키 설정 및 예외 처리
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
else:
    st.error("❌ Streamlit Secrets에 'GEMINI_API_KEY'가 설정되지 않았습니다. 배포 설정이나 로컬 .streamlit/secrets.toml을 확인해주세요.")
    st.stop()

# 모델 초기화 (안정적인 gemini-2.5-flash-lite 사용)
try:
    model = genai.GenerativeModel("gemini-2.5-flash-lite")
except Exception as e:
    st.error(f"모델 초기화 중 오류가 발생했습니다: {e}")
    st.stop()

# 3. 사이드바 - 기본 정보 및 동기부여
with st.sidebar:
    st.title("🎓 에듀케어 AI")
    st.subheader("당신만을 위한 맞춤형 학습 코치")
    st.write("---")
    st.markdown(
        """
        **💡 오늘의 공부 명언** *개선한다는 것은 변화하는 것이고, 완벽해진다는 것은 자주 변화하는 것이다.* — 윈스턴 처칠
        """
    )
    st.write("---")
    st.caption("Powered by Gemini 2.5 Flash Lite")

# 4. 메인 화면 타이틀
st.title("📚 AI 학습 상담 및 취약점 분석소")
st.write("과목별 공부 방법부터 오답 분석까지, AI 컨설턴트가 현실적인 액션 플랜을 제안합니다.")

# 5. 탭 구성을 통한 기능 차별화 (학습 상담 vs 오답 분석)
tab1, tab2 = st.tabs(["💡 1:1 과목별 학습 상담소", "🔍 오답 & 취약점 분석기"])

# ==========================================
# TAB 1: 1:1 과목별 학습 상담소
# ==========================================
with tab1:
    st.header("과목별 맞춤 공부법 진단")
    st.write("현재 나의 상황을 선택하면 맞춤형 4주 행동 플랜을 세워드립니다.")

    # 사용자 입력 폼
    with st.form("study_counsel_form"):
        col1, col2 = st.columns(2)
        with col1:
            subject = st.selectbox(
                "🎯 과목을 선택하세요",
                ["국어", "수학", "영어", "한국사", "사회탐구", "과학탐구", "기타(공인시험/자격증)"]
            )
        with col2:
            level = st.selectbox(
                "📈 현재 등급 또는 수준을 선택하세요",
                ["1~2등급 (상위권)", "3~4등급 (중위권)", "5~6등급 (중하위권)", "7등급 이하 (기초부족)", "초보자/노베이스"]
            )

        problem_type = st.radio(
            "❓ 현재 가장 큰 고민은 무엇인가요?",
            [
                "개념은 알겠는데 응용 문제나 4점짜리 문제에 손을 못 대겠어요.",
                "시험 볼 때 항상 시간이 부족해서 뒷부분을 찍어요.",
                "기초 개념 자체가 부족해서 어디서부터 시작해야 할지 모르겠어요.",
                "공부는 열심히 하는 것 같은데 성적이 정체되어 있어요.",
                "벼락치기가 필요한데 효율적인 단기 전략이 필요해요.",
                "기타 (직접 아래의 세부 상황 란에 작성하겠습니다.)"
            ]
        )

        additional_context = st.text_area(
            "📝 추가로 AI 코치에게 알려줄 세부 상황이 있다면 적어주세요 (선택)",
            placeholder="예: 매일 2시간씩 투자할 수 있습니다. 특정 문제집을 풀고 있습니다 등 (고민에서 '기타'를 고르셨다면 여기에 구체적으로 적어주세요!)",
            help="상세히 적을수록 더 구체적인 답변을 얻을 수 있습니다."
        )

        submit_counsel = st.form_submit_button("🚀 맞춤 공부법 컨설팅 받기")

    if submit_counsel:
        with st.spinner("AI 컨설턴트가 유저님의 상황을 분석하여 전략을 짜고 있습니다..."):
            # 프롬프트 엔지니어링 규칙 적용
            prompt = f"""
            [Role]
            당신은 대한민국 최고 권위의 입시 및 학습 코칭 전문가이자, 학생들의 마음을 공감해 주는 따뜻하고 냉철한 AI 학습 컨설턴트입니다.

            [Context]
            학생이 다음과 같은 학습 고민을 가지고 상담을 요청했습니다.
            - 선택 과목: {subject}
            - 현재 수준: {level}
            - 핵심 고민: {problem_type}
            - 추가 상황: {additional_context if additional_context else "없음"}

            [Guidelines]
            1. 절대 뻔하고 추상적인 말(예: "열심히 하세요", "교과서 위주로 보세요")은 하지 마세요. 당장 오늘부터 실행할 수 있는 '행동 중심'의 조언을 하세요.
            2. 학생의 현재 등급에 맞는 현실적인 목표를 설정해 주세요.
            3. 말투는 친절하고 격려하는 어조를 유지하되, 문제점을 지적할 때는 단호하고 정확하게 짚어주세요.

            [Output Format]
            반드시 다음 구조에 맞춰 마크다운(Markdown) 형식으로 한국어로 답변을 출력하세요.
            ### 🎯 1. 현재 상황 분석 및 문제 원인 진단
            ### 🚀 2. 성적 향상을 위한 핵심 학습 전략 (2~3가지)
            ### 📅 3. 당장 시작하는 4주 행동 플랜 (Action Plan)
            - 1~2주차: 
            - 3~4주차: 
            ### 📚 4. 추천하는 학습 접근법 및 활용 팁
            """
            
            try:
                response = model.generate_content(prompt)
                st.success("✨ 맞춤 컨설팅 리포트가 완성되었습니다!")
                st.markdown("---")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"⚠️ AI 답변 생성 중 오류가 발생했습니다: {e}\n잠시 후 다시 시도해 주세요.")

# ==========================================
# TAB 2: 오답 & 취약점 분석기
# ==========================================
with tab2:
    st.header("오답 유형 및 취약점 분석")
    st.write("틀린 문제의 유형, 개념, 혹은 자신이 반복하는 실수 패턴을 입력하시면 해결 방안을 처방해 드립니다.")

    with st.form("wrong_answer_form"):
        wrong_subject = st.selectbox(
            "🎯 과목 선택",
            ["국어", "수학", "영어", "탐구/기타"],
            key="wrong_sub"
        )
        
        wrong_content = st.text_area(
            "❌ 틀린 문제의 유형, 개념 또는 실수 내용을 입력하세요",
            placeholder="예시 1) 수학: 확률과 통계에서 독립시행 확률 문제를 풀 때 조건부 확률 공식이랑 자꾸 헷갈려서 틀려요.\n예시 2) 영어: 빈칸 추론 문제에서 앞부분은 해석이 되는데 선지 3, 4번이 헷갈려서 결국 반대로 찍어서 틀립니다.",
            height=200
        )
        
        submit_wrong = st.form_submit_button("🔍 취약점 진단 및 행동 요령 받기")

    if submit_wrong:
        if not wrong_content.strip():
            st.warning("⚠️ 분석할 오답 내용이나 유형을 입력해 주세요.")
        else:
            with st.spinner("AI가 오답 패턴을 분석하여 교정 행동 요령을 작성 중입니다..."):
                wrong_prompt = f"""
                [Role]
                당신은 인지심리학 및 학습 오류 분석 전문가입니다. 학생이 반복해서 틀리는 문제 유형이나 실수 패턴을 보고 메타인지를 높여줄 솔루션을 제공해야 합니다.

                [Context]
                - 과목: {wrong_subject}
                - 학생이 작성한 오답/실수 내용: {wrong_content}

                [Guidelines]
                1. 학생이 왜 이 부분을 헷갈려하거나 틀리는지 '심리적/개념적 원인'을 예리하게 분석하세요.
                2. 단순히 "개념을 다시 보세요"가 아니라, 오답을 고치기 위한 '구체적인 행동 교정 요령'을 제안하세요.
                3. 같은 실수를 반복하지 않도록 하기 위한 '나만의 오답 노트 작성 팁' 또는 '검토 규칙'을 만들어주세요.

                [Output Format]
                반드시 다음 구조에 맞춰 마크다운(Markdown) 형식으로 한국어로 답변을 출력하세요.
                ### 🔍 1. 왜 자꾸 틀릴까? 원인 정밀 분석
                ### 🛠️ 2. 실수를 박멸하는 구체적 행동 요령 (Action Rule)
                ### 📝 3. 이 유형을 위한 추천 오답 피드백 가이드
                """
                
                try:
                    response = model.generate_content(wrong_prompt)
                    st.success("🔬 오답 분석 및 처방전이 발행되었습니다!")
                    st.markdown("---")
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"⚠️ AI 답변 생성 중 오류가 발생했습니다: {e}\n잠시 후 다시 시도해 주세요.")
