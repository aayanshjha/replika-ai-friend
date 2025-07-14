
import streamlit as st
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.prompts import PromptTemplate
from langchain_ollama import OllamaLLM
import json, os, time, threading

# -------------------- Settings --------------------
st.set_page_config(page_title="🧠 Your AI Companion", layout="centered")

# -------------------- User Profile --------------------
PROFILE_FILE = "user_profile.json"
MEMORY_FILE = "memory.json"

def load_user_profile():
    if os.path.exists(PROFILE_FILE):
        with open(PROFILE_FILE, "r") as f:
            return json.load(f)
    else:
        return {"name": "Friend", "goals": []}

def save_user_profile(profile):
    with open(PROFILE_FILE, "w") as f:
        json.dump(profile, f, indent=4)

user = load_user_profile()
st.title(f"👋 Hey {user['name']}! I'm your AI Companion.")

# -------------------- Load & Save Reminders --------------------
def load_reminders():
    if not os.path.exists(MEMORY_FILE) or os.path.getsize(MEMORY_FILE) == 0:
        return []
    try:
        with open(MEMORY_FILE, "r") as f:
            data = json.load(f)
            return data.get("reminders", [])
    except json.JSONDecodeError:
        return []

def save_reminders(reminders):
    with open(MEMORY_FILE, "w") as f:
        json.dump({"reminders": reminders}, f, indent=4)

# -------------------- Reminder Checker --------------------
def reminder_loop():
    while True:
        now = time.strftime("%H:%M")
        reminders = load_reminders()
        due = [r["task"] for r in reminders if r["time"] == now]
        if due:
            st.toast("⏰ Reminder: " + ", ".join(due))
        time.sleep(60)

threading.Thread(target=reminder_loop, daemon=True).start()

# -------------------- AI Setup --------------------
llm = OllamaLLM(model="llama3")  # You can try "mistral" for faster results
if "chat_history" not in st.session_state:
    st.session_state.chat_history = ChatMessageHistory()

prompt = PromptTemplate(
    input_variables=["chat_history", "question"],
    template="""
You are a supportive and friendly AI companion who helps emotionally and practically.

Previous conversation:
{chat_history}

User: {question}
AI:"""
)

# -------------------- User Input & Display --------------------
question = st.chat_input("Talk to me...")

for msg in st.session_state.chat_history.messages:
    role = "user" if msg.type == "human" else "assistant"
    st.chat_message(role).write(msg.content)

if question:
    chat_history_text = "\n".join(
        [f"{msg.type.capitalize()}: {msg.content}" for msg in st.session_state.chat_history.messages]
    )

    response = llm.invoke(prompt.format(chat_history=chat_history_text, question=question))

    st.chat_message("user").write(question)
    st.chat_message("assistant").write(response)

    st.session_state.chat_history.add_user_message(question)
    st.session_state.chat_history.add_ai_message(response)

# -------------------- Add Reminder Form --------------------
with st.expander("📅 Set Reminder"):
    with st.form("reminder_form"):
        task = st.text_input("Task")
        time_input = st.time_input("Time (24h format)")
        submitted = st.form_submit_button("Save")
        if submitted:
            reminders = load_reminders()
            reminders.append({"task": task, "time": time_input.strftime("%H:%M")})
            save_reminders(reminders)
            st.success("Reminder saved!")

# -------------------- Custom CSS --------------------
st.markdown("""
    <style>
        .stChatMessage { padding: 10px; border-radius: 10px; }
        .stChatMessage.user { background-color: #DCF8C6; text-align: right; }
        .stChatMessage.assistant { background-color: #F1F0F0; text-align: left; }
        .main { background-color: #f9f9f9; }
    </style>
""", unsafe_allow_html=True)









#import streamlit as st
# from langchain_community.chat_message_histories import ChatMessageHistory
# from langchain_core.prompts import PromptTemplate
# from langchain_ollama import OllamaLLM
# import json, os, time, threading

