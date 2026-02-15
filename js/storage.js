function getTasks() {
    return JSON.parse(localStorage.getItem("zero_tasks")) || [];
}

function saveTasks(tasks) {
    localStorage.setItem("zero_tasks", JSON.stringify(tasks));
}
function checkNewDay() {
    const today = new Date().toISOString().split("T")[0]; 
    const savedDate = localStorage.getItem("zero_last_date");

    // ถ้าไม่มีวันที่เก็บไว้ หรือ วันที่ไม่ตรง
    if (!savedDate || savedDate !== today) {
        localStorage.setItem("zero_tasks", JSON.stringify([]));
        localStorage.setItem("zero_last_date", today);
    }
}
