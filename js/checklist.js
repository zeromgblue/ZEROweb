// js/checklist.js

const taskInput = document.getElementById("taskInput");
const addTaskBtn = document.getElementById("addTaskBtn");
const taskList = document.getElementById("taskList");

let tasks = getTasks();

/* =========================
   Render Tasks
========================= */
function renderTasks() {
    taskList.innerHTML = "";

    tasks.forEach(task => {
        const li = document.createElement("li");
        li.className = "task-item";
        li.dataset.id = task.id;

        if (task.done) {
            li.classList.add("done");
        }

        li.innerHTML = `
            <label>
                <input 
                    type="checkbox" 
                    class="task-checkbox"
                    ${task.done ? "checked" : ""}
                />
                <span class="task-text">${task.text}</span>
            </label>
        `;

        const checkbox = li.querySelector(".task-checkbox");

        checkbox.addEventListener("change", () => {
            toggleTask(task.id);
        });

        taskList.appendChild(li);
    });
}

/* =========================
   Add Task
========================= */
function addTask() {
    const text = taskInput.value.trim();
    if (!text) return;

    const newTask = {
        id: Date.now(),
        text,
        done: false
    };

    tasks.push(newTask);
    saveTasks(tasks);
    renderTasks();

    taskInput.value = "";
}

/* =========================
   Toggle Task
========================= */
function toggleTask(id) {
    tasks = tasks.map(task =>
        task.id === id
            ? { ...task, done: !task.done }
            : task
    );

    saveTasks(tasks);
    renderTasks();
}

/* =========================
   Events
========================= */
addTaskBtn.addEventListener("click", addTask);

taskInput.addEventListener("keydown", e => {
    if (e.key === "Enter") {
        addTask();
    }
});

/* =========================
   Init
========================= */
renderTasks();
