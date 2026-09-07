# Деплой на warp (django.alma-ai.cc)

Стек без Docker: `venv + gunicorn` как **user-юнит systemd** на :8300, Postgres warp (`django2026`), Caddy (vhost в `~/warp-iitu/caddy-sites.nix`).

Первый раз:
```bash
git clone https://github.com/iitu-2026-1-sem/django-2026.git ~/students/django-2026 && cd ~/students/django-2026
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
cp .env.example .env   # DEBUG=0, SECRET_KEY, ALLOWED_HOSTS=django.alma-ai.cc, DATABASE_URL, CSRF_TRUSTED_ORIGINS=https://django.alma-ai.cc
mkdir -p ~/.config/systemd/user && cp deploy/django-2026.service ~/.config/systemd/user/ && systemctl --user daemon-reload && systemctl --user enable --now django-2026
```
Каждый merge в main: `bash deploy/deploy.sh` (git pull → pip → migrate → collectstatic → restart, ~10 с). Автозапуск — `deploy/webhook.md`.
