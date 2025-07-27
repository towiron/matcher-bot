#!/bin/bash

# Скрипт для запуска фронтенда создания профиля

echo "🚀 Запуск фронтенда для создания профиля..."
echo ""

# Проверяем, установлен ли Python
if command -v python3 &> /dev/null; then
    echo "✅ Python 3 найден"
    python3 server.py 8000
elif command -v python &> /dev/null; then
    echo "✅ Python найден"
    python server.py 8000
else
    echo "❌ Python не найден. Запускаем простой HTTP сервер..."
    
    # Альтернативные способы запуска
    if command -v php &> /dev/null; then
        echo "✅ PHP найден, запускаем PHP сервер..."
        php -S localhost:8000
    elif command -v node &> /dev/null; then
        echo "✅ Node.js найден, запускаем HTTP сервер..."
        npx http-server -p 8000
    else
        echo "❌ Не найден подходящий сервер. Откройте index.html в браузере вручную."
        echo "Или установите Python: https://www.python.org/downloads/"
        exit 1
    fi
fi 