import streamlit as st
from conversation import (
    get_greeting_message,
    get_closing_message,
    generate_technical_questions,
    is_exit_message
)

# ---------------- Page Config ----------------
st.set_page_config(
    page_title="TalentScout Hiring Assistant",
    page_icon="🤖",
    layout="centered"
)

# ---------------- Styling ----------------
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(180deg, #0f2027, #203a43, #2c5364);
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🤖 TalentScout Hiring Assistant")
st.caption("AI-powered initial candidate screening")

# ---------------- Session State ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "step" not in st.session_state:
    st.session_state.step = 0

if "candidate_data" not in st.session_state:
    st.session_state.candidate_data = {}

if "field_index" not in st.session_state:
    st.session_state.field_index = 0

FIELDS = [
    "Full Name",
    "Email Address",
    "Phone Number",
    "Years of Experience",
    "Desired Position(s)",
    "Current Location"
]

# ---------------- Greeting (ONCE) ----------------
if st.session_state.step == 0:
    st.session_state.messages.append(
        {"role": "assistant", "content": get_greeting_message()}
    )
    st.session_state.messages.append(
        {"role": "assistant", "content": f"Please provide your {FIELDS[0]}."}
    )
    st.session_state.step = 1

# ---------------- Display Chat ----------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------------- User Input ----------------
user_input = st.chat_input("Type your response here...")

if user_input:
    # Exit handling
    if is_exit_message(user_input):
        st.session_state.messages.append(
            {"role": "assistant", "content": get_closing_message()}
        )
        st.stop()

    st.session_state.messages.append({"role": "user", "content": user_input})

    # -------- Step 1: Candidate Info --------
    if st.session_state.step == 1:
        current_field = FIELDS[st.session_state.field_index]
        st.session_state.candidate_data[current_field] = user_input
        st.session_state.field_index += 1

        if st.session_state.field_index < len(FIELDS):
            next_field = FIELDS[st.session_state.field_index]
            st.session_state.messages.append(
                {"role": "assistant", "content": f"Please provide your {next_field}."}
            )
        else:
            st.session_state.step = 2
            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": "Thank you. Now please list your tech stack (languages, frameworks, tools)."
                }
            )

    # -------- Step 2: Tech Stack --------
    elif st.session_state.step == 2:
        st.session_state.candidate_data["Tech Stack"] = user_input

        st.session_state.messages.append(
            {"role": "assistant", "content": "Generating technical questions based on your tech stack..."}
        )

        questions = generate_technical_questions(user_input)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": "Here are some technical questions:\n\n" + questions
            }
        )

        st.session_state.messages.append(
            {"role": "assistant", "content": get_closing_message()}
        )

        st.session_state.step = 3

    st.rerun()
