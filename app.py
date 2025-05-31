import streamlit as st
import os
import webbrowser
import shutil
import tempfile

from ai_agent import handle_input
from utils.file_utils import zip_project, delete_file, delete_generated_folder

st.set_page_config(page_title="AI Web Builder", layout="wide")

st.title("🛠️ AI-Powered Website Builder")

# Action buttons
col1, col2 = st.columns([1, 1])
with col1:
    if st.button("🗑️ Delete Existing Website"):
        if delete_generated_folder():
            st.success("Deleted generated website.")
        else:
            st.warning("No generated folder found.")

with col2:
    if os.path.exists("generated/client/index.html"):
        if st.button("🌐 Open Website in New Tab"):
            webbrowser.open_new_tab("generated/client/index.html")
    else:
        st.info("No website found to preview.")

# Form for prompt input
with st.form("prompt_form"):
    user_input = st.text_area("Enter your website idea or request", height=200)
    submitted = st.form_submit_button("Build Website")

# If submitted
if submitted and user_input:
    # Delete old website
    delete_generated_folder()

    st.info("Generating your website... please wait.")
    with st.spinner("Building step by step..."):
        steps = []
        for _ in range(50):
            result = handle_input(user_input)
            steps.append(result)
            st.write(f"**[{result['step']}]**: {result['content']}")
            if result["step"] == "output":
                break

        # Create temporary zip
        temp_dir = tempfile.gettempdir()
        zip_path = zip_project(output_dir=temp_dir)

        with open(zip_path, "rb") as file:
            st.success("✅ Website generated successfully!")
            if st.download_button("📦 Download Website ZIP", file, file_name="generated_site.zip", mime="application/zip"):
                st.info("Cleaning up ZIP file...")
                delete_file(zip_path)
