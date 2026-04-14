from flask import render_template, request, redirect, url_for
from app import app
import random
import logging

logger = logging.getLogger("my_app")

# Список шуток (Доп. задание 1)
JOKES = [
    "Почему программисты не любят природу? Там слишком много багов.",
    "В мире есть 10 типов людей: те, кто понимают двоичную систему, и те, кто нет.",
    "Программист - это организм, который превращает кофе в код.",
    "- Папа, а почему солнце встает на востоке? - Работает? Не трогай!"
]


@app.route("/")
def form():
    logger.info("Пользователь зашел на главную страницу")
    return render_template("form.html")


@app.route("/submit", methods=["POST", "GET"])
def submit():
    if request.method == "POST":
        # Получаем имя из формы
        name = request.form.get("name")
        # Получаем email из формы
        email = request.form.get("email")

        # --- Новые поля из задания 1 ---
        color = request.form.get("color")
        profession = request.form.get("profession")
        # Список для чекбоксов
        hobbies = request.form.getlist("hobbies")
        level = request.form.get("level")

        logger.info(f"Получена форма от пользователя: {name} ({email})")

        # --- Проверка формы (Доп. задание 3) ---
        if not name or name.strip() == "":
            logger.warning(f"Ошибка валидации: имя не введено. Данные: {request.form}")
            return render_template("error.html",
                                   message="Мы не можем обработать форму без Вашего имени, Мистер Аноним!"), 400
        joke = random.choice(JOKES)

        logger.info(f"Результат успешно сформирован для {name}")

        return render_template("result.html", name=name, email=email,
                               color=color, profession=profession, hobbies=hobbies, level=level, joke=joke)
    else:
        # Если запрос GET, возвращаем на форму
        logger.info("Перенаправление с GET-запроса на главную страницу")
        return redirect(url_for("form"))


@app.errorhandler(404)
def page_for_found(e):
    logger.error(f"Ошибка 404: Пользователь пытался перейти на {request.path}")
    return render_template("error.html", message="Упс! Страница потерялась в космосе."), 404


@app.errorhandler(500)
def internal_server_error(e):
    logger.critical(f"ОШИБКА 500: {str(e)}", exc_info=True)
    return render_template("error.html", message="Наш сервер приуныл.")