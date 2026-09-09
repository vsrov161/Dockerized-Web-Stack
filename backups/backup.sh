#!/bin/bash

BACKUP_DIR="/backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
DB_NAME="mydb"
DB_USER="root"
DB_PASSWORD="${DB_PASSWORD:-secret}"

mkdir -p $BACKUP_DIR

mysqldump -h db -u $DB_USER -p$DB_PASSWORD $DB_NAME > $BACKUP_DIR/backup_$TIMESTAMP.sql

# Удаляем бэкапы старше 7 дней
find $BACKUP_DIR -name "backup_*.sql" -mtime +7 -delete

echo "Backup completed: backup_$TIMESTAMP.sql"