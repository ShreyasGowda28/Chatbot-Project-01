
from html import escape

import streamlit as st

from chatbot import get_bot_response
from faq_data import FAQ_DATA


SAMPLE_QUESTIONS = [
    "What is TSIAR?",
    "What sports and games does TSIAR offer?",
    "How do I register with TSIAR?",
    "Which esports can I play through TSIAR?",
    "What badminton events does TSIAR list?",
    "How can I find upcoming tournaments?",
]


def initialize_session_state():
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []


def save_chat(user_question, bot_response):
    st.session_state.chat_history.insert(
        0,
        {
            "question": user_question,
            "response": bot_response,
        },
    )


def ask_question(question):
    response = get_bot_response(question)
    save_chat(question, response)


def show_sidebar():
    with st.sidebar:
        st.header("TSIAR Sports Questions")
        st.caption("Click a question to get an answer.")

        for i, question in enumerate(SAMPLE_QUESTIONS):
            if st.button(
                question,
                key=f"sample_question_{i}",
                use_container_width=True,
            ):
                ask_question(question)

        st.divider()

        st.markdown(
            f"**FAQ database:** {len(FAQ_DATA)} questions"
        )

        if st.button("Clear Chat History", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()


def show_header():
    st.markdown(
        """
        <div style="
            background: white;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 20px;
        ">
            <h1 style="color: #0f172a; margin-bottom: 8px;">
                TSIAR Sports Chatbot
            </h1>
            <h3 style="color: #2563eb; margin-top: 0;">
                TSIAR Sports Information Assistant
            </h3>
            <p style="color: #475569;">
                Ask about TSIAR sports, esports, registration,
                tournaments, results, and official updates.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def show_chat_card(chat_item):
    response = chat_item["response"]

    question = escape(str(chat_item["question"]))
    answer = escape(str(response["answer"]))
    status = escape(str(response["status"]))

    if response["is_confident"]:
        matched_question = escape(str(response["matched_question"]))
        category = escape(str(response["category"]))
        details = (
            f"<strong>Matched FAQ:</strong> {matched_question}<br>"
            f"<strong>Category:</strong> {category}<br>"
            f"<strong>Confidence:</strong> "
            f"{response['confidence_score']:.2f}"
        )
        status_color = "#166534"
        status_bg = "#dcfce7"
    else:
        details = (
            f"<strong>Confidence:</strong> "
            f"{response['confidence_score']:.2f}"
        )
        status_color = "#92400e"
        status_bg = "#fef3c7"

    st.markdown(
        f"""
        <div style="
            background: white;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            padding: 18px;
            margin: 14px 0;
        ">
            <p style="color: #1d4ed8; font-weight: 600;">
                You: {question}
            </p>
            <span style="
                background: {status_bg};
                color: {status_color};
                border-radius: 6px;
                padding: 5px 9px;
                font-size: 13px;
            ">{status}</span>
            <p style="
                color: #0f172a;
                line-height: 1.6;
                margin-top: 16px;
            ">
                <strong>TSIAR Assistant:</strong> {answer}
            </p>
            <hr style="border: 0; border-top: 1px solid #e2e8f0;">
            <p style="color: #64748b; font-size: 13px;">
                {details}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def run_app():
    st.set_page_config(
        page_title="TSIAR Sports Chatbot",
        page_icon="🏆",
        layout="wide",
    )

    initialize_session_state()
    show_sidebar()
    show_header()

    st.subheader("Ask a question")

    with st.form("question_form", clear_on_submit=True):
        user_question = st.text_input(
            "Your question",
            placeholder="Example: How do I register with TSIAR?",
        )
        submitted = st.form_submit_button(
            "Ask Chatbot",
            use_container_width=True,
        )

    if submitted:
        if not user_question.strip():
            st.warning("Please enter a question first.")
        else:
            ask_question(user_question.strip())

    st.subheader("Chat History")

    if st.session_state.chat_history:
        for chat_item in st.session_state.chat_history:
            show_chat_card(chat_item)
    else:
        st.info(
            "Welcome! Type a question or click one of the "
            "sample questions in the sidebar to begin."
        )


if __name__ == "__main__":
    run_app()
