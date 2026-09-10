#!/bin/bash
set -euo pipefail

TIMESTAMP=$(date +%Y-%m-%d_%H-%M-%S)
BACKUP_DIR="/backups"
FILENAME="${BACKUP_DIR}/${MYSQL_DATABASE}_${TIMESTAMP}.sql.gz"
RETENTION_DAYS="${BACKUP_RETENTION_DAYS:-7}"

mkdir -p "$BACKUP_DIR"

echo "[$(date)] Начинаю бэкап базы ${MYSQL_DATABASE}..."

mysqldump \
    -h "$DB_HOST" \
    -u "$MYSQL_USER" \
    -p"$MYSQL_PASSWORD" \
    --single-transaction \
    --quick \
    "$MYSQL_DATABASE" | gzip > "$FILENAME"

echo "[$(date)] Бэкап сохранён: $FILENAME ($(du -h "$FILENAME" | cut -f1))"

# Удаляем бэкапы старше RETENTION_DAYS дней
DELETED=$(find "$BACKUP_DIR" -name "*.sql.gz" -mtime "+${RETENTION_DAYS}" -print -delete | wc -l)
echo "[$(date)] Удалено старых бэкапов: ${DELETED} (старше ${RETENTION_DAYS} дней)"