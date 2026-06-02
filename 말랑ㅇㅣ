import streamlit as st
from google import genai
from google.genai import types

# -----------------------------
# 페이지 설정
# -----------------------------
st.set_page_config(
    page_title="말랑이 챗봇",
    page_icon="🐾",
    layout="centered"
)

st.title("🐾 말랑이 챗봇")
st.caption("Gemini 2.5 Flash-Lite 기반")

# -----------------------------
# API 키 확인
# -----------------------------
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    st.error(
        "GEMINI_API_KEY가 설정되지 않았습니다. "
        "Streamlit Secrets를 확인하세요."
    )
    st.stop()

# -----------------------------
# Gemini 클라이언트 생성
# -----------------------------
try:
    client = genai.Client(api_key=api_key)
except Exception as e:
    st.error(f"Gemini 클라이언트 생성 실패: {e}")
    st.stop()

# -----------------------------
# 채팅 기록 초기화
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "안녕! 나는 말랑이에 대해 이야기하는 "
                "말랑이 챗봇이야 🐾\n\n"
                "말랑이의 특징, 종류, 이야기, 설정 등을 물어봐!"
            ),
        }
    ]

# -----------------------------
# 기존 대화 표시
# -----------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# -----------------------------
# 사용자 입력
# -----------------------------
prompt = st.chat_input("말랑이에 대해 물어보세요")

if prompt:
    # 사용자 메시지 저장
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # Gemini 대화 형식 변환
        contents = []

        system_prompt = """
        너는 '말랑이' 전문 챗봇이다.

        규칙:
        - 항상 친절하게 답변한다.
        - 말랑이에 관한 질문을 우선적으로 다룬다.
        - 모르는 내용은 추측하지 말고 솔직히 모른다고 말한다.
        - 답변은 한국어로 한다.
        """

        contents.append(
            types.Content(
                role="user",
                parts=[types.Part(text=system_prompt)]
            )
        )

        for msg in st.session_state.messages:
            role = "model" if msg["role"] == "assistant" else "user"

            contents.append(
                types.Content(
                    role=role,
                    parts=[types.Part(text=msg["content"])]
                )
            )

        with st.chat_message("assistant"):
            with st.spinner("생각 중..."):
                response = client.models.generate_content(
                    model="gemini-2.5-flash-lite",
                    contents=contents,
                )

                answer = response.text

                st.markdown(answer)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

    except Exception as e:
        error_msg = (
            "죄송해요. 응답을 생성하는 중 오류가 발생했어요.\n\n"
            f"오류 내용: {e}"
        )

        with st.chat_message("assistant"):
            st.error(error_msg)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": error_msg
            }
        )

# -----------------------------
# 대화 초기화 버튼
# -----------------------------
st.divider()

if st.button("대화 초기화"):
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "안녕! 나는 말랑이 챗봇이야 🐾\n\n"
                "새로운 대화를 시작해보자!"
            ),
        }
    ]
    st.rerun()
