import streamlit as st

from utils.utils import get_tasks, save_task, Task, TaskStatus

# Inicializa el estado de la sesión
if "tasks" not in st.session_state:
    st.session_state["tasks"] = get_tasks()
if "editing_task" not in st.session_state:
    st.session_state["editing_task"] = None


def add_task(title: str, description: str):
    new_id = len(st.session_state["tasks"]) + 1
    task = Task(
        id=new_id,
        title=title,
        description=description,
    )
    
    st.session_state.tasks.append(task.model_dump())
    save_task(st.session_state.tasks)

def update_task_status(task_id: int, new_status: TaskStatus):
    """Actualiza el estado de una tarea y vuelve a guardar el archivo."""
    for task in st.session_state.tasks:
        if task["id"] == task_id:
            task["status"] = new_status.value
            save_task(st.session_state.tasks)
            st.rerun()
            break

def delete_task(task_id: int):
    st.session_state.tasks = [task for task in st.session_state.tasks if task["id"] != task_id]
    save_task(st.session_state.tasks)
    st.rerun()

def edit_task(task_id: int, new_title: str, new_description: str):
    for task in st.session_state.tasks:
        if task["id"] == task_id:
            task["title"] = new_title
            task["description"] = new_description
            save_task(st.session_state.tasks)
            st.session_state["editing_task"] = None
            st.rerun()
            break
            
# --- Nuevas funciones de callback para los botones ---
def handle_add_task():
    """Maneja el clic del botón Agregar y limpia el formulario."""
    title = st.session_state["add_task_title_input"]
    description = st.session_state["add_task_description_input"]

    if title and description:
        add_task(title, description)
        st.session_state["add_task_title_input"] = ""  # Limpia después de agregar
        st.session_state["add_task_description_input"] = ""
        st.success("Tarea añadida con éxito!")
    else:
        st.warning("Por favor, ingresa un título y una descripción.")

def handle_clear_form():
    """Limpia los campos del formulario."""
    st.session_state["add_task_title_input"] = ""
    st.session_state["add_task_description_input"] = ""
# --- Fin de las nuevas funciones de callback ---

def show_add_form():
    with st.expander("Agregar tarea", expanded=True):
        st.text_input("Título", key="add_task_title_input")
        st.text_area("Descripción", key="add_task_description_input")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.button("Agregar", on_click=handle_add_task)
        
        with col2:
            st.button("Limpiar", on_click=handle_clear_form)

def show_tasks_by_status(status: TaskStatus):
    tasks_to_display = [task for task in st.session_state.tasks if task["status"] == status.value]
    
    for task_data in tasks_to_display:
        if st.session_state.get("editing_task") == task_data["id"]:
            with st.form(key=f"edit_form_{task_data['id']}", border=True):
                new_title = st.text_input("Título", value=task_data["title"], key=f"edit_title_{task_data['id']}")
                new_description = st.text_area("Descripción", value=task_data["description"], key=f"edit_desc_{task_data['id']}")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.form_submit_button("Guardar"):
                        edit_task(task_data["id"], new_title, new_description)
                with col2:
                    if st.form_submit_button("Cancelar"):
                        st.session_state["editing_task"] = None
                        st.rerun()
        else:
            with st.expander(f"**{task_data['title']}**"):
                st.markdown(f"_{task_data['description']}_")
                st.write(f"ID: {task_data['id']}")
                st.write(f"Creada: {task_data['timestamp']}")
                
                st.write("---") # Separador para los botones
                
                # Botones de control de estado (se muestran según el estado de la tarea)
                if status == TaskStatus.PENDING:
                    if st.button("▶️ Mover a En Progreso", key=f"to_progress_{task_data['id']}"):
                        update_task_status(task_data['id'], TaskStatus.IN_PROGRESS)
                    if st.button("✅ Mover a Completado", key=f"to_completed_from_pending_{task_data['id']}"):
                        update_task_status(task_data['id'], TaskStatus.COMPLETED)
                
                elif status == TaskStatus.IN_PROGRESS:
                    if st.button("✅ Mover a Completado", key=f"to_completed_{task_data['id']}"):
                        update_task_status(task_data['id'], TaskStatus.COMPLETED)
                    if st.button("❌ Mover a Pendiente", key=f"to_pending_{task_data['id']}"):
                        update_task_status(task_data['id'], TaskStatus.PENDING)
                
                elif status == TaskStatus.COMPLETED:
                    if st.button("⏪ Mover a Pendiente", key=f"to_pending_{task_data['id']}"):
                        update_task_status(task_data['id'], TaskStatus.PENDING)

                # Botones de acción (Editar y Eliminar)
                st.write("---") # Separador para los botones de acción
                if st.button("✏️ Editar Tarea", key=f"edit_{task_data['id']}"):
                    st.session_state["editing_task"] = task_data["id"]
                    st.rerun()
                if st.button("🗑️ Eliminar Tarea", key=f"delete_{task_data['id']}"):
                    delete_task(task_data['id'])


def show_tasks():
    st.subheader("Tareas")
    col_pending, col_in_progress, col_completed = st.columns(3)

    with col_pending:
        st.markdown("<h3 style='text-align: center;'>Pendientes</h3>", unsafe_allow_html=True)
        show_tasks_by_status(TaskStatus.PENDING)

    with col_in_progress:
        st.markdown("<h3 style='text-align: center;'>En Progreso</h3>", unsafe_allow_html=True)
        show_tasks_by_status(TaskStatus.IN_PROGRESS)

    with col_completed:
        st.markdown("<h3 style='text-align: center;'>Completadas</h3>", unsafe_allow_html=True)
        show_tasks_by_status(TaskStatus.COMPLETED)

def main():
    st.header("To-Do App")
    show_add_form()
    show_tasks()

if __name__ == "__main__":
    main()