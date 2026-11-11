document.addEventListener("DOMContentLoaded", () => {
  const burger = document.querySelector(".burger-menu");
  const sidebar = document.querySelector(".sidebar");

  if (burger && sidebar) {
    burger.addEventListener("click", () => {
      sidebar.classList.toggle("active");
    });

    document.addEventListener("click", (e) => {
      if (window.innerWidth <= 768) {
        if (
          !sidebar.contains(e.target) &&
          !burger.contains(e.target) &&
          sidebar.classList.contains("active")
        ) {
          sidebar.classList.remove("active");
        }
      }
    });
  }
});
