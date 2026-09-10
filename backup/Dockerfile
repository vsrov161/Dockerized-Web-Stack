# Берём образ mysql — в нём уже есть mysqldump и mysql-client,
# не нужно ставить их отдельно
FROM mysql:8.0

# А вот cron и gzip в базовом образе уже нет — их ставим сами.
# Это как раз тот случай "настроить окружение по-своему", о котором
# вы спрашивали: официальный образ заточен под одну задачу (быть
# MySQL-сервером), а нам от него нужен только клиент + свой планировщик.
RUN apt-get update \
    && apt-get install -y --no-install-recommends cron gzip \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /backup
COPY backup.sh /backup/backup.sh
RUN chmod +x /backup/backup.sh

# Расписание: каждый день в 03:00. Переменные окружения контейнера
# не наследуются в cron-задачи автоматически — поэтому явно прокидываем
# их в файл /etc/environment при старте (см. entrypoint.sh)
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh \
    && echo "0 3 * * * /backup/backup.sh >> /var/log/backup.log 2>&1" > /etc/cron.d/db-backup \
    && chmod 0644 /etc/cron.d/db-backup \
    && touch /var/log/backup.log

ENTRYPOINT ["/entrypoint.sh"]