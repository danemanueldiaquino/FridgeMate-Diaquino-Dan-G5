const menuButton = document.querySelector(".mobile-menu-button");
const sidebar = document.querySelector(".sidebar");
const scrim = document.querySelector(".mobile-scrim");

function closeMenu() {
    if (!sidebar || !menuButton) return;
    sidebar.classList.remove("is-open");
    document.body.classList.remove("menu-open");
    menuButton.setAttribute("aria-expanded", "false");
}

if (menuButton && sidebar) {
    menuButton.addEventListener("click", () => {
        const isOpen = sidebar.classList.toggle("is-open");
        document.body.classList.toggle("menu-open", isOpen);
        menuButton.setAttribute("aria-expanded", String(isOpen));
    });
    if (scrim) scrim.addEventListener("click", closeMenu);
    sidebar.querySelectorAll("a").forEach((link) => link.addEventListener("click", closeMenu));
}

const dateElement = document.querySelector("#today-date");
if (dateElement) {
    dateElement.textContent = new Intl.DateTimeFormat(undefined, {
        weekday: "long",
        month: "long",
        day: "numeric",
    }).format(new Date());
}

document.querySelectorAll("[data-preview-action]").forEach((button) => {
    button.addEventListener("click", () => {
        const feedback = document.querySelector(".demo-toast");
        if (!feedback) return;
        feedback.textContent = "Inventory and member tools are a visual preview — they are not connected to your account yet.";
        feedback.classList.add("is-visible");
        window.setTimeout(() => feedback.classList.remove("is-visible"), 4200);
    });
});
