import streamlit as st
from ai_agent import handle_input
from utils.file_utils import zip_project

st.set_page_config(page_title="AI Web Builder", layout="wide")

st.title("🛠️ AI-Powered Website Builder")

with st.form("prompt_form"):
    user_input = st.text_area("Enter your website idea or request", height=200)
    submitted = st.form_submit_button("Build Website")

if submitted and user_input:
    st.info("Generating your website... please wait.")
    with st.spinner("Building step by step..."):
        steps = []
        for _ in range(50): 
            result = handle_input(user_input)
            steps.append(result)
            st.write(f"**[{result['step']}]**: {result['content']}")
            if result["step"] == "output":
                break

        zip_file_path = zip_project()
        with open(zip_file_path, "rb") as file:
            st.success("✅ Website generated successfully!")
            st.download_button("📦 Download Website ZIP", file, file_name="website.zip")
