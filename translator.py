import os
from dotenv import load_dotenv
import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain.chat_models import init_chat_model

# Load environment variables
load_dotenv()

# Initialize model
model = init_chat_model("cohere:c4ai-aya-vision-8b")

# Streamlit page configuration
st.set_page_config(page_title="🌍 AI Translator", layout="centered")

# ---------- Custom CSS ----------
st.markdown("""
    <style>
        body {
            background-color: #f4f6f8;
        }
        .main {
            background-color: #ffffff;
            padding: 2rem;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
        .stTextArea textarea {
            font-size: 16px;
            padding: 1rem;
        }
        .stSelectbox select {
            padding: 0.6rem;
            font-size: 16px;
        }
        .translate-result {
            border: 1px solid #e0e0e0;
            border-radius: 10px;
            background-color: #ffffff;
            padding: 1.5rem;
            margin-top: 1rem;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        }
        .translate-result h4 {
            color: #007BFF;
            margin-bottom: 1rem;
        }
        .translate-result p {
            font-size: 18px;
            line-height: 1.6;
            color: #333333;
        }
        .header-title {
            font-size: 40px;
            font-weight: 800;
            background: linear-gradient(90deg, #1e90ff, #00c6ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
    </style>
""", unsafe_allow_html=True)

# ---------- Title ----------
st.markdown("<h1 class='header-title'>🌍 AI Translator</h1>", unsafe_allow_html=True)
st.write("Seamlessly translate between languages using AI — natural, friendly, and fast.")

st.markdown("---")

# ---------- Languages ----------
languages = [
    "English", "Hindi", "Spanish", "French", "German", "Chinese", "Japanese",
    "Korean", "Russian", "Italian", "Portuguese", "Arabic", "Bengali", "Urdu",
    "Turkish", "Greek", "Persian", "Thai", "Vietnamese"
]

# Initialize session state
if "source_language" not in st.session_state:
    st.session_state.source_language = "English"
if "target_language" not in st.session_state:
    st.session_state.target_language = "Hindi"

# ---------- Language Selection ----------
st.subheader("🔤 Choose Languages")
col1, col2 = st.columns(2)
with col1:
    st.session_state.source_language = st.selectbox(
        "Source Language:",
        options=languages,
        index=languages.index(st.session_state.source_language)
    )
with col2:
    st.session_state.target_language = st.selectbox(
        "Target Language:",
        options=languages,
        index=languages.index(st.session_state.target_language)
    )

# ---------- Text Input ----------
st.subheader("✍️ Enter Text to Translate")
text = st.text_area(
    "Input Text:",
    placeholder="e.g., Hello, how are you doing today?",
    height=160
)
st.caption(f"🧮 Character count: {len(text)}")

# ---------- Translate Button ----------
translate_btn = st.button("🌐 Translate Now", use_container_width=True)

# ---------- Result ----------
st.subheader("📤 Translation Output")
result_placeholder = st.empty()

# ---------- Translation Logic ----------
if translate_btn:
    if text.strip() == "":
        st.warning("⚠️ Please enter some text before translating.")
    else:
        with st.spinner("🔄 Translating... please wait."):
            # Prompt creation
            translation_template = ChatPromptTemplate.from_messages([
                ("system", "You are a professional language translator. "
                           "Translate the following text from {source_language} to {target_language} "
                           "with a polite and natural tone."),
                ("human", "{text}")
            ])

            messages = translation_template.format_messages(
                text=text,
                source_language=st.session_state.source_language,
                target_language=st.session_state.target_language
            )

            # Call the model
            response = model.invoke(messages)

            # Show result
            result_placeholder.markdown(
                f"""
                <div class="translate-result">
                    <h4>🌐 Translated to {st.session_state.target_language}:</h4>
                    <p>{response.content}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
