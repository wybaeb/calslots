#!/bin/bash

# Скрипт для размещения ярлыка Calendar Slots на рабочем столе

echo "🗓️  Размещение ярлыка Calendar Slots на рабочем столе"
echo "====================================================="

# Получаем путь к рабочему столу
DESKTOP_PATH="$HOME/Desktop"

# Проверяем, что рабочий стол существует
if [ ! -d "$DESKTOP_PATH" ]; then
    echo "❌ Рабочий стол не найден по пути: $DESKTOP_PATH"
    exit 1
fi

# Проверяем наличие файла show_slots.sh
if [ ! -f "show_slots.sh" ]; then
    echo "❌ Файл show_slots.sh не найден в текущей директории"
    echo "💡 Убедитесь, что вы запускаете скрипт из директории проекта"
    exit 1
fi

# Создаем красивое имя для ярлыка
SHORTCUT_NAME="📅 Calendar Slots"
SHORTCUT_PATH="$DESKTOP_PATH/$SHORTCUT_NAME"

# Получаем текущий путь к проекту
CURRENT_DIR="$(pwd)"

# Создаем временный файл с правильным путем
echo "📂 Создаю ярлык с правильным путем к проекту..."
sed "s|PROJECT_DIR=\"/Users/admin/Sites/calslots\"|PROJECT_DIR=\"$CURRENT_DIR\"|g" show_slots.sh > "$SHORTCUT_PATH"

# Делаем скрипт исполняемым
chmod +x "$SHORTCUT_PATH"

# Проверяем успешность операции
if [ -f "$SHORTCUT_PATH" ]; then
    echo "✅ Ярлык успешно создан!"
    echo ""
    echo "📍 Расположение: $SHORTCUT_PATH"
    echo "📂 Путь к проекту: $CURRENT_DIR"
    echo ""
    echo "🚀 Теперь вы можете:"
    echo "   • Дважды кликнуть по ярлыку на рабочем столе"
    echo "   • Или запустить из Терминала: open '$SHORTCUT_PATH'"
    echo ""
    echo "💡 Ярлык будет:"
    echo "   • Показывать свободные слоты для встреч"
    echo "   • Начиная с текущего времени на 2 недели вперед"
    echo "   • Автоматически проверять доступ к календарю"
    echo ""
    echo "⚠️  Важно: Не перемещайте папку проекта $CURRENT_DIR"
    echo "   иначе ярлык перестанет работать"
else
    echo "❌ Ошибка при создании ярлыка"
    exit 1
fi

# Спрашиваем, хотим ли мы протестировать ярлык
echo ""
read -p "🧪 Хотите протестировать ярлык сейчас? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🔄 Запускаю ярлык..."
    echo ""
    open "$SHORTCUT_PATH"
fi

echo ""
echo "🎉 Готово! Ярлык размещен на рабочем столе" 