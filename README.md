# Hammer System Test Task

### Общее описание функционала
- Сервис позволяет регистрироваться и авторизовываться через подтверждающий код в смс.
- После регистрации пользователью присваивается уникальный 6-значный номер.
- Используя уникальный 6-значный номер пользователи могут указать друг друга в качестве рефералов.
- Каждый пользователь может быть рефералом для нескольких пользователей, но у каждого пользователя есть только один реферал.
- На своей странице мы можете увидеть пригласительный номер своего реферала, и список телефонов пользователей, для которых вы являетесь рефералами.
- Сразу после регистрации у вас нет реферала, его необходимо добавить введя его 6-значный код.

# Описание API
## Метод отправки 4-значного кода в смс.

- **Request**

`POST /api/users/send_otp/`

```json
{
    "phone_number": "string"
}
```
- **Response**
```json
{
    "phone_number": "string",
    "otp": "string"
}
```

## Авторизация/регистрация через подтверждающий код из смс.

- **Request**

`POST /api/users/auth/`

```json
{
    "otp": "string"
}
```
- **Response**
```json
{
    "phone_number": "string",
    "token": "string"
}
```
## Личная страница пользователя.

- **Request**

`GET /api/users/me/`

- **Response**
```json
{
    "phone_number": "string",
    "invite_code": "string",
    "activated_invite_code": "string",
    "refs": [
        "string"
    ]
}
```

## Cтраница пользователя по его {id}.

- **Request**

`GET /api/users/{id}/`

- **Response**
```json
{
    "phone_number": "string",
    "invite_code": "string",
    "activated_invite_code": "string",
    "refs": [
        "string"
    ]
}
```

## Указание реферального кода.

- **Request**

`POST api/users/referal/`

```json
{
    "phone_number": "string",
    "activated_invite_code": "string"
}
```
- **Response**
```json
{
    "phone_number": "string",
    "activated_invite_code": "string",
    "you_invited_by": "string"
}
```

 - #### Документация Redoc доступна по адресу `/redoc/`

 # Как развернуть локально

 ## Без использования Docker

 - Для Windows
 
 Клонировать  репозиторий и выполнить команды

 ```
python -m venv venv

. venv/Scripts/activate

python -m pip install --upgrade pip

pip install -r requirements.txt
 ```
