# Frontend для создания профиля пользователя

Красивый и современный веб-интерфейс для заполнения профиля пользователя в приложении знакомств.

## Особенности

- 🎨 **Современный дизайн** с градиентами и анимациями
- 📱 **Адаптивный интерфейс** для всех устройств
- 🔄 **Пошаговая форма** с индикатором прогресса
- ✅ **Валидация данных** в реальном времени
- 📍 **Автоматическое определение местоположения**
- 🎯 **Удобная навигация** с возможностью возврата
- 💫 **Плавные анимации** и переходы

## Структура файлов

```
frontend/
├── index.html      # Главная HTML страница
├── styles.css      # CSS стили
├── script.js       # JavaScript логика
└── README.md       # Документация
```

## Поля профиля

Форма включает все необходимые поля для создания профиля:

1. **Имя** - отображается другим пользователям
2. **Фамилия** - не отображается другим пользователям
3. **Пол** - мужской/женский
4. **Возраст** - от 18 до 100 лет
5. **Город** - с возможностью автоматического определения
6. **Национальность** - выбор из списка
7. **Религия** - выбор из основных религий
8. **Уровень религиозности** - низкий/средний/высокий
9. **Образование** - без/среднее/высшее
10. **Профессия** - опциональное поле
11. **Рост** - в сантиметрах
12. **Вес** - в килограммах
13. **Семейное положение** - холост/разведен/вдовец
14. **Наличие детей** - да/нет
15. **Отношение к многожёнству** - принимаю/не принимаю/не уверен
16. **Цель знакомства** - дружба/общение/брак

## Установка и запуск

### Простой запуск

1. Откройте файл `index.html` в браузере
2. Или запустите локальный сервер:

```bash
# Python 3
python -m http.server 8000

# Python 2
python -m SimpleHTTPServer 8000

# Node.js (если установлен)
npx http-server
```

### Интеграция с бэкендом

Для работы с вашим API замените URL в функции `sendToAPI()` в файле `script.js`:

```javascript
async sendToAPI(data) {
    const response = await fetch('YOUR_API_ENDPOINT/profile/create', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    });
    
    return await response.json();
}
```

## API Endpoint

Фронтенд ожидает API endpoint для создания профиля:

**POST** `/api/profile/create`

**Request Body:**
```json
{
    "name": "string",
    "surname": "string", 
    "gender": "male|female",
    "age": 25,
    "city": "string",
    "latitude": 41.3111,
    "longitude": 69.2797,
    "ethnicity": "string",
    "religion": "string",
    "religious_level": "low|medium|high",
    "education": "none|secondary|higher",
    "job": "string|null",
    "height": 175,
    "weight": 70,
    "marital_status": "single|divorced|widowed",
    "has_children": true,
    "polygamy": true|false|null,
    "goal": "friendship|communication|marriage"
}
```

**Response:**
```json
{
    "success": true,
    "message": "Профиль успешно создан",
    "profile_id": 123
}
```

## Кастомизация

### Изменение цветовой схемы

Отредактируйте CSS переменные в `styles.css`:

```css
:root {
    --primary-color: #667eea;
    --secondary-color: #764ba2;
    --accent-color: #ff6b6b;
    --success-color: #00b894;
    --error-color: #e74c3c;
}
```

### Добавление новых полей

1. Добавьте HTML разметку в `index.html`
2. Добавьте валидацию в `script.js`
3. Обновите общее количество шагов (`totalSteps`)

### Изменение текстов

Все тексты находятся в HTML файле и могут быть легко изменены.

## Браузерная поддержка

- Chrome 60+
- Firefox 55+
- Safari 12+
- Edge 79+

## Лицензия

MIT License

## Поддержка

Если у вас есть вопросы или предложения, создайте issue в репозитории проекта. 