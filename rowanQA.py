import streamlit as st
import requests

st.set_page_config(page_title="Rowan Schedule Assistant", page_icon="🎓")
st.title("🎓 Rowan Schedule Assistant")
st.markdown("---")

# --- Session state for login ---
if "student_id" not in st.session_state:
    st.session_state.student_id = None

# --- Login Block ---
# --- Login Block ---
if not st.session_state.student_id:
    st.subheader("Login")
    student_id = st.text_input("Enter your Student ID")

    if st.button("Login"):
        if not student_id.strip():
            st.warning("Please enter a valid Student ID.")
        else:
            response = requests.post("http://localhost:8000/login", json={"student_id": student_id})
            if response.status_code == 200:
                st.session_state.student_id = student_id
                st.success("Logged in successfully! You can now ask a question below 👇")
            else:
                st.error(response.json().get("detail", "Login failed."))
    st.stop()

# --- Chat Interface (only visible after login) ---
st.markdown("---")
st.caption(f"Logged in as `{st.session_state.student_id}`")
st.subheader("Ask me anything about your schedule 📅")

query = st.text_input("Your question")

if st.button("Ask"):
    if not query.strip():
        st.warning("Please enter a question.")
    elif not st.session_state.get("student_id"):
        st.error("You're not logged in. Please enter your student ID above.")
    else:
        try:
            res = requests.post("http://localhost:8000/response", json={
                "student_id": st.session_state.student_id,
                "message": query
            })
            if res.status_code == 200:
                st.success("✅ Answer:")
                st.write(f"🤖: {res.json()['answer']}")
            else:
                st.error(res.json().get("detail", "Something went wrong."))
        except Exception as e:
            st.error(f"Request failed: {str(e)}")