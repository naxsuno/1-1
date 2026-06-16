import streamlit as st
import google.generativeai as genai

# 1. 페이지 기본 설정 및 테마
st.set_page_config(
    page_title="메타노트 AI | AI 오답 분석기",
    page_icon="📝",
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

# 3. 사이드바 - 메타인지 가이드 및 동기부여
with st.sidebar:
    st.title("📝 메타노트 AI")
    st.subheader("실수를 실력으로 바꾸는 시간")
    st.write("---")
    st.markdown(
        """
        **💡 메타인지 학습법**
        틀린 문제를 단순히 '실수'로 넘기면 다음 시험에서 똑같이 틀립니다. 
        AI와 함께 **내가 왜 틀렸는지** 근본적인 인지 과정을 분석해 보세요.
        """
    )
    st.write("---")
    st.caption("Powered by Gemini 2.5 Flash Lite")

# 4. 메인 화면 타이틀 및 설명
st.title("🔍 AI 오답 유형 및 취약점 분석기")
st.write("틀린 문제의 유형, 헷갈렸던 개념, 혹은 자주 반복하는 실수 패턴을 입력하시면 AI가 맞춤형 처방전을 발행해 드립니다.")
st.markdown("---")

# 5. 오답 입력 폼 (단일 메인 기능으로 집중)
with st.form("wrong_answer_form"):
    col1, col2 = st.columns([1, 3])
    
    with col1:
        wrong_subject = st.selectbox(
            "🎯 과목을 선택하세요",
            ["국어", "수학", "영어", "한국사", "사회탐구", "과학탐구", "기타(공인시험/자격증)"]
        )
        
        st.info(
            "💡 **작성 팁:**\n"
            "단순히 '수학 5번 틀림' 보다는 "
            "'어떤 개념과 헷갈렸는지', "
            "'선지 중에 무엇과 고민했는지' "
            "상세히 적을수록 분석이 정확해집니다."
        )
    
    with col2:
        wrong_content = st.text_area(
            "❌ 틀린 문제의 유형, 헷갈린 개념 또는 실수 내용을 입력하세요",
            placeholder="예시 1) 수학: 확률과 통계에서 독립시행 확률 문제를 풀 때 조건부 확률 공식이랑 자꾸 헷갈려서 틀려요.\n\n"
                        "예시 2) 영어: 빈칸 추론 문제에서 앞부분은 해석이 잘 되는데, 뒷부분 매력적인 오답 선지 3번과 4번이 헷갈려서 결국 반대로 찍어서 틀립니다.\n\n"
                        "예시 3) 국어: 과학 기술 지문에서 정보량이 많아지면 밑줄 친 인과관계를 놓치고 주관적인 직관으로 문제를 풀다 틀려요.",
            height=230
        )
    
    # 제출 버튼
    submit_wrong = st.form_submit_button("🔍 AI 취약점 진단 및 행동 요령 받기")

# 6. AI 분석 및 결과 출력
if submit_wrong:
    if not wrong_content.strip():
        st.warning("⚠️ 분석할 오답 내용이나 유형을 입력해 주세요.")
    else:
        with st.spinner("AI가 오답 패턴을 정밀 분석하여 맞춤형 처방전을 작성 중입니다..."):
            wrong_prompt = f"""
            [Role]
            당신은 인지심리학 및 학습 오류 분석 전문가입니다. 학생이 반복해서 틀리는 문제 유형이나 실수 패턴을 보고 메타인지를 높여줄 솔루션을 제공해야 합니다.

            [Context]
            - 과목: {wrong_subject}
            - 학생이 작성한 오답/실수 내용: {wrong_content}

            [Guidelines]
            1. 학생이 왜 이 부분을 헷갈려하거나 틀리는지 '심리적/개념적 원인'을 날카롭고 예리하게 분석하세요.
            2. 단순히 "개념을 다시 보세요" 같은 추상적인 조언은 배제하고, 다음 시험이나 문제 풀이 시 즉시 적용할 수 있는 '구체적인 행동 교정 요령'을 제안하세요.
            3. 같은 실수를 반복하지 않도록 하기 위한 이 유형 전용 '오답 피드백 규칙' 또는 '검토 규칙'을 만들어주세요.

            [Output Format]
            반드시 다음 구조에 맞춰 마크다운(Markdown) 형식으로 한국어로 답변을 출력하세요.
            ### 🔍 1. 왜 자꾸 틀릴까? 원인 정밀 분석
            - 학생의 입력 내용을 바탕으로 한 인지적 오류 및 약점 진단

            ### 🛠️ 2. 실수를 박멸하는 구체적 행동 요령 (Action Rule)
            - 문제를 풀 때 행동 지침 (예: ~하는 순간, 손을 멈추고 ~를 적을 것)

            ### 📝 3. 이 유형을 위한 추천 오답 피드백 가이드
            - 다음 번에 유사 문제를 만났을 때 검토해야 할 체크리스트 문항 제공
            """
            
            try:
                response = model.generate_content(wrong_prompt)
                st.success("🔬 AI 오답 처방전이 발행되었습니다!")
                st.markdown("---")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"⚠️ AI 답변 생성 중 오류가 발생했습니다: {e}\n잠시 후 다시 시도해 주세요.")
