# Используем базовый образ Nginx
FROM nginx

# Копируем файл конфигурации Nginx
COPY nginx.conf /etc/nginx/nginx.conf

# Очистка директории /usr/share/nginx/html
RUN rm -rf /usr/share/nginx/html/*
