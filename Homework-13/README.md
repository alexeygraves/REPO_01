# ReactShop — Homework 13

Интернет-магазин на React. Домашнее задание к теме 15 — оптимизация и развёртывание.

## Запуск

```bash
npm install
npm run dev
```

## Тесты

```bash
npm test
```

Используется **Vitest** (Jest-совместимый API) + **React Testing Library**.

## Структура

```
src/
  components/
    Navbar.jsx        навигация с бейджами корзины и избранного
    ProductCard.jsx   карточка товара (React.memo)
  context/
    AppContext.jsx    глобальное состояние: избранное, корзина, тема
  pages/
    Home.jsx
    List.jsx          список товаров из DummyJSON API
    Details.jsx       детальная страница товара
    Favourites.jsx    страница избранного (/favourites)
    Cart.jsx          страница корзины (/cart)
    About.jsx
  __tests__/
    ProductCard.test.jsx
    Favourites.test.jsx
    Cart.test.jsx
```

## Реализованный функционал

**Избранное**
- Маршрут `/favourites` — список избранных товаров
- Отображает название, цену, категорию, наличие на складе, рейтинг
- Удаление из избранного прямо из списка
- Сохраняется в `localStorage` между сессиями

**Корзина**
- Маршрут `/cart`
- Добавление товаров с карточки и со страницы деталей
- Подсчёт итоговой суммы через `useMemo`

**Оптимизация**
- `React.memo` — ProductCard не перерисовывается при несвязанных изменениях родителя
- `useCallback` — функции `toggleFavorite`, `addToCart`, `removeFromCart` стабилизированы
- `useMemo` — мемоизация значения контекста и итоговой суммы корзины
- `React.lazy` + `Suspense` — все страницы загружаются лениво, бандл разбит на чанки

**Тестирование**
- 14 тестов для компонентов ProductCard, Favourites, Cart
- Проверяется рендер, взаимодействие (клик на кнопки), edge-кейсы

## Развёртывание

Для публикации на Vercel:
```bash
npm run build
npx vercel --prod
```

Для GitHub Pages:
```bash
npm run build
# содержимое папки dist/ деплоим в gh-pages ветку
```
