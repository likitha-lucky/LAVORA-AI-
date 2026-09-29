import streamlit as st
import ollama
import html


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖🌐",
    layout="centered"
)


# =========================================================
# SESSION STATE
# =========================================================

if "chat_started" not in st.session_state:
    st.session_state.chat_started = False

if "messages" not in st.session_state:
    st.session_state.messages = []


# =========================================================
# WELCOME SCREEN
# =========================================================

if not st.session_state.chat_started:

    st.markdown("""
<style>

.stApp {
    background: linear-gradient(
        135deg,
        #0f172a,
        #111827,
        #1e1b4b
    );
}


/* =====================================================
   WELCOME AREA
===================================================== */

.welcome-area {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    padding-top: 20px;
}


/* =====================================================
   WELCOME TITLE
===================================================== */

.welcome-title {
    font-size: 52px;
    font-weight: 800;
    color: white;

    margin-top: 0;
    margin-bottom: 12px;
}


/* =====================================================
   WELCOME TEXT
===================================================== */

.welcome-text {
    font-size: 20px;
    color: #c7d2fe;

    margin-bottom: 20px;
}


/* =====================================================
   ENTER CHAT BUTTON
===================================================== */

div[data-testid="stButton"] {
    width: 100% !important;
    display: flex !important;
    justify-content: center !important;
    align-items: center !important;
}

div[data-testid="stButton"] > button {
    width: 240px !important;
    height: 55px !important;

    margin: 0 auto !important;

    border-radius: 14px !important;
    border: none !important;

    background: linear-gradient(
        90deg,
        #6366f1,
        #8b5cf6
    ) !important;

    color: white !important;

    font-size: 18px !important;
    font-weight: 700 !important;
}

div[data-testid="stButton"] > button:hover {
    transform: translateY(-2px);

    box-shadow:
        0 7px 20px
        rgba(99,102,241,0.4) !important;
}

</style>
""", unsafe_allow_html=True)


    # =====================================================
    # WELCOME CONTENT
    # =====================================================

    st.markdown(
        '<div class="welcome-area">'
        '<div class="welcome-title">'
        'LAVORA AI🌐'
        '</div>'
        '<div class="welcome-text">'
        'Your intelligent AI assistant🫱🏻‍🫲🏻😎'
        '</div>',
        unsafe_allow_html=True
    )


    # =====================================================
    # ENTER CHAT
    # =====================================================

    if st.button(
        "ENTER CHAT ⌨  ➔",
        key="enter_chat"
    ):

        st.session_state.chat_started = True

        st.rerun()


    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


# =========================================================
# CHAT SCREEN
# =========================================================

