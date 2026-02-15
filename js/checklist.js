function renderTasks() {
    const container = document.getElementById("scheduleContainer");
    if (!container) return;

    container.innerHTML = "";
    const tasks = getTasks();

    tasks.forEach((task, index) => {

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

        li.querySelector(".check-btn").addEventListener("click", (e) => {
            e.stopPropagation();
            tasks[index].completed = true;
            saveTasks(tasks);
            renderTasks();
        });

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

    /* ===============================
       ส่งแจ้งเตือนเข้า LINE ตอนเพิ่ม
    ================================= */

    fetch("http://127.0.0.1:5000/send-line", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            message: `📌 เพิ่มกิจกรรมใหม่\n${title}\nเวลา ${time}`
        })
    }).catch(err => console.log("LINE Error:", err));
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


/* ===============================
   ระบบแจ้งเตือนเมื่อถึงเวลา
================================= */

if ("Notification" in window) {
    Notification.requestPermission();
}

let notifiedTasks = new Set();

setInterval(() => {

    const tasks = getTasks();
    const now = new Date();
    const currentTime = now.toTimeString().slice(0, 5);

    tasks.forEach(task => {

        if (!task.completed && task.time === currentTime) {

            const uniqueKey = task.title + task.time;

            if (!notifiedTasks.has(uniqueKey)) {

                // แจ้งเตือนใน Browser
                if (Notification.permission === "granted") {
                    new Notification("ถึงเวลาแล้ว!", {
                        body: `${task.title} - ${task.time}`
                    });
                }

                // ส่งเข้า LINE ตอนถึงเวลา
                fetch("https://line-backend-53y1.onrender.com", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        message: `⏰ ถึงเวลาแล้ว!\n${task.title}\nเวลา ${task.time}`
                    })
                }).catch(err => console.log("LINE Error:", err));

                notifiedTasks.add(uniqueKey);
            }
        }
    });

}, 1000);


document.addEventListener("DOMContentLoaded", () => {
    checkNewDay();
    renderTasks();
});
