import streamlit as st
import os
import tempfile
from ai_agent import handle_input, get_last_project_name
from utils.file_utils import delete_project, zip_project

st.set_page_config(page_title="AI Web Builder", layout="wide")
st.title("🛠️ AI-Powered Website Builder")

if "last_project" not in st.session_state:
    st.session_state.last_project = None

col1, col2 = st.columns([1, 1])
with col1:
    if st.button("🗑️ Delete Recent Project"):
        if st.session_state.last_project and delete_project(st.session_state.last_project):
            st.success(f"Deleted project: {st.session_state.last_project}")
            st.session_state.last_project = None
        else:
            st.warning("No recent project to delete or error occurred.")

with col2:
    if st.button("🌐 Open Website in New Tab"):
        if st.session_state.last_project:
            st.info("Starting development server...")
            with st.spinner("Running..."):
                response = handle_input(f"Start development server for {st.session_state.last_project}")
                st.write(f"**[{response['step']}]**: {response['content']}")
        else:
            st.warning("No recent project found to run.")

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
            with st.container():
                st.markdown(f"**🧱 Step: `{result['step']}`**")
                st.code(result['content'])
            if result["step"] == "output":
                break

    st.success("Website generation complete!")

    # Track recent project
    project_name = get_last_project_name()
    st.session_state.last_project = project_name

    if project_name:
        if st.button("📦 Download Website ZIP"):
            temp_dir = tempfile.gettempdir()
            zip_path = zip_project(f"generated/{project_name}", temp_dir)
            with open(zip_path, "rb") as f:
                st.download_button(
                    label=f"Download {project_name}.zip",
                    data=f,
                    file_name=f"{project_name}.zip",
                    mime="application/zip"
                )
