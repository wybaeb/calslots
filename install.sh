#!/bin/bash

# Скрипт установки зависимостей для Mac Calendar Free Slots Finder

echo "🗓️  Mac Calendar Free Slots Finder - Установка"
echo "================================================"

# Проверяем, что мы на macOS
if [[ "$(uname)" != "Darwin" ]]; then
    echo "❌ Этот скрипт работает только на macOS"
    exit 1
fi

# Проверяем наличие Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 не найден. Пожалуйста, установите Python 3"
    exit 1
fi

echo "✅ Python найден: $(python3 --version)"

# Проверяем наличие pip
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip не найден. Пожалуйста, установите pip"
    exit 1
fi

echo "✅ pip найден"

# Создаем виртуальное окружение (опционально)
read -p "Создать виртуальное окружение? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🔧 Создаю виртуальное окружение..."
    python3 -m venv venv
    echo "✅ Виртуальное окружение создано"
    echo "📝 Для активации используйте: source venv/bin/activate"
    
    # Активируем виртуальное окружение
    source venv/bin/activate
    echo "✅ Виртуальное окружение активировано"
fi

# Устанавливаем зависимости
echo "📦 Устанавливаю зависимости..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Зависимости установлены успешно!"
else
    echo "❌ Ошибка при установке зависимостей"
    exit 1
fi

# Делаем скрипт исполняемым
chmod +x calendar_slots.py

echo "🎉 Установка завершена!"
echo ""
echo "📖 Для запуска используйте:"
echo "   python3 calendar_slots.py"
echo ""
echo "💡 При первом запуске macOS запросит доступ к календарю" 