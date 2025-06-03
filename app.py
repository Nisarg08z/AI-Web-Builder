import streamlit as st
import os
import tempfile
from ai_agent import handle_input
from utils.file_utils import delete_generated_content, zip_project

st.set_page_config(page_title="AI Web Builder", layout="wide")

st.title("🛠️ AI-Powered Website Builder")

col1, col2 = st.columns([1, 1])
with col1:
    if st.button("🗑️ Delete Existing Website"):
        if delete_generated_content():
            st.success("Deleted contents inside the generated folder.")
        else:
            st.warning("No content to delete or error occurred.")

with col2:
    if st.button("🌐 Open Website in New Tab"):
        st.info("Starting development server...")
        with st.spinner("Running..."):
            response = handle_input("Start development server")
            st.write(f"**[{response['step']}]**: {response['content']}")

with st.form("prompt_form"):
    user_input = st.text_area("Enter your website idea or request", height=200)
    submitted = st.form_submit_button("Build Website")

if submitted and user_input:
    delete_generated_content()

    st.info("Generating your website... please wait.")
    with st.spinner("Building step by step..."):
        steps = []
        for _ in range(50):
            result = handle_input(user_input)
            steps.append(result)
            st.write(f"**[{result['step']}]**: {result['content']}")
            if result["step"] == "output":
                break

    st.success("Website generation complete! Click browser button to open.")

    if st.button("📦 Download Website ZIP"):
        temp_dir = tempfile.gettempdir()
        zip_path = zip_project("generated", temp_dir)
        with open(zip_path, "rb") as f:
            st.download_button(
                label="Download Website ZIP",
                data=f,
                file_name=os.path.basename(zip_path),
                mime="application/zip"
            )
