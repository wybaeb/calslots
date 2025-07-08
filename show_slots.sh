#!/bin/bash

# Mac Calendar Free Slots - Ярлык для рабочего стола
# Скрипт для быстрого показа свободных слотов для встреч

# Автоматически определяем путь к проекту
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Если скрипт запущен с рабочего стола, ищем проект в стандартных местах
if [[ "$SCRIPT_DIR" == *"/Desktop"* ]]; then
    # Проверяем стандартные пути
    POSSIBLE_PATHS=(
        "$HOME/Sites/calslots"
        "$HOME/Projects/calslots"
        "$HOME/Documents/calslots"
        "$HOME/calslots"
    )
    
    PROJECT_DIR=""
    for path in "${POSSIBLE_PATHS[@]}"; do
        if [ -d "$path" ] && [ -f "$path/calendar_slots.py" ]; then
            PROJECT_DIR="$path"
            break
        fi
    done
    
    # Если не найден, спрашиваем у пользователя
    if [ -z "$PROJECT_DIR" ]; then
        echo "❌ Не могу найти проект calslots!"
        echo "💡 Укажите полный путь к папке проекта:"
        read -p "Путь: " PROJECT_DIR
        
        if [ ! -d "$PROJECT_DIR" ] || [ ! -f "$PROJECT_DIR/calendar_slots.py" ]; then
            echo "❌ Неверный путь к проекту!"
            read -p "Нажмите Enter для выхода..."
            exit 1
        fi
    fi
else
    PROJECT_DIR="$SCRIPT_DIR"
fi

# Переходим в директорию проекта
cd "$PROJECT_DIR"

# Показываем найденный путь проекта
echo "📂 Проект найден: $PROJECT_DIR"
echo ""

# Проверяем наличие виртуального окружения
if [ ! -d "venv" ]; then
    echo "❌ Виртуальное окружение не найдено!"
    echo "💡 Запустите install.sh для настройки проекта в $PROJECT_DIR"
    echo ""
    read -p "Нажмите Enter для выхода..."
    exit 1
fi

# Проверяем наличие Python скрипта
if [ ! -f "calendar_slots.py" ]; then
    echo "❌ Файл calendar_slots.py не найден!"
    echo "💡 Убедитесь, что проект находится в $PROJECT_DIR"
    echo ""
    read -p "Нажмите Enter для выхода..."
    exit 1
fi

# Активируем виртуальное окружение
source venv/bin/activate

# Показываем заголовок
echo "🗓️  Свободные слоты для встреч"
echo "================================"
echo ""

# Проверяем доступ к календарю через AppleScript
echo "🔍 Проверяю доступ к календарю..."
if ! osascript -e 'tell application "Calendar" to get name of first calendar' >/dev/null 2>&1; then
    echo "❌ Нет доступа к календарю!"
    echo ""
    echo "💡 Необходимо предоставить доступ к календарю:"
    echo "   1. Откройте Настройки системы (System Settings)"
    echo "   2. Перейдите в Приватность и защита (Privacy & Security)"
    echo "   3. Выберите Календари (Calendars)"
    echo "   4. Включите доступ для Terminal"
    echo ""
    echo "🔄 Или попробуйте запустить эту команду для получения доступа:"
    echo "   osascript -e 'tell application \"Calendar\" to get name of first calendar'"
    echo ""
    read -p "Нажмите Enter, чтобы попробовать снова, или Ctrl+C для выхода..."
    
    # Попытка получить доступ через AppleScript
    echo "🔄 Попытка получить доступ..."
    osascript -e 'tell application "Calendar" to get name of first calendar'
    
    if [ $? -eq 0 ]; then
        echo "✅ Доступ к календарю получен!"
        echo ""
    else
        echo "❌ Доступ по-прежнему не получен"
        echo "💡 Настройте доступ вручную в Настройках системы"
        echo ""
        read -p "Нажмите Enter для выхода..."
        exit 1
    fi
fi

# Запускаем Python скрипт
echo "🗓️ Получаю свободные слоты..."
echo ""
python3 calendar_slots.py

# Показываем инструкцию
echo ""
echo "💡 Команды:"
echo "   • Для подробного режима: python3 calendar_slots.py --verbose"
echo "   • Для 1 недели: python3 calendar_slots.py --weeks 1"  
echo "   • Для других часов: python3 calendar_slots.py --start-hour 9 --end-hour 20"
echo ""
echo "📋 Результат можно копировать и отправлять для планирования встреч"
echo ""

# Ждем нажатия Enter перед закрытием
read -p "Нажмите Enter для выхода..." 