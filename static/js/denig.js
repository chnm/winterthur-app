document.addEventListener("DOMContentLoaded", function () {
    const menuToggle = document.getElementById("menu-toggle");
    const mobileMenu = document.getElementById("mobile-menu");
    const hamburgerIcon = document.getElementById("hamburger-icon");
    const closeIcon = document.getElementById("close-icon");

    if (menuToggle) {
        menuToggle.addEventListener("click", function () {
            mobileMenu.classList.toggle("hidden");
            hamburgerIcon.classList.toggle("hidden");
            closeIcon.classList.toggle("hidden");
        });
    } else {
        console.error("Menu toggle button not found");
    }
});
