function getTasks() {
    return JSON.parse(localStorage.getItem("zero_tasks")) || [];
}

function saveTasks(tasks) {
    localStorage.setItem("zero_tasks", JSON.stringify(tasks));
}
