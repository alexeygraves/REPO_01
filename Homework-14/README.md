# Домашнее задание 14 — React Auth + PWA

Тема 16: Безопасность в браузере, Cookie, LocalStorage, CORS, XSRF и Progressive Web App

## Стек

- React 18 + React Router v6
- Vite
- Service Worker (ручная регистрация через `public/sw.js`)

## Запуск

```bash
npm install
npm run dev
```

Для проверки Service Worker необходима production-сборка (SW не работает в dev-режиме Vite):

```bash
npm run build
npm run preview
```

## Структура проекта

```
src/
  utils/auth.js          — работа с токеном (localStorage)
  hooks/useNetwork.js    — хук для отслеживания онлайн/офлайн
  components/
    Header.jsx           — шапка с индикатором авторизации
    NetworkStatus.jsx    — всплывающее уведомление о сети
    ProtectedRoute.jsx   — защита маршрутов
  pages/
    LoginPage.jsx        — форма входа
    HomePage.jsx         — защищённая главная страница
public/
  sw.js                  — Service Worker
```

## Реализовано

**Авторизация**
- Форма входа с валидацией (формат email, длина пароля >= 6 символов)
- JWT-подобный токен сохраняется в `localStorage` с проверкой срока действия (1 час)
- Защита маршрутов — без токена редирект на `/login`
- Кнопка «Выйти» очищает токен и перенаправляет на страницу входа

**Service Worker**
- Событие `install` — прекеш `index.html`
- Событие `fetch` — cache-first для ресурсов, network-first для навигации
- Событие `activate` — удаление устаревших версий кеша
- Офлайн-режим: при отсутствии сети отдаёт страницу из кеша

**Индикаторы**
- Шапка показывает имя пользователя после входа или кнопку «Войти»
- Всплывающее уведомление при переходе в офлайн / восстановлении соединения

## Тестирование

Данные для входа: любой корректный `email@domain.com`, пароль от 6 символов.
