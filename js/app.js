const nav = document.querySelector(".top-nav");

window.addEventListener("scroll", () => {
    if (window.scrollY > 20) {
        nav.classList.add("scrolled");
    } else {
        nav.classList.remove("scrolled");
    }
});