# # -------------------- Settings --------------------
# st.set_page_config(page_title="🧠 Your AI Companion", layout="centered")

# # -------------------- User Profile --------------------
# PROFILE_FILE = "user_profile.json"
# MEMORY_FILE = "memory.json"

# def load_user_profile():
#     if os.path.exists(PROFILE_FILE):
#         with open(PROFILE_FILE, "r") as f:
#             return json.load(f)
#     else:
#         return {"name": "Friend", "goals": []}

# def save_user_profile(profile):
#     with open(PROFILE_FILE, "w") as f:
#         json.dump(profile, f, indent=4)

# user = load_user_profile()
# st.title(f"👋 Hey {user['name']}! I'm your AI Companion.")

# # -------------------- Load & Save Reminders --------------------
# def load_reminders():
#     if not os.path.exists(MEMORY_FILE) or os.path.getsize(MEMORY_FILE) == 0:
#         return []
#     try:
#         with open(MEMORY_FILE, "r") as f:
#             data = json.load(f)
#             return data.get("reminders", [])
#     except json.JSONDecodeError:
#         return []

# def save_reminders(reminders):
#     with open(MEMORY_FILE, "w") as f:
#         json.dump({"reminders": reminders}, f, indent=4)

# # -------------------- Reminder Checker --------------------
# def reminder_loop():
#     while True:
#         now = time.strftime("%H:%M")
#         reminders = load_reminders()
#         due = [r["task"] for r in reminders if r["time"] == now]
#         if due:
#             st.toast("⏰ Reminder: " + ", ".join(due))
#         time.sleep(60)

# threading.Thread(target=reminder_loop, daemon=True).start()

# # -------------------- AI Setup --------------------
# llm = OllamaLLM(model="llama3")  # You can try "mistral" for faster results
# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = ChatMessageHistory()

# prompt = PromptTemplate(
#     input_variables=["chat_history", "question"],
#     template="""
# You are a supportive and friendly AI companion who helps emotionally and practically.

# Previous conversation:
# {chat_history}

# User: {question}
# AI:"""
# )

# # -------------------- User Input & Display --------------------
# question = st.chat_input("Talk to me...")

# for msg in st.session_state.chat_history.messages:
#     role = "user" if msg.type == "human" else "assistant"
#     st.chat_message(role).write(msg.content)

# if question:
#     chat_history_text = "\n".join(
#         [f"{msg.type.capitalize()}: {msg.content}" for msg in st.session_state.chat_history.messages]
#     )

#     response = llm.invoke(prompt.format(chat_history=chat_history_text, question=question))

#     st.chat_message("user").write(question)
#     st.chat_message("assistant").write(response)

#     st.session_state.chat_history.add_user_message(question)
#     st.session_state.chat_history.add_ai_message(response)

# # -------------------- Add Reminder Form --------------------
# with st.expander("📅 Set Reminder"):
#     with st.form("reminder_form"):
#         task = st.text_input("Task")
#         time_input = st.time_input("Time (24h format)")
#         submitted = st.form_submit_button("Save")
#         if submitted:
#             reminders = load_reminders()
#             reminders.append({"task": task, "time": time_input.strftime("%H:%M")})
#             save_reminders(reminders)
#             st.success("Reminder saved!")

# # -------------------- Custom CSS --------------------
# st.markdown("""
#     <style>
#         .stChatMessage { padding: 10px; border-radius: 10px; }
#         .stChatMessage.user { background-color: #DCF8C6; text-align: right; }
#         .stChatMessage.assistant { background-color: #F1F0F0; text-align: left; }
#         .main { background-color: #f9f9f9; }
#     </style>
# """, unsafe_allow_html=True)























# # import streamlit as st
# # import json
# # import os
# # from datetime import datetime
# # from langchain_ollama import OllamaLLM
# # from langchain_core.prompts import PromptTemplate
# # from langchain_community.chat_message_histories import ChatMessageHistory

