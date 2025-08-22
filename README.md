# 🤖 Проєкт "Telegram/ChatGPT"

Телеграм-бот із підключенням **ChatGPT**. Виконано 4 обов’язкові пункти та 2 пункти на вибір. Код відповідає [PEP8](https://peps.python.org/pep-0008/), є логування, змінні середовища, та інші покращення.

---

## ✅ Виконані умови

- Проєкт представляє собою Telegram-бота з підключенням ChatGPT.
- У проєкті реалізовані функціональності з **4 обов'язкових пунктів** та **2 пунктів на вибір**.
- Код проєкту відповідає стандарту [PEP8](https://peps.python.org/pep-0008/).
- Код відмовостійкий.
- Використано будь-яку бібліотеку для Telegram API.

### Додаткові плюси:
- Наявність файлу **README**
- Наявність файлу **requirements.txt**
- Використання **ConversationHandler**
- Використання **змінних середовища** (для зберігання токенів)
- **Логування**
- **Розгортання** проєкту на сервері (ngrok, pythonanywhere, glitch або ін.)
- Використання технологій, які **не розглядалися** в першому модулі

---

## 🧩 Завдання

### 0. 🔐 Винесено токен в окремий файл
- Токен додано до **.gitignore**.

---

### 1. 🎲 "Випадковий факт" (`/random`)
Телеграм-бот обробляє команду **/random**: надсилає підготовлене зображення, робить запит до ChatGPT за підготовленим промптом, повертає відповідь. Додаються кнопки:
- **"Закінчити"** — працює як команда `/start`
- **"Хочу ще факт"** — працює як команда `/random`

<p align="center">Скріншоти</p>

<div align="center">

<table border="1" cellpadding="6">
  <tr>
    <td><img src="https://github.com/user-attachments/assets/b086c16d-ad84-43eb-8a1e-83cde7226b30" width="360" alt="Start_запуск_бота"></td>
    <td><img src="https://github.com/user-attachments/assets/66eb8bab-9db5-493e-a4cf-f1ff55589bf1" width="360" alt="Рандомні факти"></td>
  </tr>
</table>

</div>

---

### 2. 💬 "ChatGPT інтерфейс" (`/gpt`)
Бот надсилає підготовлене зображення та робить запит до ChatGPT, передаючи текст отриманого повідомлення. Відповідь надсилається користувачеві текстом.

<p align="center">Скріншоти</p>

<div align="center">

<table border="1" cellpadding="6">
  <tr>
    <td><img src="https://github.com/user-attachments/assets/a95819e8-5342-4f43-b663-391fa590cd60" width="320" alt="Старт роботи з чатом-gpt"></td>
    <td><img src="https://github.com/user-attachments/assets/2a4e6414-8ad0-4966-ac2c-1de0f69ea38f" width="320" alt="Питання до чату"></td>
    <td><img src="https://github.com/user-attachments/assets/1f50620b-943d-406a-938e-806acc9a1ea5" width="320" alt="Друге питання до чату"></td>
  </tr>
</table>

</div>

---

### 3. 🗣️ "Діалог з відомою особистістю" (`/talk`)
Бот надсилає підготовлене зображення та пропонує вибір відомих особистостей (кнопки). Після вибору — застосовується відповідний промпт. Подальші повідомлення користувача передаються ChatGPT та повертаються відповіді. Є кнопка **"Закінчити"** (як `/start`).

<p align="center">Скріншоти</p>

<div align="center">

<table border="1" cellpadding="6">
  <tr>
    <td><img src="https://github.com/user-attachments/assets/c3c89c0f-44e9-41cd-973f-ec6e29f3fe45" width="320" alt="Леся Українка"></td>
    <td><img src="https://github.com/user-attachments/assets/38fea662-d0ec-449f-ba9c-aed0c7f03497" width="320" alt="Марі Кюрі"></td>
    <td><img src="https://github.com/user-attachments/assets/5bdf4145-b109-4179-a912-fe9eafa05c10" width="320" alt="Нікола Тесла"></td>
  </tr>
</table>

</div>

---

### 4. 🧠 "Квіз" (`/quiz`)
Бот надсилає підготовлене зображення та пропонує вибір тем (кнопки). Після вибору:
- надсилаються питання квізу
- наступне повідомлення користувача — відповідь
- відповідь перевіряється в ChatGPT
- повертається результат із можливістю:
  - задати ще питання на ту ж тему,
  - змінити тему,
  - закінчити квіз  
Бот веде рахунок правильних відповідей і відображає його.

<p align="center">Скріншоти</p>

<div align="center">

<table border="1" cellpadding="6">
  <tr>
    <td><img src="https://github.com/user-attachments/assets/0112e04b-e705-43cc-95f0-420e75266d58" width="360" alt="quiz1"></td>
    <td><img src="https://github.com/user-attachments/assets/5ff18384-f295-4173-934e-7ce65b6696b2" width="360" alt="кві2"></td>
  </tr>
  <tr>
    <td><img src="https://github.com/user-attachments/assets/de84540e-2494-4029-a4b7-bdde70076159" width="360" alt="квіз1"></td>
    <td><img src="https://github.com/user-attachments/assets/f21618e3-db99-4731-a16d-916b97f4b01e" width="360" alt="квіз4"></td>
  </tr>
</table>

</div>

---

### 5. 🌟 Тема на вибір (опціонально)

**"Допомога з резюме"**  
Бот запитує інформацію про освіту, досвід та навички, генерує шаблон резюме та надсилає користувачеві.

<div align="center">

<table border="1" cellpadding="6">
  <tr>
    <td><img src="https://github.com/user-attachments/assets/67f92419-35aa-4b35-b331-72ba524c4d10" width="420" alt="Резюме"></td>
  </tr>
</table>

</div>

**Своя тема**  
Додано **спливаючу кнопку меню**, яка постійно присутня під час усієї роботи боту.

<div align="center">

<table border="1" cellpadding="6">
  <tr>
    <td><img src="https://github.com/user-attachments/assets/895959ee-8a1e-4ab1-ab30-1f2e6dab4a15" width="420" alt="Кнопка Меню"></td>
  </tr>
</table>

</div>

---

## 📝 Примітки
- Зображення зменшені для зручності перегляду.
- Рамки реалізовані через HTML-таблиці в Markdown, щоб стабільно відображались на GitHub.

---