else:

    st.markdown("""
<style>

/* =====================================================
   BACKGROUND
===================================================== */

.stApp {
    background: linear-gradient(
        135deg,
        #0f172a 0%,
        #111827 50%,
        #1e1b4b 100%
    );

    color: white;
}


/* =====================================================
   MAIN CONTAINER
===================================================== */

.block-container {
    max-width: 1000px;
    padding-top: 35px;
    padding-bottom: 100px;
}


/* =====================================================
   HEADER
===================================================== */

.chat-title {
    text-align: center;
    font-size: 42px;
    font-weight: 800;
    color: white;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    color: #a5b4fc;
    font-size: 17px;
    margin-bottom: 35px;
}


/* =====================================================
   USER MESSAGE
===================================================== */

.user-row {
    display: flex;
    justify-content: flex-end;
    align-items: flex-end;
    width: 100%;

    margin-top: 18px;
    margin-bottom: 12px;
}

.user-message {
    max-width: 65%;

    background: linear-gradient(
        135deg,
        #6366f1,
        #8b5cf6
    );

    color: white;

    padding: 13px 18px;

    border-radius:
        18px
        18px
        4px
        18px;

    font-size: 17px;
    line-height: 1.5;

    box-shadow:
        0 5px 15px
        rgba(0,0,0,0.2);

    overflow-wrap: break-word;
    white-space: pre-wrap;
}

.user-avatar {
    margin-left: 8px;
    font-size: 22px;
    align-self: flex-end;
}


/* =====================================================
   AI MESSAGE
===================================================== */

.ai-row {
    display: flex;
    justify-content: flex-start;
    align-items: flex-end;
    width: 100%;

    margin-top: 8px;
    margin-bottom: 18px;
}

.ai-avatar {
    margin-right: 8px;
    font-size: 22px;
    align-self: flex-end;
}

.ai-message {
    max-width: 75%;

    background: #1e293b;

    border: 1px solid #475569;

    color: #f8fafc;

    padding: 16px 20px;

    border-radius:
        18px
        18px
        18px
        4px;

    font-size: 17px;
    line-height: 1.7;

    box-shadow:
        0 5px 18px
        rgba(0,0,0,0.25);

    overflow-wrap: break-word;
    white-space: pre-wrap;
}


/* =====================================================
   AI RESPONSE STATUS
===================================================== */

.ai-status {
    color: #f8fafc;

    font-size: 17px;

    font-weight: 600;

    margin-top: 10px;
    margin-bottom: 12px;

    min-height: 25px;
}


/* =====================================================
   QUESTION LABEL
===================================================== */

.question-label {
    color: #f1f5f9;

    font-size: 18px;
    font-weight: 700;

    margin-top: 15px;
    margin-bottom: 8px;
}


/* =====================================================
   FORM
===================================================== */

div[data-testid="stForm"] {
    border: none !important;

    padding: 0 !important;

    background: transparent !important;
}


/* =====================================================
   INPUT
===================================================== */

div[data-baseweb="input"] {
    background-color: #f8fafc !important;

    border: 2px solid #64748b !important;

    border-radius: 13px !important;

    min-height: 52px;
}

div[data-baseweb="input"] input {
    color: #111827 !important;

    -webkit-text-fill-color: #111827 !important;

    font-size: 18px !important;
}

div[data-baseweb="input"] input::placeholder {
    color: #64748b !important;

    opacity: 1 !important;
}

div[data-baseweb="input"]:focus-within {
    border: 2px solid #818cf8 !important;

    box-shadow:
        0 0 15px
        rgba(129,140,248,0.3);
}


/* =====================================================
   SEND BUTTON
===================================================== */

div[data-testid="stFormSubmitButton"] button {
    width: 100% !important;

    min-height: 52px !important;

    margin-top: 0 !important;

    border-radius: 13px !important;

    border: none !important;

    background: linear-gradient(
        90deg,
        #6366f1,
        #8b5cf6
    ) !important;

    color: white !important;

    font-size: 16px !important;

    font-weight: 700 !important;

    transition: all 0.2s ease !important;
}

div[data-testid="stFormSubmitButton"] button:hover {
    transform: translateY(-2px) !important;

    box-shadow:
        0 7px 20px
        rgba(99,102,241,0.4) !important;
}


/* =====================================================
   EXIT CHAT BUTTON
===================================================== */

div[data-testid="stButton"] button {
    width: 190px !important;

    min-height: 48px !important;

    margin-top: 20px !important;

    border-radius: 12px !important;

    border: none !important;

    background: linear-gradient(
        90deg,
        #6366f1,
        #8b5cf6
    ) !important;

    color: white !important;

    font-size: 17px !important;

    font-weight: 700 !important;

    transition: all 0.2s ease !important;
}

div[data-testid="stButton"] button:hover {
    transform: translateY(-2px) !important;

    box-shadow:
        0 7px 20px
        rgba(99,102,241,0.4) !important;
}


/* =====================================================
   WARNING
===================================================== */

div[data-testid="stAlert"] {
    margin-top: 10px;
}

</style>
""", unsafe_allow_html=True)


    # =====================================================
    # HEADER
    # =====================================================

    st.markdown(
        '<div class="chat-title">'
        'LAVORA AI🌐'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Your Intelligent AI Assistant🧠💡🤖'
        '</div>',
        unsafe_allow_html=True
    )


    # =====================================================
    # DISPLAY CHAT
    # =====================================================

    for message in st.session_state.messages:

        content = html.escape(
            str(message["content"])
        )


        # -------------------------------------------------
        # USER MESSAGE
        # -------------------------------------------------

        if message["role"] == "user":

            st.markdown(
                '<div class="user-row">'
                '<div class="user-message">'
                + content +
                '</div>'
                '<div class="user-avatar">'
                '👩‍💻'
                '</div>'
                '</div>',
                unsafe_allow_html=True
            )


        # -------------------------------------------------
        # AI MESSAGE
        # -------------------------------------------------

        elif message["role"] == "assistant":

            st.markdown(
                '<div class="ai-row">'
                '<div class="ai-avatar">'
                '🔎'
                '</div>'
                '<div class="ai-message">'
                + content +
                '</div>'
                '</div>',
                unsafe_allow_html=True
            )


    # =====================================================
    # AI RESPONSE STATUS
    # =====================================================

    response_status = st.empty()


    # =====================================================
    # QUESTION LABEL
    # =====================================================

    st.markdown(
        '<div class="question-label">'
        'ENTER YOUR INQUIRY TO BEGIN 🎯'
        '</div>',
        unsafe_allow_html=True
    )


    # =====================================================
    # INPUT + SEND BUTTON
    # =====================================================

    with st.form(
        key="question_form",
        clear_on_submit=True
    ):

        input_column, send_column = st.columns(
            [5.5, 1.2],
            gap="small"
        )


        # -------------------------------------------------
        # INPUT
        # -------------------------------------------------

        with input_column:

            question = st.text_input(
                "",
                placeholder="Type your input here...",
                label_visibility="collapsed"
            )


        # -------------------------------------------------
        # SEND
        # -------------------------------------------------

        with send_column:

            submitted = st.form_submit_button(
                "SEND 📤🚀"
            )


    # =====================================================
    # PROCESS QUESTION
    # =====================================================

    if submitted:

        if question.strip():

            response_status.markdown(
                '<div class="ai-status">'
                '💻 AI response...'
                '</div>',
                unsafe_allow_html=True
            )


            # -------------------------------------------------
            # ADD USER MESSAGE
            # -------------------------------------------------

            st.session_state.messages.append({
                "role": "user",
                "content": question.strip()
            })


            # -------------------------------------------------
            # ASK OLLAMA
            # -------------------------------------------------

            try:

                response = ollama.chat(
                    model="llama3.2",
                    messages=st.session_state.messages
                )

                answer = response["message"]["content"]

            except Exception as e:

                answer = (
                    "⚠️ Ollama error: "
                    + str(e)
                )


            # -------------------------------------------------
            # ADD AI RESPONSE
            # -------------------------------------------------

            st.session_state.messages.append({
                "role": "assistant",
                "content": answer
            })


            # -------------------------------------------------
            # REFRESH
            # -------------------------------------------------

            st.rerun()


        else:

            st.warning(
                "⚠️ Please enter a question."
            )


    # =====================================================
    # EXIT CHAT
    # =====================================================

    if st.button(
        "EXIT CHAT 🚪",
        key="exit_chat"
    ):

        st.session_state.chat_started = False

        st.session_state.messages = []

        st.rerun()
