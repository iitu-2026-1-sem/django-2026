#!/usr/bin/env bash
# Быстрый деплой Django на warp: pull → deps → migrate → static → restart. Печатает OK ✓ / FAIL ✗.
set -euo pipefail
cd "$(dirname "$0")/.."
git pull -q --ff-only origin main
.venv/bin/pip install -q -r requirements.txt
set -a; . ./.env; set +a
.venv/bin/python manage.py migrate --noinput
.venv/bin/python manage.py collectstatic --noinput -v 0
systemctl --user restart django-2026
sleep 1
curl -fsS -o /dev/null http://127.0.0.1:8300/health/ && echo "OK ✓ django-2026 $(git rev-parse --short HEAD)" || { echo "FAIL ✗ health"; exit 1; }
