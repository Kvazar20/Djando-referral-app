
# API документация

Данный API предназначен для реализации двухфакторной аутентификации через телефонный номер с использованием кодов подтверждения и инвайт-кодов для пользователей.

## 1. `POST /api/enter_phone/`

### Описание:
Этот эндпоинт отправляет пользователю на телефон код подтверждения для дальнейшей авторизации.

### Параметры запроса:
- **phone** (обязательный): Номер телефона пользователя. Должен быть передан в формате строки.

### Пример запроса:
```json
{
  "phone": "79161234567"
}
```

### Ответ:
- Если запрос успешен:
  - Статус: `200 OK`
  - Тело ответа:
  ```json
  {
    "message": "Код подтверждения отправлен успешно!",
    "Verification code": "1234"
  }
  ```

- Если запрос невалиден:
  - Статус: `400 Bad Request`
  - Тело ответа:
  ```json
  {
    "phone": ["This field is required."]
  }
  ```

## 2. `POST /api/enter_code/`

### Описание:
Этот эндпоинт принимает код подтверждения, введенный пользователем, и выполняет его проверку.

### Параметры запроса:
- **verification_code** (обязательный): Код подтверждения, который был отправлен на телефон пользователя.

### Пример запроса:
```json
{
  "verification_code": "1234"
}
```

### Ответ:
- Если код введен правильно:
  - Статус: `200 OK`
  - Тело ответа:
  ```json
  {
    "message": "Авторизация прошла успешно!"
  }
  ```

- Если код введен неверно:
  - Статус: `401 Unauthorized`
  - Тело ответа:
  ```json
  {
    "error": "Неверный код подтверждения!"
  }
  ```

- Если код не был найден в сессии:
  - Статус: `400 Bad Request`
  - Тело ответа:
  ```json
  {
    "error": "Код подтверждения не найден!"
  }
  ```

## 3. `GET /api/profile/`

### Описание:
Этот эндпоинт возвращает информацию о профиле текущего пользователя.

### Ответ:
- Статус: `200 OK`
- Тело ответа:
```json
{
  "phone": "79161234567",
  "invite_code": "ABC123",
  "activated_invite_code": "XYZ789",
  "referred_users": [
    {
      "phone": "79162345678"
    },
    {
      "phone": "79163456789"
    }
  ]
}
```

## 4. `POST /api/profile/`

### Описание:
Этот эндпоинт обрабатывает запрос на активацию инвайт-кода.

### Параметры запроса:
- **invite_code** (обязательный): Инвайт-код, который пользователь хочет активировать.

### Пример запроса:
```json
{
  "invite_code": "ABC123"
}
```

### Ответ:
- Если инвайт-код успешно активирован:
  - Статус: `200 OK`
  - Тело ответа:
  ```json
  {
    "message": "Инвайт-код ABC123 успешно активирован!"
  }
  ```

- Если инвайт-код уже был активирован:
  - Статус: `409 Conflict`
  - Тело ответа:
  ```json
  {
    "error": "Вы уже активировали инвайт-код!"
  }
  ```

- Если инвайт-код не найден:
  - Статус: `404 Not Found`
  - Тело ответа:
  ```json
  {
    "error": "Пользователь с данным инвайт-кодом не найден!"
  }
  ```

## Ошибки

- **400 Bad Request** — Невалидные или отсутствующие параметры запроса.
- **401 Unauthorized** — Неверный код подтверждения.
- **404 Not Found** — Инвайт-код не найден.
- **409 Conflict** — Инвайт-код уже активирован.