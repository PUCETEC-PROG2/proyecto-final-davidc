const themes = [
    {
        background: "#f8f3f3",
        color: "#222222",
        primaryColor: "#20B2AA"
    },
    {
        name: "Gris Intenso",
        background: "#e0e0e0", // Un gris más marcado
        color: "#333333",      // Texto en gris oscuro para buen contraste
        primaryColor: "#80CBC4" // Conservando el tono suave de teal
    },
    {
        name: "Menta Vistosa",
        background: "#A8E6CF", // Fondo mint más vibrante
        color: "#004D40",      // Texto en verde oscuro para buen contraste
        primaryColor: "#26A69A"
    },
    {
        name: "Oscuro Gris",
        background: "#2C2C2C",  // Gris oscuro
        color: "#FFFFFF",
        primaryColor: "#40E0D0"
    },

    
    
    
];

const setTheme = (theme) => {
    const root = document.querySelector(":root");
    root.style.setProperty("--background", theme.background);
    root.style.setProperty("--color", theme.color);
    root.style.setProperty("--primary-color", theme.primaryColor);
    root.style.setProperty("--glass-color", theme.glassColor);
};

const displayThemeButtons = () => {
    const btnContainer = document.querySelector(".theme-btn-container");
    themes.forEach((theme) => {
        const div = document.createElement("div");
        div.className = "theme-btn";
        div.style.cssText = `background: ${theme.background}; width: 25px; height: 25px`;
        btnContainer.appendChild(div);
        div.addEventListener("click", () => setTheme(theme));
    });
};

displayThemeButtons();

function changeTheme(theme) {
    fetch(`/set-theme/${theme}/`)  // Llama a la vista de Django para guardar la preferencia
    .then(() => {
        let themeFile = theme === "dark" ? "dark-theme.css" : "light-theme.css";
        document.getElementById("theme-link").href = themeFile;
    });
}