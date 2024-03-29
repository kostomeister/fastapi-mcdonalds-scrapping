# McD's Menu API 🍟

Цей API дозволяє отримати доступ до меню з веб-сайту McDonald's. Тепер ви можете легко отримати інформацію про свої улюблені страви прямо зі скрапера.

## Інструкції по встановленню

1. **Клонуйте репозиторій:**
   ```bash
   git clone https://github.com/kostomeister/fastapi-mcdonalds-scrapping.git
   ```

2. **Створіть віртуальне середовище:**
   ```bash
   cd fastapi-mcdonalds-scrapping
   python -m venv venv
   ```

3. **Активуйте віртуальне середовище:**
   - Для Windows:
     ```bash
     venv\Scripts\activate
     ```
   - Для Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Встановіть залежності:**
   ```bash
   pip install -r requirements.txt
   ```

## Опис ендпоінтів

- **GET /api/v1/all_products/** 🍔
  Повертає список всіх продуктів у форматі JSON.

- **GET /api/v1/products/{product_name}** 🍟
  Повертає інформацію про продукт за його назвою.

- **GET /api/v1/products/{product_name}/{product_field}** 🥤
  Повертає значення конкретного поля продукту (наприклад, калорії або жири).

## Запуск сервера

1. **Запустіть сервер:**
   ```bash
   uvicorn main:app --reload
   ```

2. **Відкрийте документацію API:**
   Після запуску сервера перейдіть на `http://localhost:8000/docs`, щоб побачити документацію API та спробувати ендпоінти.

## Запуск скрапера

1. **Запустіть скрапер:**
   ```bash
   python src/scraping/scrape.py
   ```

## Збереження даних

- Дані про меню зберігаються у файлі `mcdonalds_menu.json`.
- Початкові дані можуть бути вже наявними у цьому файлі у форматі JSON.

🎉 Тепер ви готові користуватися API та отримувати дані про меню McDonald's просто натиснувши кілька кнопок! 🍔🥤