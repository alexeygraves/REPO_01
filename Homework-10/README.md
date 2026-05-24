# UI Kit — Домашнее задание 10

Базовая дизайн-система (UI Kit) с компонентами пользовательского интерфейса.
Методология БЭМ, адаптивная вёрстка, SCSS-архитектура.

## Структура проекта

```
Homework-10/
├── index.html              # страница-документация со всеми компонентами
└── styles/
    ├── main.css            # скомпилированный CSS (подключается в index.html)
    ├── main.scss           # точка входа SCSS, подключает все части
    ├── _variables.scss     # переменные: цвета, шрифты, отступы
    ├── _reset.scss         # сброс браузерных стилей
    ├── _base.scss          # базовые утилиты
    ├── components/
    │   ├── _button.scss    # .btn, .btn--primary, .btn--sm
    │   ├── _input.scss     # .input-field, .input-field--error
    │   ├── _dropdown.scss  # .dropdown, .dropdown--open
    │   ├── _checkbox.scss  # .checkbox, .radio
    │   ├── _card.scss      # .card, .card--md
    │   └── _navbar.scss    # .navbar, .navbar__menu--open
    └── layout/
        ├── _container.scss # .container
        └── _grid.scss      # .grid, .grid--3, .flex
```

## Компоненты

### Button `.btn`

| Класс | Описание |
|---|---|
| `.btn--primary` | основная кнопка |
| `.btn--secondary` | второстепенная |
| `.btn--sm / --md / --lg` | размеры |
| `disabled` | неактивное состояние |

Состояния: `:hover`, `:active`, `:focus-visible`

### Input `.input-field`

| Класс | Описание |
|---|---|
| `.input-field--with-icon` | иконка слева |
| `.input-field--error` | состояние ошибки + сообщение |

### Dropdown `.dropdown`

Открывается/закрывается через JS: `classList.toggle('dropdown--open')`.

### Checkbox `.checkbox` / Radio `.radio`

Кастомные элементы управления. Состояния: checked, focus, disabled.

### Card `.card`

| Класс | Описание |
|---|---|
| `.card--sm / --md / --lg` | размеры для standalone |
| внутри `.grid` | заполняет ячейку, max-width убирается |

### Navbar `.navbar`

- Десктоп: горизонтальное меню
- Мобильный (`<768px`): скрывается, появляется кнопка-гамбургер

JS для гамбургера:
```js
toggle.addEventListener('click', () => {
  menu.classList.toggle('navbar__menu--open');
  toggle.classList.toggle('navbar__toggle--active');
});
```

### Grid / Flex

```html
<div class="grid grid--3">...</div>  <!-- 3 колонки → 2 → 1 -->
<div class="grid grid--auto">...</div>  <!-- auto-fill minmax(240px, 1fr) -->
<div class="flex flex--between flex--gap-4">...</div>
```

## Компиляция SCSS

```bash
npm install -g sass
sass styles/main.scss styles/main.css --watch
```

## Просмотр

Открыть `index.html` в браузере — страница-документация со всеми компонентами в живом виде.
