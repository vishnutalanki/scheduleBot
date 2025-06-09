import streamlit as st
import requests

st.set_page_config(page_title="Rowan Student Schedule Assistant", page_icon="🎓", layout="centered")
st.title("🎓 Ro - Smart Schedule Assistant")

# Session state initialization
if "student_id" not in st.session_state:
    st.session_state.student_id = None
if "messages" not in st.session_state:
    st.session_state.messages = []

# Login block
if not st.session_state.student_id:
    st.header("Login")
    student_id_input = st.text_input("Enter your Student ID", key="login_input")
    if st.button("Login"):
        if student_id_input.strip():
            response = requests.post("http://127.0.0.1:8000/login", json={"student_id": student_id_input.strip()})
            if response.status_code == 200:
                st.session_state.student_id = student_id_input.strip()
                st.rerun()  # 💡 Trigger script rerun to show the Q&A section right away
            else:
                st.error("Invalid student ID. Please try again.")
        else:
            st.warning("Please enter a valid Student ID.")
    st.stop()

# Logged-in state
st.caption(f"Logged in as :green[{st.session_state.student_id}]")
st.subheader("Ask me anything about your schedule 🗓️")

question = st.text_input("Your question", key="question_input")
if st.button("Ask"):
    if question.strip():
        payload = {
            "student_id": st.session_state.student_id,
            "message": question.strip()
        }
        response = requests.post("http://127.0.0.1:8000/response", json=payload)
        if response.status_code == 200:
            answer = response.json()["answer"]
            st.session_state.messages.append(("user", question.strip()))
            st.session_state.messages.append(("bot", answer))
        else:
            st.error(response.json()["detail"])
    else:
        st.warning("Please enter a valid question.")

# Display message history (latest or full)
if st.session_state.messages:
    show_all = st.checkbox("Show full chat history", value=False)

    if not show_all:
        messages_to_display = st.session_state.messages[-2:]
    else:
        messages_to_display = st.session_state.messages

    for role, msg in messages_to_display:
        if role == "user":
            st.markdown(f"🧑‍🎓 **You**: {msg}")
        else:
            st.markdown(f"🤖 **Ro**: {msg}")