document.addEventListener('DOMContentLoaded', function () {
    // Function to apply the correct theme based on preference or system setting
    function applyTheme(theme) {
        const themeStylesheet = document.getElementById('themeStylesheet');
        const sunIcon = document.querySelectorAll('#sunIcon, #sunIconMobile');
        const moonIcon = document.querySelectorAll('#moonIcon, #moonIconMobile');
        
        if (theme === 'dark') {
            themeStylesheet.setAttribute('href', 'style.css');
            sunIcon.forEach(icon => icon.classList.add('d-none'));
            moonIcon.forEach(icon => icon.classList.remove('d-none'));
        } else {
            themeStylesheet.setAttribute('href', 'light.css');
            sunIcon.forEach(icon => icon.classList.remove('d-none'));
            moonIcon.forEach(icon => icon.classList.add('d-none'));
        }
        localStorage.setItem('theme', theme);
    }

    // Event listeners for theme toggle
    document.querySelectorAll('#sunIcon, #sunIconMobile').forEach(icon => {
        icon.addEventListener('click', function () {
            applyTheme('dark');
        });
    });

    document.querySelectorAll('#moonIcon, #moonIconMobile').forEach(icon => {
        icon.addEventListener('click', function () {
            applyTheme('light');
        });
    });

    // Load the user's theme preference on page load
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        applyTheme(savedTheme);
    } else {
        const prefersDarkScheme = window.matchMedia("(prefers-color-scheme: dark)").matches;
        applyTheme(prefersDarkScheme ? 'dark' : 'light');
    }

    // Sidebar toggle
    document.querySelector('.slogo').addEventListener('click', function () {
        document.querySelector('.sidebar').classList.toggle('show');
    });

    document.querySelector('.hamburger').addEventListener('click', function () {
        document.querySelector('.sidebar').classList.toggle('show');
    });
});
