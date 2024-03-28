document.addEventListener("DOMContentLoaded", function () {
    document
        .getElementById("hamburger-menu")
        .addEventListener("click", function () {
            const dropdownMenu = document.getElementById("dropdown-menu");
            dropdownMenu.classList.toggle("hidden");
        });
});
