// ===== ZERO TASK SYSTEM =====

const TASK_KEY = "zero_tasks";

// ดึง task จาก localStorage
function getTasks() {
    return JSON.parse(localStorage.getItem(TASK_KEY)) || [];
}

// บันทึก task
function saveTasks(tasks) {
    localStorage.setItem(TASK_KEY, JSON.stringify(tasks));
}

// เพิ่ม task
function addTask(title, time) {
    const tasks = getTasks();

    const newTask = {
        id: Date.now(),
        title: title,
        time: time || "",
        completed: false
    };

    tasks.push(newTask);
    saveTasks(tasks);
    renderTasks();
}


// toggle เสร็จ/ไม่เสร็จ
function toggleTask(id) {
    const tasks = getTasks();

    const updated = tasks.map(task =>
        task.id === id
            ? { ...task, completed: !task.completed }
            : task
    );

    saveTasks(updated);
    renderTasks();
}

// ลบ task
function deleteTask(id) {
    const tasks = getTasks().filter(task => task.id !== id);
    saveTasks(tasks);
    renderTasks();
}

// render task
function renderTasks() {
    const container = document.getElementById("scheduleContainer");
    const tasks = getTasks();

    container.innerHTML = "";

    tasks.forEach(task => {
        const div = document.createElement("div");
        div.className = "time-block";

    div.innerHTML = `
    <div style="display:flex; justify-content:space-between; width:100%;">
        <span class="task ${task.completed ? 'done' : ''}">
            ${task.title}
        </span>

        ${task.time ? `<span class="task-time">${task.time} น.</span>` : ""}
    </div>

    <div>
        <button onclick="toggleTask(${task.id})">✔</button>
        <button onclick="deleteTask(${task.id})">🗑</button>
    </div>
`;


        container.appendChild(div);
    });

    updateProgress();
}
