#!/bin/bash
set -euo pipefail

# cron не видит переменные окружения контейнера по умолчанию —
# он запускает задачи в "чистом" окружении. Поэтому сохраняем текущие
# переменные в /etc/environment, откуда их подхватит cron-задача.
printenv | grep -E '^(DB_HOST|MYSQL_USER|MYSQL_PASSWORD|MYSQL_DATABASE|BACKUP_RETENTION_DAYS)=' \
    > /etc/environment

echo "[$(date)] Контейнер бэкапов запущен. Первый плановый запуск — по расписанию из /etc/cron.d/db-backup"

# Запускаем cron в foreground (-f), чтобы контейнер не завершался,
# и одновременно выводим лог бэкапов в stdout, чтобы `docker compose logs` его видел
cron -f &
tail -f /var/log/backup.log