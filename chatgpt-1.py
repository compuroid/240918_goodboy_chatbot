import streamlit as st
from openai import OpenAI

# 비밀번호 입력 받기
pw = "fdsafdsa2."
if "authenticated" not in st.session_state:
    password = st.text_input("비밀번호를 입력하세요", type="password")
    if password == pw:
        # 사용자가 비밀번호를 올바르게 입력한 경우
        st.session_state["authenticated"] = True
    elif password:
        # 비밀번호가 틀렸을 경우
        st.error("비밀번호가 틀렸습니다.")
        st.stop()
    else:
        # 비밀번호를 입력할 때까지 기다립니다.
        st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = [{"role":"assistant","content":"무엇을 알려드릴까요?"}]


for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.write(m["content"])

if prompt := st.chat_input("질문을 입력하세요"):
    st.session_state.messages.append({"role":"user","content":prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    response = completion.to_dict()["choices"][0]["message"]["content"]
    st.session_state.messages.append({"role":"assistant","content":response})
    with st.chat_message("assistant"):
        st.markdown(response)
