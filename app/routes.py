from flask import render_template, request, redirect, url_for
from app import app
import random

# Список шуток (Доп. задание 1)
JOKES = [
    "Почему программисты не любят природу? Там слишком много багов.",
    "В мире есть 10 типов людей: те, кто понимают двоичную систему, и те, кто нет.",
    "Программист - это организм, который превращает кофе в код.",
    "- Папа, а почему солнце встает на востоке? - Работает? Не трогай!"
]


@app.route("/")
def form():
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

        # --- Проверка формы (Доп. задание 3) ---
        if not name or name.strip() == "":
            return render_template("error.html",
                                   message="Мы не можем обработать форму без Вашего имени, Мистер Аноним!"), 400
        joke = random.choice(JOKES)

        return render_template("result.html", name=name, email=email,
                               color=color, profession=profession, hobbies=hobbies, level=level, joke=joke)
    else:
        # Если запрос GET, возвращаем на форму
        return redirect(url_for("form"))