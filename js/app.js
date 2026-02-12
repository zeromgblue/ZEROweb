// js/app.js

document.addEventListener("DOMContentLoaded", () => {

    // โหลด task ถ้ามีหน้า checklist
    if (typeof renderTasks === "function") {
        renderTasks();
    }

    // ถ้าอยู่หน้า summary ให้แสดง progress
    if (document.getElementById("progressPercent")) {
        renderProgress();
    }

});
