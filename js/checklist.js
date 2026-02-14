function renderTasks() {
    const container = document.getElementById("scheduleContainer");
    if (!container) return;

    container.innerHTML = "";
    const tasks = getTasks();

    tasks.forEach((task, index) => {

        // ไม่แสดง task ที่ completed แล้ว
        if (task.completed) return;

        const li = document.createElement("li");
        li.className = "time-block task-item";

        li.innerHTML = `
            <span class="time">${task.time || "-"}</span>
            <span class="task">${task.title}</span>

            <div class="task-actions">
                <button class="check-btn">
                    <i data-lucide="check"></i>
                </button>
                <button class="delete-btn">
                    <i data-lucide="trash-2"></i>
                </button>
            </div>
        `;

        // ✔ ติ๊กเสร็จ → หายทันที
        li.querySelector(".check-btn").addEventListener("click", (e) => {
            e.stopPropagation();
            tasks[index].completed = true;
            saveTasks(tasks);
            renderTasks();
        });

        // 🗑 ลบกิจกรรม
        li.querySelector(".delete-btn").addEventListener("click", (e) => {
            e.stopPropagation();
            tasks.splice(index, 1);
            saveTasks(tasks);
            renderTasks();
        });

        container.appendChild(li);
    });

    updateStats();
    lucide.createIcons();
}

function addTask(title, time) {
    const tasks = getTasks();

    tasks.push({
        title: title,
        time: time,
        completed: false
    });

    saveTasks(tasks);
    renderTasks();
}

function updateStats() {
    const tasks = getTasks();

    const total = tasks.length;
    const completed = tasks.filter(t => t.completed).length;
    const percent = total === 0 ? 0 : Math.round((completed / total) * 100);

    document.getElementById("totalTasks").textContent = total;
    document.getElementById("completedTasks").textContent = completed;
    document.getElementById("progressPercent").textContent = percent + "%";
    document.getElementById("progressFill").style.width = percent + "%";
}

/* ===============================
   รีเซ็ตอัตโนมัติเมื่อขึ้นวันใหม่
================================= */

function checkNewDay() {
    const today = new Date().toISOString().split("T")[0];
    const savedDate = localStorage.getItem("zero_last_date");

    if (!savedDate || savedDate !== today) {
        localStorage.setItem("zero_tasks", JSON.stringify([]));
        localStorage.setItem("zero_last_date", today);
    }
}

document.addEventListener("DOMContentLoaded", () => {
    checkNewDay();   // 👈 เช็ควันก่อนทุกครั้ง
    renderTasks();
});
