import streamlit as st
from google import genai
from google.genai import types

# 페이지 설정
st.set_page_config(
    page_title="말랑이 거래 챗봇",
    page_icon="🧸",
    layout="centered"
)

st.title("🧸 말랑이 거래 챗봇")
st.caption("Gemini 2.5 Flash-Lite 기반")

# API 키 확인
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    st.error(
        "GEMINI_API_KEY가 설정되지 않았습니다. "
        "Streamlit Secrets를 확인해주세요."
    )
    st.stop()

# Gemini 클라이언트 생성
try:
    client = genai.Client(api_key=api_key)
except Exception as e:
    st.error(f"Gemini 클라이언트 생성 실패: {e}")
    st.stop()

# 채팅 기록 초기화
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "안녕하세요! 🧸\n\n"
                "저는 말랑이 거래 도우미입니다.\n"
                "시세 문의, 거래 팁, 상품 설명 작성 등을 도와드릴 수 있습니다."
            )
        }
    ]

# 기존 대화 출력
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자 입력
prompt = st.chat_input("질문을 입력하세요")

if prompt:
    # 사용자 메시지 저장
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # 대화 이력 구성
            history_text = ""

            for msg in st.session_state.messages:
                role = "사용자" if msg["role"] == "user" else "챗봇"
                history_text += f"{role}: {msg['content']}\n"

            system_prompt = """
당신은 '말랑이 거래 전문 상담사'입니다.

역할:
- 말랑이 거래 관련 질문 답변
- 거래 팁 제공
- 판매글 작성 지원
- 구매자 응대 문구 작성
- 친절하고 간결하게 답변

거래 가격은 실제 시세가 아니라 추정치임을 안내하세요.
"""

            response = client.models.generate_content(
                model="gemini-2.5-flash-lite",
                contents=f"""
{system_prompt}

대화 기록:
{history_text}

현재 질문:
{prompt}
""",
                config=types.GenerateContentConfig(
                    temperature=0.7,
                    max_output_tokens=1024
                )
            )

            answer = response.text

        except Exception as e:
            answer = (
                "⚠️ 오류가 발생했습니다.\n\n"
                f"오류 내용: {str(e)}"
            )

        st.markdown(answer)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )
