const THEME_KEY = "theme";
const prefersDark = window.matchMedia("(prefers-color-scheme: dark)");

function getStoredTheme() {
  try {
    const stored = localStorage.getItem(THEME_KEY);
    return stored === "light" || stored === "dark" ? stored : null;
  } catch (e) {
    return null;
  }
}

function setStoredTheme(theme) {
  try {
    localStorage.setItem(THEME_KEY, theme);
  } catch (e) {
    // Ignore storage failures (e.g. private browsing).
  }
}

function currentTheme() {
  return document.documentElement.dataset.theme === "dark" ? "dark" : "light";
}

function applyTheme(theme) {
  const isDark = theme === "dark";
  document.documentElement.dataset.theme = theme;

  document.querySelectorAll("[data-theme-toggle]").forEach((button) => {
    const label = isDark ? "Switch to light mode" : "Switch to dark mode";
    button.setAttribute("aria-pressed", String(isDark));
    button.setAttribute("aria-label", label);
    button.setAttribute("title", label);
  });
}

function initTheme() {
  const stored = getStoredTheme();
  applyTheme(stored || (prefersDark.matches ? "dark" : "light"));

  document.querySelectorAll("[data-theme-toggle]").forEach((button) => {
    button.addEventListener("click", () => {
      const next = currentTheme() === "dark" ? "light" : "dark";
      setStoredTheme(next);
      applyTheme(next);
    });
  });

  const onSystemThemeChange = (event) => {
    if (!getStoredTheme()) {
      applyTheme(event.matches ? "dark" : "light");
    }
  };

  if (typeof prefersDark.addEventListener === "function") {
    prefersDark.addEventListener("change", onSystemThemeChange);
  } else if (typeof prefersDark.addListener === "function") {
    prefersDark.addListener(onSystemThemeChange);
  }
}

document.addEventListener("DOMContentLoaded", () => {
  initTheme();

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
