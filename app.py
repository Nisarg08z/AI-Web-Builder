import streamlit as st
import os
import io
import tempfile
import threading
from ai_agent import handle_input, get_last_project_name
from utils.file_utils import delete_project, zip_project, is_react_project, build_react_project

st.set_page_config(page_title="AI Web Builder", layout="wide")
st.title("🛠️ AI-Powered Website Builder")

if "last_project" not in st.session_state:
    st.session_state.last_project = None

def open_website_preview(project_name: str):
    project_path = os.path.abspath(os.path.join("generated", project_name))
    index_html_path = None

    if is_react_project(project_path):
        success, msg = build_react_project(project_path)
        if not success:
            st.error(msg)
            return
        # Look for common build folders
        for folder in ["dist", "build"]:
            html_path = os.path.join(project_path, folder, "index.html")
            if os.path.exists(html_path):
                index_html_path = html_path
                break
    else:
        html_path = os.path.join(project_path, "index.html")
        if os.path.exists(html_path):
            index_html_path = html_path

    if index_html_path:
        st.success("✅ Opening preview!")
        with open(index_html_path, encoding='utf-8') as f:
            html_content = f.read()
        preview_html = f"""
        <iframe srcdoc="{html_content.replace('"', '&quot;')}" 
                style="width: 100vw; height: 100vh; border: none;"
                frameborder="0"
                allowfullscreen
                sandbox="allow-scripts allow-same-origin">
        </iframe>
        """
        st.components.v1.html(preview_html, height=900, scrolling=False)
    else:
        st.warning("⚠️ index.html not found for preview.")

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
            st.info("⏳ Preparing site preview...")
            open_website_preview(st.session_state.last_project)
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

    st.success("✅ Website generation complete!")

    project_name = get_last_project_name()
    st.session_state.last_project = project_name

    if project_name:
        zip_path = zip_project(f"generated/{project_name}", tempfile.gettempdir())
        
        with open(zip_path, "rb") as f:
            zip_bytes = io.BytesIO(f.read()) 

        st.download_button(
            label=f"📦 Download {project_name}.zip",
            data=zip_bytes,
            file_name=f"{project_name}.zip",
            mime="application/zip"
        )

