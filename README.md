# DIMSONSGFX — Портфолио цифрового художника

🌐 **Сайт:** [https://dimsonsgfx.github.io](https://dimsonsgfx.github.io)  
📦 **Репозиторий:** [https://github.com/dimsonsgfx/dimsonsgfx.github.io](https://github.com/dimsonsgfx/dimsonsgfx.github.io)

Статический адаптивный сайт-портфолио на **GitHub Pages**, оформленный на основе шаблона **Simple Blog v2 (avaxgfxgreen)**:
- 3 колонки сетки работ (посты в 3 ряда)
- Левая боковая колонка (навигация, выбор редакции, топ работ)
- Правая колонка убрана для максимального фокуса на галерее
- Текстовый логотип-заглушка `DIMSONSGFX`
- Переключатель тёмной / светлой темы (с сохранением в `localStorage`)
- Клиентский быстрый поиск по работам
- Полная SEO-оптимизация (JSON-LD, Open Graph, Twitter Cards, Sitemap с картинками, robots.txt)
- Подготовленная архитектура для автопостинга из Telegram

---

## Быстрый старт (сборка и деплой)

Сайт генерируется локальным скриптом на Python без сторонних зависимостей.

1. Пересобрать сайт:
```bash
python scripts/build.py
```
2. Отправить изменения на GitHub (деплой произойдёт автоматически за 1-2 минуты):
```bash
git add -A
git commit -m "Update portfolio"
git push
```

---

## Структура проекта

```text
dimsonsgfx.github.io/
├── index.html              ← Главная страница (последние и все работы)
├── 404.html                ← Страница ошибки 404
├── sitemap.xml             ← Карта сайта с разметкой image:image
├── robots.txt              ← Инструкции для поисковых роботов
├── .nojekyll               ← Отключение Jekyll на GitHub Pages
├── category/               ← Страницы категорий с пагинацией
│   ├── arts/index.html
│   ├── logos/index.html
│   ├── banners/index.html
│   ├── illustrations/index.html
│   └── other/index.html
├── works/                  ← Отдельные страницы для каждой работы
│   ├── urban-dreams/index.html
│   ├── logo-minimalist/index.html
│   └── ...
├── search/                 ← Страница живого поиска
│   └── index.html
├── assets/
│   ├── css/
│   │   ├── styles.css      ← Базовые стили шаблона avaxgfxgreen
│   │   ├── patch.css       ← 3 ряда постов, тёмная тема, логотип, скрытие правой колонки
│   │   └── fonts.css       ← Декларации Font Awesome
│   ├── js/
│   │   ├── libs.js         ← Вспомогательные библиотеки
│   │   └── site.js         ← Управление темой, поиск, ленивая загрузка, сайдбар
│   ├── images/             ← Изображения работ (SVG/PNG/JPG/WebP), логотип, og-default.svg
│   ├── dleimages/          ← Иконки элементов интерфейса
│   └── webfonts/           ← Шрифты Font Awesome 5 Pro
├── data/
│   ├── works.json          ← Единая база всех работ (источник данных)
│   └── categories.json     ← Список категорий и их метаданные
└── scripts/
    └── build.py            ← Генератор статичных страниц и SEO
```

---

## Как добавить новую работу

Все работы хранятся в файле [`data/works.json`](data/works.json).

### 1. Подготовка файла изображения
- Имя файла **только латиницей в kebab-case** (например, `logo-dark-fox.webp` или `cyber-samurai-art.jpg`, но **НЕ** `IMG_0123.jpg`).
- Положите файл в папку `assets/images/`.
- Рекомендуемые форматы: WebP или JPG (ширина 800–1920px, качественное сжатие).

### 2. Добавление записи в `data/works.json`
Добавьте в массив новый JSON-объект:

```json
{
  "slug": "logo-dark-fox",
  "title": "Dark Fox Studio",
  "description": "Фирменный знак и айдентика для игровой инди-студии. Минималистичный силуэт лисы с акцентом на геометрию и динамику. Разработано в векторе для адаптации под любые носители.",
  "category": "logos",
  "categoryLabel": "Логотипы",
  "date": "2026-10-01",
  "image": "/assets/images/logo-dark-fox.webp",
  "thumb": "/assets/images/logo-dark-fox.webp",
  "emoji": "🦊",
  "tags": ["логотип", "студия", "минимализм", "вектор"],
  "views": 0,
  "source": "manual"
}
```

> **Важно по SEO:**
> - `description` должен содержать не менее 2–3 предложений с понятным описанием стиля и контекста работы.
> - `alt` для изображения формируется автоматически по формуле: `"{title} — {categoryLabel}"`.

### 3. Пересборка:
```bash
python scripts/build.py
git add -A && git commit -m "Add work: Dark Fox Studio" && git push
```

---

## Как добавить или изменить категорию

Категории настраиваются в файле [`data/categories.json`](data/categories.json):

```json
{
  "slug": "3d-models",
  "label": "3D Модели",
  "icon": "🧊",
  "description": "Низкополигональные и высокополигональные 3D модели, рендеры и текстуры"
}
```

После редактирования запустите `python scripts/build.py`. Скрипт создаст папку `/category/3d-models/index.html`, добавит её в меню, навигацию, sitemap.xml и карту сайта.

---

## Как заменить логотип-заглушку на реальный логотип

Сейчас в шапке отображается аккуратная текстовая заглушка `DIMSONSGFX`.

Когда будет готов графический логотип:
1. Сохраните изображение размером `280x60` px как `assets/images/logo.png`.
2. В файле [`assets/css/patch.css`](assets/css/patch.css) найдите блок:
```css
/* Скрываем битый img логотипа, показываем текст */
.logo img { display: none; }
.logo-text { display: block !important; }
```
3. Замените на:
```css
.logo img { display: block !important; max-height: 50px; }
.logo-text { display: none !important; }
```
4. Запустите `git add -A && git commit -m "Update logo" && git push`.

---

## Как изменить оформление и цвета

1. **Акцентный цвет сайта (`#36c537` — зелёный):**
   - Замените hex-код `#36c537` в `assets/css/styles.css` и `assets/css/patch.css` на желаемый (например, золотой `#c8a96e`, бирюзовый `#00ccaa` или индиго `#6366f1`).
2. **Тёмная тема:**
   - Все параметры тёмной темы находятся в секции `[data-theme="dark"]` файла `assets/css/patch.css`.
   - Можно менять фон карточек, шапки, футера и текста.

---

## Подтверждение прав: Google Search Console и Яндекс Вебмастер

В скрипте [`scripts/build.py`](scripts/build.py) предусмотрены переменные для добавления кодов верификации:

```python
GOOGLE_VERIFICATION = ""   # Вставьте код подтверждения Google сюда
YANDEX_VERIFICATION = ""   # Вставьте код подтверждения Яндекс сюда
```

### Пошаговая инструкция: Google Search Console
1. Перейдите в [Google Search Console](https://search.google.com/search-console/).
2. Нажмите **Добавить ресурс** (Add Property).
3. Выберите вариант **Префикс URL** (URL prefix) и введите:  
   `https://dimsonsgfx.github.io`
4. В способах подтверждения раскройте **Тег HTML** (HTML tag).
5. Скопируйте значение атрибута `content`:
   `<meta name="google-site-verification" content="ВАШ_КОД_ЗДЕСЬ" />`
6. Откройте `scripts/build.py`, укажите:
   ```python
   GOOGLE_VERIFICATION = "ВАШ_КОД_ЗДЕСЬ"
   ```
7. Запустите сборку и отправьте изменения на GitHub:
   ```bash
   python scripts/build.py
   git add -A && git commit -m "Add Google verification" && git push
   ```
8. В Search Console нажмите кнопку **Подтвердить** (Verify).
9. В левом меню перейдите в **Файлы Sitemap** (Sitemaps) и отправьте URL:  
   `https://dimsonsgfx.github.io/sitemap.xml`

### Пошаговая инструкция: Яндекс Вебмастер
1. Перейдите в [Яндекс Вебмастер](https://webmaster.yandex.ru/).
2. Нажмите **Добавить сайт** и введите:  
   `https://dimsonsgfx.github.io`
3. Выберите метод подтверждения **Метатег**.
4. Скопируйте значение из `content`:
   `<meta name="yandex-verification" content="ВАШ_КОД_ЗДЕСЬ" />`
5. В `scripts/build.py` укажите:
   ```python
   YANDEX_VERIFICATION = "ВАШ_КОД_ЗДЕСЬ"
   ```
6. Соберите и запушьте:
   ```bash
   python scripts/build.py
   git add -A && git commit -m "Add Yandex verification" && git push
   ```
7. В Яндекс Вебмастере нажмите **Проверить**.
8. Перейдите в раздел **Индексирование** → **Файлы Sitemap** и укажите:  
   `https://dimsonsgfx.github.io/sitemap.xml`

---

## Архитектура автопостинга из Telegram

Полная реализация будет развёрнута отдельным шагом, но вся структура данных и разметка уже готовы:

### 1. Формат поста в Telegram-канале
При публикации в Telegram подпись к фотографии оформляется по шаблону:

```text
Название работы

Подробное описание работы: в какой программе создано, в чём идея, ключевые особенности дизайна. Не менее двух-трёх законченных предложений.

#арты #иллюстрация #photoshop
```

### 2. Сопоставление хэштегов с категориями сайта
Бот парсит хэштеги в конце поста:
- `#арты` или `#арт` → `arts` (Арты)
- `#логотипы` или `#лого` → `logos` (Логотипы)
- `#баннеры` или `#баннер` → `banners` (Баннеры)
- `#иллюстрации` или `#иллюстрация` → `illustrations` (Иллюстрации)
- По умолчанию / другие хэштеги → `other` (Прочее)

### 3. Шаблон записи, которую формирует автопостинг:
Бот сохраняет сжатое фото в `assets/images/tg-{id}.webp` и добавляет объект в `data/works.json`:

```json
{
  "slug": "cyber-samurai-20261015",
  "title": "Cyber Samurai",
  "description": "Кибер-самурай — Арты. Концепт персонажа для футуристической новеллы. Световые мечи и неоновые пластины брони на фоне ночного неонового Токио.",
  "category": "arts",
  "categoryLabel": "Арты",
  "date": "2026-10-15",
  "image": "/assets/images/tg-12345.webp",
  "thumb": "/assets/images/tg-12345.webp",
  "emoji": "🎨",
  "tags": ["самурай", "киберпанк", "неон"],
  "views": 0,
  "source": "telegram",
  "telegram_post_id": 12345
}
```

### 4. Автоматизация через GitHub Actions
Будет создан `.github/workflows/telegram-sync.yml`, который:
1. Запускается по cron (например, раз в 30 минут) или по вебхуку.
2. Скачивает новые фото из канала через Bot API.
3. Оптимизирует изображения (WebP, 85% качество, max width 1600px).
4. Заполняет `title`, `description`, `alt`, `tags`.
5. Запускает `python scripts/build.py`.
6. Коммитит и пушит в ветку `main`.
7. Сайт автоматически обновляется на GitHub Pages.

---

## Реализованное SEO

- [x] **Уникальные Title и Meta Description** для каждой страницы
- [x] **Единственный тег H1** на каждой странице (семантически правильная иерархия)
- [x] **Теги Canonical** со строгими абсолютными URL
- [x] **Open Graph и Twitter Card** на всех страницах (корректные превью при шеринге)
- [x] **Карта сайта `sitemap.xml`** с расширением `xmlns:image` и тегами `<image:image>`
- [x] **Файл `robots.txt`** с запретом индексации поисковой страницы и ссылкой на sitemap
- [x] **Микроразметка Schema.org (JSON-LD)**:
  - `WebSite` с поисковым действием `SearchAction` (на главной)
  - `Person` — информация об авторе
  - `CreativeWork` и `ImageObject` — детальная информация об иллюстрациях
  - `BreadcrumbList` — цепочка хлебных крошек
  - `CollectionPage` — страницы категорий
- [x] **Оптимизация загрузки**: `loading="lazy"`, явные размеры `width`/`height` для защиты от сдвигов верстки (CLS)
- [x] **Защита от 404 индексации**: директива `noindex, follow` на странице 404

---

## Чеклист готовности

- [x] Репозиторий и хостинг на GitHub Pages
- [x] Вёрстка по шаблону avaxgfxgreen
- [x] Посты в 3 ряда без правой колонки
- [x] Текстовый логотип-заглушка `DIMSONSGFX`
- [x] Тёмная и светлая тема
- [x] 17 тестовых работ в 5 категориях
- [x] Сайдбар с выбором редакции и топом работ
- [x] Живой поиск
- [x] Полный пакет SEO (JSON-LD, Sitemap, OG)
- [x] Места под коды Google Search Console и Яндекс Вебмастер
- [x] Документация и спецификация автопостинга
- [ ] *В будущем:* привязать реальный логотип и фотографии работ
- [ ] *В будущем:* настроить скрипт автопостинга из Telegram через GitHub Actions
- [ ] *В будущем:* вставить коды верификации вебмастеров после их получения
