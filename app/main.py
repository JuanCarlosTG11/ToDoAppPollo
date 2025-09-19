import streamlit as st



from utils.utils import get_tasks, save_task, Task

if "tasks" not in st.session_state:
    st.session_state["tasks"] = get_tasks()


def add_task(title:str, description:str):
    task = Task(
        id=len(st.session_state["tasks"]) + 1,
        title=title,
        description=description
    )

    st.session_state.tasks.append(task.model_dump())
    save_task(st.session_state.tasks)
   

def show_add_form():
    with st.expander("Te Amo", expanded=True):
        title = st.text_input("AJJAJAA Hola we")
        description = st.text_area("KKKKKKK")

        if st.button("Añade we"):
            add_task(title, description)
            st.success("Añadida We")
            st.experimental_rerun()

    


def main():

    st.header("To-Do App")
    show_add_form()



if __name__ == "__main__":
    main()