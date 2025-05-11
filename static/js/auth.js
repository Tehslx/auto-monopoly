document.addEventListener("DOMContentLoaded", () => {
    // Обработка формы авторизации
    document.getElementById("auth-form").addEventListener("submit", async (event) => {
        event.preventDefault();

        const nickname = document.getElementById("auth-form-nick").value.trim();
        const password = document.getElementById("auth-form-password").value;

        if (password.length < 10) {
            alert("Ошибка: пароль слишком короткий.");
            return;
        }

        try {
            const response = await fetch("/api/auth", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ nickname, password })
            });

            const data = await response.json();

            if (data.success) {
                localStorage.setItem("access_token", data.token);
                window.location.href = "/games";
            } else {
                alert("Ошибка: " + (data.message || "Неверный логин или пароль."));
            }
        } catch (error) {
            alert("Ошибка сети. Попробуйте позже.");
        }
    });

    // Обработка формы регистрации
    document.getElementById("reg-form").addEventListener("submit", async (event) => {
        event.preventDefault();

        const nickname = document.getElementById("reg-form-nick").value.trim();
        const password = document.getElementById("reg-form-password").value;
        const passwordRetype = document.getElementById("reg-form-password_retype").value;

        // Валидация
        if (password.length < 10) {
            alert("Ошибка: пароль слишком короткий.");
            return;
        }
        if (password !== passwordRetype) {
            alert("Ошибка: пароли не совпадают.");
            return;
        }
        if (nickname.length < 2 || nickname.length > 20) {
            alert("Ошибка: никнейм должен быть от 2 до 20 символов.");
            return;
        }

        try {
            const response = await fetch("/api/register", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ nickname, password })
            });

            const data = await response.json();

            if (data.success) {
                localStorage.setItem("access_token", data.token);
                window.location.href = "/profile";
            } else {
                alert("Ошибка: " + (data.message || "Регистрация не удалась."));
            }
        } catch (error) {
            alert("Ошибка сети. Попробуйте позже.");
        }
    });
});