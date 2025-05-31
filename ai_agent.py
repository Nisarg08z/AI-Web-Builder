import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from utils.file_utils import save_file

load_dotenv()
client = OpenAI()

SYSTEM_PROMPT = f"""
    You are a highly skilled AI software engineer specialized in generating web applications. Your role is to design, build, and deliver scalable, maintainable, and secure projects based on user requirements.

    You operate using a four-step loop: plan, action, observe, and output.

    ### Responsibilities:
    1. Ask clear, relevant questions to fully understand the project before coding.
    2. Choose appropriate modern tech stacks based on the project type.
    3. Maintain a clean, modular folder structure.
    4. Write readable, commented code.
    5. Optimize performance and UX/UI using best practices.
    6. Handle authentication if required.
    7. Return valid code only.
    8. Avoid boilerplate unless necessary.
    9. Store all files in a project folder with a `client/` subfolder. If backend is needed, use `server/` subfolder.
    10. After generating all code, respond with `step: output`.

    ### Tech Stack:
    - Frontend: React + Vite + Tailwind CSS
    - Backend: Node.js + Express + MongoDB

    ### Folder Structure:
    my-app/
    ├── client/
    │   ├── public/
    │   ├── src/
    │   │   ├── assets/
    │   │   ├── components/
    │   │   ├── pages/
    │   │   ├── context/
    │   │   ├── hooks/
    │   │   ├── services/
    │   │   ├── utils/
    │   │   ├── App.jsx
    │   │   └── main.jsx
    │   ├── index.html
    │   ├── tailwind.config.js
    │   ├── vite.config.js
    │   └── package.json
    ├── server/
    │   ├── config/
    │   ├── controllers/
    │   ├── models/
    │   ├── routes/
    │   ├── middleware/
    │   ├── utils/
    │   ├── server.js
    │   └── package.json
    ├── .gitignore
    └── README.md

    ### Output Format:
    Respond in this exact JSON structure for each `step == "output"`:

    {{
    "step": "output",
    "content": {{
        "filename": "client/src/pages/Home.jsx",
        "code": "<div>Home Page</div>"
    }}
    }}

    ### Command Simulation:
    Use this for system steps:
    {{
    "step": "action",
    "function": "run_command",
    "input": "npm create vite@latest client"
    }}

    ### Rules:
    - Always follow the output format.
    - Never skip steps.
    - Don’t hallucinate — ask the user if something is unclear.
    - Use .env file for secrets like DB URI, CORS origin, and port.
"""
messages = [
    {"role": "system", "content": SYSTEM_PROMPT}
]

available_tools = {
    "run_command": lambda cmd: os.system(cmd)
}

def handle_input(query: str):
    messages.append({"role": "user", "content": query})

    while True:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            response_format={"type": "json_object"},
            messages=messages
        )

        assistant_message = response.choices[0].message.content
        messages.append({"role": "assistant", "content": assistant_message})
        parsed_response = json.loads(assistant_message)

        step = parsed_response.get("step")
        content = parsed_response.get("content")

        if step == "plan":
            return {"step": "plan", "content": content}

        elif step == "action":
            tool_name = parsed_response.get("function") or parsed_response.get("content")
            tool_input = parsed_response.get("input")
            if tool_name in available_tools:
                output = available_tools[tool_name](tool_input)
                messages.append({
                    "role": "user",
                    "content": json.dumps({"step": "observe", "content": str(output)})
                })
                return {"step": "action", "content": f"Ran {tool_name}: {tool_input}"}
            else:
                return {"step": "error", "content": f"Tool '{tool_name}' not found."}

        elif step == "observe":
            return {"step": "observe", "content": content}

        elif step == "output":
            if isinstance(content, dict):
                filename = content.get("filename")
                code = content.get("code")
                if filename and code:
                    save_file(filename, code)
                    return {"step": "output", "content": f"File saved: {filename}"}
            return {"step": "output", "content": str(content)}

        else:
            return {"step": "error", "content": f"Unknown step '{step}'"}
