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

# 4. 사이드바 - 누적 데이터 시각화 (차별화 기능)
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
        subject_counts = df["과목"].value_value_counts()
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
with st.form("wrong_answer_form_v2"):
    col1, col2 = st.columns([1, 2])
    
    with col1:
        wrong_subject = st.selectbox(
            "🎯 과목을 선택하세요",
            ["국어", "수학", "영어", "한국사", "사회탐구", "과학탐구", "기타"]
        )
        
        # 차별화 기능: 실수 태그 선택 (Multi-select)
        error_tags = st.multiselect(
            "🏷️ 이번 실수의 원인 태그 (중복 선택 가능)",
            ["단순 계산/마킹 실수", "개념/공식 기억 안 남", "문제의 조건을 잘못 읽음", "시간 부족으로 찍음", "매력적인 오답 선지에 낚임", "지문 독해 능력 부족"],
            default=["개념/공식 기억 안 남"]
        )
        
    with col2:
        wrong_content = st.text_area(
            "❌ 틀린 문제의 구체적인 상황이나 헷갈린 점을 적어주세요",
            placeholder="예시: 수학 기출문제를 푸는데 조건부 확률 공식이랑 독립시행 확률 공식이 머릿속에서 꼬여서 엄두를 못 냈습니다. 결국 계산도 하기 전에 포기했어요.",
            height=150
        )
    
    submit_wrong = st.form_submit_button("🔍 AI 취약점 진단 및 처방전 받기")

# 7. AI 분석 및 결과 출력
if submit_wrong:
    if not wrong_content.strip():
        st.warning("⚠️ 분석할 오답 내용이나 유형을 입력해 주세요.")
    else:
        with st.spinner("AI가 오답 패턴을 분석하여 처방전을 작성 중입니다..."):
            
            # 세션 상태에 과목 기록 추가 (좌측 그래프 업데이트용)
            st.session_state["wrong_history"].append(wrong_subject)
            
            # 태그를 문자열로 변환하여 프롬프트에 주입
            tags_str = ", ".join(error_tags) if error_tags else "없음"
            
            wrong_prompt = f"""
            [Role]
            당신은 인지심리학 및 학습 오류 분석 전문가입니다. 학생이 반복해서 틀리는 문제 유형이나 실수 패턴을 보고 메타인지를 높여줄 솔루션을 제공해야 합니다.

            [Context]
            - 과목: {wrong_subject}
            - 학생이 선택한 실수 태그: {tags_str}
            - 학생이 작성한 구체적 오답 내용: {wrong_content}

            [Guidelines]
            1. 학생이 선택한 [실수 태그]와 [오답 내용]을 연결 지어 왜 이 부분을 헷갈려하거나 틀리는지 '심리적/개념적 원인'을 예리하게 분석하세요.
            2. 다음 시험이나 문제 풀이 시 즉시 적용할 수 있는 '구체적인 행동 교정 요령(Action Rule)'을 제안하세요.
            3. 같은 실수를 반복하지 않도록 하기 위한 이 유형 전용 '오답 피드백 체크리스트'를 만들어주세요.

            [Output Format]
            반드시 다음 구조에 맞춰 마크다운(Markdown) 형식으로 한국어로 답변을 출력하세요.
            ### 🔍 1. 왜 자꾸 틀릴까? 원인 정밀 분석
            ### 🛠️ 2. 실수를 박멸하는 구체적 행동 요령 (Action Rule)
            ### 📝 3. 이 유형을 위한 추천 오답 피드백 가이드
            """
            
            try:
                response = model.generate_content(wrong_prompt)
                analysis_result = response.text
                
                st.success("🔬 AI 오답 처방전이 발행되었습니다! (좌측 사이드바에 통계가 반영되었습니다.)")
                st.markdown("---")
                st.markdown(analysis_result)
                
                # 차별화 기능: 결과 다운로드 버튼 추가
                st.markdown("---")
                st.download_button(
                    label="📥 AI 오답 처방전 다운로드 (.txt)",
                    data=analysis_result,
                    file_name=f"AI_오답처방전_{wrong_subject}.txt",
                    mime="text/plain"
                )
                
            except Exception as e:
                st.error(f"⚠️ AI 답변 생성 중 오류가 발생했습니다: {e}")
