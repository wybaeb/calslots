#!/bin/bash

# Скрипт установки зависимостей для Mac Calendar Free Slots Finder

echo "🗓️  Mac Calendar Free Slots Finder - Установка"
echo "================================================"

# Проверяем, что мы на macOS
if [[ "$(uname)" != "Darwin" ]]; then
    echo "❌ Этот скрипт работает только на macOS"
    exit 1
fi

# Функция для установки Homebrew
install_homebrew() {
    echo "🍺 Устанавливаю Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    
    # Добавляем Homebrew в PATH для Apple Silicon Macs
    if [[ -f "/opt/homebrew/bin/brew" ]]; then
        echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
        eval "$(/opt/homebrew/bin/brew shellenv)"
    fi
    
    # Для Intel Macs
    if [[ -f "/usr/local/bin/brew" ]]; then
        echo 'eval "$(/usr/local/bin/brew shellenv)"' >> ~/.zprofile  
        eval "$(/usr/local/bin/brew shellenv)"
    fi
}

# Проверяем наличие Homebrew
if ! command -v brew &> /dev/null; then
    echo "🍺 Homebrew не найден"
    echo "💡 Homebrew - это пакетный менеджер для macOS, который упростит установку Python"
    echo ""
    read -p "Хотите установить Homebrew? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        install_homebrew
        if [ $? -eq 0 ]; then
            echo "✅ Homebrew установлен успешно!"
        else
            echo "❌ Ошибка при установке Homebrew"
            echo "💡 Вы можете установить Python вручную с https://python.org"
            exit 1
        fi
    else
        echo "💡 Без Homebrew установка будет сложнее"
        echo "💡 Вы можете установить Python вручную с https://python.org"
        echo "💡 Или запустить этот скрипт позже после установки Homebrew"
        exit 1
    fi
else
    echo "✅ Homebrew найден"
fi

# Проверяем наличие Python
if ! command -v python3 &> /dev/null; then
    echo "🐍 Python 3 не найден"
    echo "💡 Python необходим для работы Calendar Slots"
    echo ""
    read -p "Хотите установить Python через Homebrew? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "🔧 Устанавливаю Python..."
        brew install python3
        if [ $? -eq 0 ]; then
            echo "✅ Python установлен успешно!"
        else
            echo "❌ Ошибка при установке Python"
            exit 1
        fi
    else
        echo "❌ Python необходим для работы приложения"
        echo "💡 Установите Python с https://python.org и запустите скрипт снова"
        exit 1
    fi
fi

echo "✅ Python найден: $(python3 --version)"

# Проверяем наличие pip
if ! command -v pip3 &> /dev/null; then
    echo "📦 pip не найден"
    echo "💡 pip необходим для установки зависимостей Python"
    echo ""
    read -p "Хотите установить pip? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "🔧 Устанавливаю pip..."
        python3 -m ensurepip --upgrade
        if [ $? -eq 0 ]; then
            echo "✅ pip установлен успешно!"
        else
            echo "❌ Ошибка при установке pip"
            exit 1
        fi
    else
        echo "❌ pip необходим для установки зависимостей"
        exit 1
    fi
fi

echo "✅ pip найден"

# Создаем виртуальное окружение (настоятельно рекомендуется)
echo ""
echo "🔧 Создание виртуального окружения"
echo "💡 Виртуальное окружение изолирует зависимости проекта"
echo "💡 Это предотвращает конфликты с другими Python проектами"
echo ""
read -p "Создать виртуальное окружение? (рекомендуется) (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🔧 Создаю виртуальное окружение..."
    python3 -m venv venv
    echo "✅ Виртуальное окружение создано"
    
    # Активируем виртуальное окружение
    source venv/bin/activate
    echo "✅ Виртуальное окружение активировано"
else
    echo "⚠️  Виртуальное окружение не создано"
    echo "💡 Зависимости будут установлены глобально"
fi

# Устанавливаем зависимости
echo ""
echo "📦 Установка зависимостей Python..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Зависимости установлены успешно!"
else
    echo "❌ Ошибка при установке зависимостей"
    exit 1
fi

# Делаем скрипты исполняемыми
chmod +x calendar_slots.py
chmod +x move_to_desktop.sh

echo ""
echo "🎉 Установка завершена!"
echo ""

# Предлагаем создать ярлык на рабочем столе
echo "🖥️  Создание ярлыка на рабочем столе"
echo "💡 Ярлык позволит запускать Calendar Slots одним кликом"
echo "💡 Он будет автоматически находить проект и показывать свободные слоты"
echo ""
read -p "Создать ярлык на рабочем столе? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "🔧 Создаю ярлык на рабочем столе..."
    ./move_to_desktop.sh
else
    echo ""
    echo "📖 Ярлык не создан. Для запуска используйте:"
    echo "   python3 calendar_slots.py"
    echo ""
    echo "💡 Чтобы создать ярлык позже, выполните:"
    echo "   ./move_to_desktop.sh"
fi

echo ""
echo "🎊 Поздравляем! Calendar Slots готов к работе!"
echo ""
echo "📚 Полезные команды:"
echo "   python3 calendar_slots.py              # Базовый запуск"
echo "   python3 calendar_slots.py --verbose    # Подробный режим"
echo "   python3 calendar_slots.py --help       # Все параметры"
echo ""
echo "💡 При первом запуске macOS запросит доступ к календарю"
echo "💡 Результаты автоматически копируются в буфер обмена"
echo ""
echo "🚀 Готово! Приятного использования!" 