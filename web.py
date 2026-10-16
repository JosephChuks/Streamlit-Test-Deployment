import streamlit as st
import functions
import socket

st.set_page_config(page_title="Todo", page_icon="🌐", layout="centered")

hostname = socket.gethostname()
ip = socket.gethostbyname(hostname)
todos = functions.get_todos()
# st.session_state["selected"] = []


def add_todo():
    todo = st.session_state["new_todo"] + "\n"
    if todo:
        todos.append(todo)
        functions.write_todos(todos)
        st.session_state["new_todo"] = ""


def delete_todo(task):
    todo = st.session_state[task]
    if todo:
        id, task = todo.split("_")
        id = int(id)
        todos.pop(id)
        del st.session_state[todo]
        functions.write_todos(todos)


def complete_todo():
    marked = [
        key
        for key in st.session_state
        if key.startswith("todos_") and st.session_state[key]
    ]

    if not marked:
        st.toast("Please select at least 1 task", icon="⚠️", duration="short")
        return

    indices = sorted((int(key.split("_", 2)[1]) for key in marked), reverse=True)
    for i in indices:
        todos.pop(i)

    for key in marked:
        del st.session_state[key]

    functions.write_todos(todos)
    st.toast("Task completed successfully", icon="✅", duration="short")


st.title("🌐 My To-Do List")
st.subheader("Keep track of your tasks and stay organized.")
st.write("This is a simple to-do list application built with Streamlit.")

st.html("<hr>")

for index, todo in enumerate(todos):
    checkbox = st.checkbox(todo, key=f"todos_{index}_{todo}")
    # if checkbox:
    #     st.session_state["selected"] = [f"{index}_{todo}"]

st.html("<hr>")

col1, col2 = st.columns([0.1, 0.9], gap="small", vertical_alignment="center")
with col1:
    st.button("Edit", key="Edit")

with col2:
    st.button("Complete", key="Complete", on_click=complete_todo)


st.text_input(
    "",
    key="new_todo",
    placeholder="Add new task here...",
    on_change=add_todo,
)

st.html(f"""
    <div style="font-size: 12px; color: gray; margin-top: 20px;">
       <b style='color:gold'>Hostname/IP:</b> {hostname}: {ip}
    </div>
""")

st.session_state