# # # Set page
# # st.set_page_config(page_title="AI Friend", layout="centered")
# # st.markdown(
# #     "<style> body { background-color: #f4f4f4; } </style>",
# #     unsafe_allow_html=True,
# # )
# # st.markdown("<h1 style='text-align:center;'>💫 Meet Luna - Your AI Companion</h1>", unsafe_allow_html=True)

# # # CSS for chat bubble design
# # st.markdown("""
# #     <style>
# #         .user-msg {
# #             background-color: #d1e7dd;
# #             padding: 12px;
# #             border-radius: 12px;
# #             margin-bottom: 8px;
# #             max-width: 80%;
# #             align-self: flex-end;
# #         }
# #         .ai-msg {
# #             background-color: #fff;
# #             padding: 12px;
# #             border-radius: 12px;
# #             margin-bottom: 8px;
# #             max-width: 80%;
# #             align-self: flex-start;
# #             box-shadow: 0px 2px 6px rgba(0,0,0,0.1);
# #         }
# #         .chat-row {
# #             display: flex;
# #             flex-direction: column;
# #         }
# #     </style>
# # """, unsafe_allow_html=True)

# # # Load model
# # llm = OllamaLLM(model="llama3")

# # # Memory
# # if "chat_history" not in st.session_state:
# #     st.session_state.chat_history = ChatMessageHistory()

# # MEMORY_FILE = "memory.json"
# # if not os.path.exists(MEMORY_FILE):
# #     with open(MEMORY_FILE, "w") as f:
# #         json.dump({"reminders": []}, f)

# # def load_reminders():
# #     with open(MEMORY_FILE, "r") as f:
# #         return json.load(f)["reminders"]

# # def save_reminder(text):
# #     reminders = load_reminders()
# #     reminders.append({"text": text, "time": str(datetime.now())})
# #     with open(MEMORY_FILE, "w") as f:
# #         json.dump({"reminders": reminders}, f)

# # # Prompt template
# # prompt = PromptTemplate(
# #     input_variables=["chat_history", "question"],
# #     template="""
# # You are Luna, a warm, caring, and supportive AI friend. You remember the user's emotions, help them through tough times, and chat naturally like a human best friend. Be casual, encouraging, and understanding.

# # Previous messages:
# # {chat_history}

# # User: {question}
# # Luna:"""
# # )

# # # Get input
# # question = st.chat_input("Talk to Luna...")

# # # Chat bubble rendering
# # def display_message(role, message):
# #     if role == "user":
# #         st.markdown(f"<div class='chat-row user-msg'><strong>You:</strong><br>{message}</div>", unsafe_allow_html=True)
# #     else:
# #         st.markdown(f"<div class='chat-row ai-msg'><strong>Luna:</strong><br>{message}</div>", unsafe_allow_html=True)

# # # Display history
# # for msg in st.session_state.chat_history.messages:
# #     role = "user" if msg.type == "human" else "assistant"
# #     display_message(role, msg.content)

# # # Process message
# # if question:
# #     chat_history_text = "\n".join([f"{msg.type.capitalize()}: {msg.content}" for msg in st.session_state.chat_history.messages])
# #     response = llm.invoke(prompt.format(chat_history=chat_history_text, question=question))

# #     display_message("user", question)
# #     display_message("assistant", response)

# #     st.session_state.chat_history.add_user_message(question)
# #     st.session_state.chat_history.add_ai_message(response)

# #     if "remind me" in question.lower():
# #         save_reminder(question)
# #         st.toast("📌 Reminder saved!")

# # # Show reminders
# # with st.expander("📋 My Reminders"):
# #     reminders = load_reminders()
# #     if reminders:
# #         for r in reminders:
# #             st.markdown(f"• {r['text']} <small>({r['time']})</small>", unsafe_allow_html=True)
# #     else:
# #         st.write("No reminders yet.")
