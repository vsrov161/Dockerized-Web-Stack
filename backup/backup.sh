#!/bin/sh
set -e

BACKUP_DIR=/backups
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/backup_$TIMESTAMP.sql"

echo "[backup] dumping database..."
mysqldump -h "$DB_HOST" -u "$DB_USER" -p"$DB_PASSWORD" "$DB_NAME" > "$BACKUP_FILE"

# Храним только последние 7 бэкапов
ls -1t "$BACKUP_DIR"/backup_*.sql | tail -n +8 | xargs -r rm -f

echo "[backup] done: $BACKUP_FILE"