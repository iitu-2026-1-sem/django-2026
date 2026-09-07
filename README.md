# django-2026 — Service Desk (учебный проект, кафедра ЦИС МУИТ, осень 2026)

Сквозной проект дисциплины **SFT6206 «Разработка корпоративных приложений на фреймворке Django»** (группы IT1-2401, IT1-2402, IT1-2403, SIS-2305).
Один общий репозиторий: каждая фича — Issue, каждый студент/пара берёт Issue и делает Pull Request. Преподаватель ревьюит и мержит в `main`,
`main` автоматически деплоится на https://django.alma-ai.cc.

## Запуск за 3 команды
```bash
python -m venv .venv && . .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate && python manage.py runserver
```
Откройте http://127.0.0.1:8000 — по умолчанию SQLite, ничего настраивать не надо. Postgres: скопируйте `.env.example` → `.env` и задайте `DATABASE_URL`.

## Как сдавать работу (коротко; подробно — CONTRIBUTING.md)
1. Возьмите Issue (напишите в нём «беру»), или создайте Issue по шаблону «Фича».
2. Fork → ветка `feat/<номер-issue>-<кратко>` → коммиты → `make check` зелёный → Pull Request в `main` по шаблону.
3. Ревью преподавателя → правки → merge. После merge фича через минуту живёт на https://django.alma-ai.cc.

## Что внутри
- `servicedesk/` — настройки проекта (`settings.py` читает `.env`), URL, WSGI.
- `apps/accounts/` — кастомная модель пользователя с ролями (`employee` / `agent` / `manager`).
- `apps/tickets/` — заявки: модель, список, создание, просмотр; здесь растёт основная функциональность.
- `templates/`, `static/` — Django-шаблоны + Bootstrap 5 (CDN), без сборщика.
- `tests/` — pytest-django; `make check` = ruff + pytest.
- `deploy/` — как проект живёт на сервере (gunicorn + systemd + Caddy) и скрипт деплоя.

## Правила кода
Python 3.12+, Django 5.2, PEP 8 через `ruff`, тесты на каждую фичу, миграции коммитятся, секретов в репо нет (`.env` в `.gitignore`).
