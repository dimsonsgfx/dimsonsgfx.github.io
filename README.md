# DIMSONSGFX — Портфолио

Статический сайт-портфолио на GitHub Pages: **https://dimsonsgfx.github.io**

Дизайн основан на шаблоне **Simple Blog v2 (avaxgfxgreen)** — макет, CSS, JS и шрифты перенесены без серверной части DLE.

---

## Структура сайта

```
dimsonsgfx.github.io/
├── index.html              ← Главная страница
├── category/
│   ├── arts/index.html
│   ├── logos/index.html
│   ├── banners/index.html
│   ├── illustrations/index.html
│   └── other/index.html
├── works/
│   └── {slug}/index.html  ← Страница каждой работы
├── search/index.html       ← Клиентский поиск
├── 404.html
├── sitemap.xml
├── robots.txt
├── .nojekyll
├── assets/
│   ├── css/
│   │   ├── styles.css      ← Оригинальный CSS шаблона
│   │   └── patch.css       ← Патч: исправления + тёмная тема
│   ├── js/
│   │   ├── libs.js         ← Оригинальный JS шаблона
│   │   └── site.js         ← Загрузка данных, тема, поиск
│   ├── images/             ← Картинки, placeholder SVG
│   └── webfonts/           ← Font Awesome Pro woff/woff2
├── data/
│   ├── works.json          ← ВСЕ работы (единый источник)
│   └── categories.json     ← Категории
└── scripts/
    └── build.py            ← Генератор страниц
```

---

## Как добавить новую работу

### Вариант А — вручную (через `works.json`)

Добавь объект в [`data/works.json`](data/works.json):

```json
{
  "slug": "my-new-work",
  "title": "Название работы",
  "description": "Описание работы — что изображено, в каком стиле",
  "category": "arts",
  "categoryLabel": "Арты",
  "date": "2026-10-01",
  "image": "/assets/images/my-new-work.jpg",
  "thumb": "/assets/images/my-new-work.jpg",
  "emoji": "🎨",
  "tags": ["тег1", "тег2"],
  "views": 0,
  "source": "manual"
}
```

Затем запусти генератор:
```bash
python scripts/build.py
git add -A && git commit -m "Add: Название работы" && git push
```

### Вариант Б — папка с файлом (для автопостинга)

Положи изображение в `assets/images/` и запись в `data/works.json`.

---

## Как добавить категорию

В [`data/categories.json`](data/categories.json) добавь:

```json
{
  "slug": "my-category",
  "label": "Моя категория",
  "icon": "🖌",
  "description": "Описание категории для meta description"
}
```

Затем пересобери сайт (`python scripts/build.py` + push).

---

## Как сменить тему

Сайт поддерживает светлую и тёмную тему.  
Переключатель ☀️ в шапке.  
Тема сохраняется в `localStorage` браузера.

Чтобы изменить цвета тёмной темы — редактируй `assets/css/patch.css`, блок `[data-theme="dark"]`.  
Акцентный цвет (`#36c537`) — в `assets/css/styles.css` (поиск по `#36c537`).

---

## Что убрано из DLE

| Функция DLE | Что сделано |
|---|---|
| Регистрация / вход | Убрана (кнопка "Войти" убрана из шапки) |
| Комментарии | Убраны (можно добавить giscus) |
| Рейтинги / лайки | Убраны |
| Личные сообщения (PM) | Убраны |
| Голосования (Опросы) | Убраны |
| Добавить в избранное | Убрана |
| Поиск (серверный) | Заменён на клиентский JS-поиск по works.json |
| Просмотры | Статичное поле `views` в JSON (можно подключить analytics) |
| AJAX-навигация | Заменена обычными ссылками |
| Боковые виджеты (VK, опрос) | Убраны |

---

## Автопостинг из Telegram (будущее)

Формат одной работы для автопостинга:

```json
{
  "slug": "telegram-post-12345",
  "title": "Подпись из поста (первая строка)",
  "description": "Полный текст поста",
  "category": "arts",
  "categoryLabel": "Арты",
  "date": "2026-10-15",
  "image": "/assets/images/post-12345.jpg",
  "thumb": "/assets/images/post-12345.jpg",
  "emoji": "🎨",
  "tags": ["хэштег1", "хэштег2"],
  "views": 0,
  "source": "telegram",
  "telegram_post_id": 12345
}
```

**Категория** определяется по хэштегу в подписи:
- `#арты` → `arts`
- `#логотипы` → `logos`
- `#баннеры` → `banners`
- `#иллюстрации` → `illustrations`

**Схема автопостинга (GitHub Actions):**
1. Бот на Python опрашивает Telegram API
2. Находит новые посты с картинками
3. Скачивает медиа → `assets/images/`
4. Добавляет запись в `data/works.json`
5. Запускает `python scripts/build.py`
6. Коммитит и пушит в `main`
7. GitHub Pages автоматически деплоит

Workflow-файл: `.github/workflows/telegram-sync.yml` (будет добавлен отдельно).

---

## Технологии

- **Хостинг**: GitHub Pages (бесплатно)
- **Шаблон**: Simple Blog v2 (avaxgfxgreen)
- **Сборка**: Python 3 (build.py)
- **SEO**: sitemap.xml, robots.txt, Open Graph, Schema.org
- **Поиск**: клиентский JS по works.json
- **Шрифты**: Montserrat + Rubik (Google Fonts), Font Awesome 5 Pro (локально)
