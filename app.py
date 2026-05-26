import streamlit as st
import pandas as pd
from datetime import date

# 제목
st.title("📚 수행평가 관리 앱")

# 세션 상태 초기화
if "tasks" not in st.session_state:
    st.session_state.tasks = []

# 입력 영역
st.header("수행평가 추가")

task_date = st.date_input("날짜 선택", value=date.today())
subject = st.text_input("과목")
task = st.text_input("수행평가 내용")

# 추가 버튼
if st.button("추가하기"):

    if subject and task:
        st.session_state.tasks.append({
            "날짜": task_date,
            "과목": subject,
            "내용": task
        })

        st.success("추가 완료!")

    else:
        st.warning("과목과 내용을 입력하세요.")

# 목록 출력
st.header("📅 수행평가 일정")

if st.session_state.tasks:

    df = pd.DataFrame(st.session_state.tasks)

    df = df.sort_values(by="날짜")

    st.dataframe(df, use_container_width=True)

else:
    st.info("아직 등록된 수행평가가 없습니다.")
