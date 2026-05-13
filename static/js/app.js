const mobileMenu = document.getElementById("mobileMenu");
const navLinks = document.getElementById("navLinks");
const darkToggle = document.getElementById("darkToggle");

if (mobileMenu) {
    mobileMenu.addEventListener("click", () => {
        navLinks.classList.toggle("open");
    });
}

function setDarkMode(enabled) {
    if (enabled) {
        document.body.classList.add("dark");
        darkToggle.textContent = "Light";
    } else {
        document.body.classList.remove("dark");
        darkToggle.textContent = "Dark";
    }
}

if (darkToggle) {
    const storedMode = localStorage.getItem("devops-dark-mode");
    const darkMode = storedMode === "true";
    setDarkMode(darkMode);

    darkToggle.addEventListener("click", () => {
        const isDark = document.body.classList.contains("dark");
        setDarkMode(!isDark);
        localStorage.setItem("devops-dark-mode", String(!isDark));
    });
}
