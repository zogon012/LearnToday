import streamlit as st

st.set_page_config(page_title="Todo", page_icon="📋")
import requests
import os
import time

API_URL = os.getenv("API_URL", "http://web:8000/todos/")

# React-style custom CSS (타이틀 포함)
st.markdown(
    """
    <style>
    .big-title {
        font-size: 2.8rem;
        font-weight: 900;
        background: linear-gradient(90deg, #4f8cff 30%, #38d9a9 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 2px 2px 8px rgba(79,140,255,0.08);
        margin-bottom: 2rem;
        letter-spacing: -2px;
        display: flex;
        align-items: center;
        gap: 0.7rem;
    }
    .todo-icon {
        font-size: 2.2rem;
        vertical-align: middle;
    }
    .todo-box {
        background: #f8f9fa;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }
    .todo-item {
        font-size: 1.2rem;
        padding: 0.5rem 0;
        border-bottom: 1px solid #e0e0e0;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .todo-item:last-child {
        border-bottom: none;
    }
    .done {
        color: #adb5bd;
        text-decoration: line-through;
    }
    .todo-btn {
        background: #4f8cff;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 0.3rem 1.5rem;
        margin-left: 0.7rem;
        font-size: 1rem;
        cursor: pointer;
        transition: background 0.2s;
        min-width: 90px;
    }
    .todo-btn.delete {
        background: #ff6b6b;
    }
    .todo-btn:active {
        background: #1c5ed6;
    }
    </style>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="big-title">
        <span class="todo-icon">📋</span>
        Todo
    </div>
""",
    unsafe_allow_html=True,
)

# Add todo
with st.form(key="add_todo_form"):
    new_todo = st.text_input("Add new todo", key="new_todo")
    submitted = st.form_submit_button("Add")
    if submitted:
        if not new_todo.strip():
            st.error("Please enter a todo!")
        else:
            resp = requests.post(API_URL, json={"title": new_todo})
            if resp.status_code == 201:
                st.toast("Added!", icon="🟢")
            else:
                st.error("Failed to add!")
            time.sleep(0.7)
            st.rerun()
            # st.stop()

# Get todos
resp = requests.get(API_URL)
todos = resp.json() if resp.status_code == 200 else []

st.markdown(
    '<div class="big-title" style="font-size:1.5rem; margin-top:2rem;">Todo</div>',
    unsafe_allow_html=True,
)

st.markdown('<div class="todo-box">', unsafe_allow_html=True)
for todo in todos:
    is_done = todo.get("is_done", False)
    title_html = (
        f"<span class='done'>{todo['title']}</span>" if is_done else todo["title"]
    )
    btn_key = f"done_{todo['id']}" if not is_done else f"undo_{todo['id']}"
    btn_label = "Done" if not is_done else "Undo"
    col1, col2, col3 = st.columns([8, 1.5, 1.5])
    with col1:
        st.markdown(
            f'<div class="todo-item">{title_html}</div>', unsafe_allow_html=True
        )
    with col2:
        if st.button(btn_label, key=btn_key):
            update_data = {
                "title": todo.get("title", ""),
                "description": todo.get("description", ""),
                "is_done": not is_done,
            }
            requests.put(f"{API_URL}{todo['id']}", json=update_data)
            if not is_done:
                st.toast("Marked as done!", icon="✔️")
            else:
                st.toast("Marked as todo!", icon="🔁")
            time.sleep(0.3)
            st.rerun()
            # st.stop()
    with col3:
        if st.button("Delete", key=f"delete_{todo['id']}"):
            requests.delete(f"{API_URL}{todo['id']}")
            st.toast("Deleted!", icon="❌")
            time.sleep(0.3)
            st.rerun()
            # st.stop()
st.markdown("</div>", unsafe_allow_html=True)
