#!/usr/bin/env python3
"""
Mac Calendar Free Slots Finder
Скрипт для поиска свободных слотов в Mac календаре для планирования встреч.
"""

import datetime
from datetime import timedelta
import sys
import os
import time
import threading
import argparse
import subprocess

try:
    from EventKit import EKEventStore, EKEntityTypeEvent
    from Foundation import NSDate, NSCalendar, NSCalendarUnitDay, NSCalendarUnitWeekOfYear
    import objc
    HAS_EVENTKIT = True
except ImportError:
    HAS_EVENTKIT = False
    print("EventKit не найден. Установите pyobjc: pip install pyobjc-framework-EventKit")


def copy_to_clipboard(text):
    """Копирует текст в буфер обмена на Mac."""
    try:
        process = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE, text=True)
        process.communicate(input=text)
        return True
    except Exception as e:
        print(f"❌ Ошибка копирования в буфер: {e}")
        return False


class CalendarConfig:
    """Конфигурация для поиска свободных слотов."""
    
    def __init__(self):
        # Рабочие часы по умолчанию
        self.working_hours_start = 8  # 8:00
        self.working_hours_end = 19   # 19:00
        
        # Рабочие дни (0=понедельник, 6=воскресенье)
        self.working_days = [0, 1, 2, 3, 4]  # Понедельник-Пятница
        
        # Количество недель для анализа
        self.weeks_count = 2  # Текущая + следующая неделя
        
        # Начальная дата (None = автоматически с текущей недели)
        self.start_date = None
        
        # Конечная дата (None = автоматически на основе weeks_count)
        self.end_date = None
        
        # Минимальная длительность свободного слота в минутах
        self.min_slot_duration = 30
    
    def get_working_days_names(self):
        """Возвращает названия рабочих дней."""
        day_names = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
        return [day_names[i] for i in self.working_days]


class MacCalendarManager:
    """Класс для работы с Mac календарем."""
    
    def __init__(self):
        if not HAS_EVENTKIT:
            raise ImportError("EventKit не доступен")
            
        self.event_store = EKEventStore.alloc().init()
        self.access_granted = False
        self.request_access()
    
    def request_access(self):
        """Запрашивает доступ к календарю."""
        # Используем семафор для синхронизации
        semaphore = threading.Semaphore(0)
        granted = [False]
        
        def completion_handler(access_granted, error):
            granted[0] = access_granted
            if error:
                print(f"❌ Ошибка при запросе доступа: {error}")
            semaphore.release()
        
        # Запрашиваем доступ асинхронно
        self.event_store.requestAccessToEntityType_completion_(
            EKEntityTypeEvent, 
            completion_handler
        )
        
        # Ждем ответа пользователя (максимум 30 секунд)
        if semaphore.acquire(timeout=30):
            if granted[0]:
                self.access_granted = True
                return True
            else:
                self.access_granted = False
                return False
        else:
            self.access_granted = False
            return False
    
    def get_events_for_date_range(self, start_date, end_date):
        """Получает события для заданного диапазона дат."""
        if not self.access_granted:
            print("❌ Доступ к календарю не предоставлен")
            return []
            
        # Конвертируем Python datetime в NSDate
        start_ns = NSDate.dateWithTimeIntervalSince1970_(start_date.timestamp())
        end_ns = NSDate.dateWithTimeIntervalSince1970_(end_date.timestamp())
        
        # Создаем предикат для поиска событий
        predicate = self.event_store.predicateForEventsWithStartDate_endDate_calendars_(
            start_ns, end_ns, None
        )
        
        # Получаем события
        events = self.event_store.eventsMatchingPredicate_(predicate)
        
        # Конвертируем в Python объекты
        python_events = []
        for event in events:
            if event.startDate() and event.endDate():
                start_time = datetime.datetime.fromtimestamp(event.startDate().timeIntervalSince1970())
                end_time = datetime.datetime.fromtimestamp(event.endDate().timeIntervalSince1970())
                
                python_events.append({
                    'title': str(event.title()),
                    'start': start_time,
                    'end': end_time,
                    'all_day': event.isAllDay()
                })
        
        return sorted(python_events, key=lambda x: x['start'])


class FreeSlotsFinder:
    """Класс для поиска свободных слотов."""
    
    def __init__(self, config: CalendarConfig):
        self.config = config
    
    def get_date_range(self):
        """Возвращает диапазон дат для анализа."""
        if self.config.start_date and self.config.end_date:
            # Используем заданные даты
            return self.config.start_date, self.config.end_date
        
        today = datetime.date.today()
        
        if self.config.start_date:
            # Начальная дата задана, конечная вычисляется
            start_date = self.config.start_date
            end_date = start_date + timedelta(weeks=self.config.weeks_count)
        else:
            # Автоматически с текущей недели
            days_since_monday = today.weekday()
            start_date = today - timedelta(days=days_since_monday)
            end_date = start_date + timedelta(weeks=self.config.weeks_count)
        
        return start_date, end_date
    
    def get_weeks_in_range(self, start_date, end_date):
        """Разбивает диапазон на недели."""
        weeks = []
        current_week_start = start_date
        
        while current_week_start < end_date:
            current_week_end = current_week_start + timedelta(days=6)
            if current_week_end > end_date:
                current_week_end = end_date
            
            weeks.append((current_week_start, current_week_end))
            current_week_start += timedelta(days=7)
        
        return weeks
    
    def is_working_day(self, date):
        """Проверяет, является ли день рабочим."""
        return date.weekday() in self.config.working_days
    
    def find_free_slots(self, events, date):
        """Находит свободные слоты на определенную дату."""
        if not self.is_working_day(date):
            return []
        
        now = datetime.datetime.now()
        today = now.date()
        
        # Пропускаем прошедшие дни
        if date < today:
            return []
            
        # Фильтруем события только на эту дату
        day_events = [
            event for event in events 
            if event['start'].date() == date and not event['all_day']
        ]
        
        # Создаем временные слоты для рабочего дня
        day_start = datetime.datetime.combine(date, datetime.time(self.config.working_hours_start, 0))
        day_end = datetime.datetime.combine(date, datetime.time(self.config.working_hours_end, 0))
        
        # Если это сегодня, начинаем с текущего времени
        if date == today:
            day_start = max(day_start, now)
            # Если рабочий день уже закончился, не показываем слоты
            if day_start >= day_end:
                return []
        
        # Если нет событий, весь день свободен
        if not day_events:
            return [(day_start, day_end)]
        
        free_slots = []
        current_time = day_start
        
        for event in day_events:
            event_start = max(event['start'], day_start)
            event_end = min(event['end'], day_end)
            
            # Если есть свободное время перед событием
            if current_time < event_start:
                slot_duration = (event_start - current_time).total_seconds() / 60
                if slot_duration >= self.config.min_slot_duration:
                    free_slots.append((current_time, event_start))
            
            # Обновляем текущее время
            current_time = max(current_time, event_end)
        
        # Проверяем свободное время после последнего события
        if current_time < day_end:
            slot_duration = (day_end - current_time).total_seconds() / 60
            if slot_duration >= self.config.min_slot_duration:
                free_slots.append((current_time, day_end))
        
        return free_slots
    
    def format_time_slot(self, start_time, end_time):
        """Форматирует временной слот для отображения."""
        duration = end_time - start_time
        hours = duration.seconds // 3600
        minutes = (duration.seconds % 3600) // 60
        
        return f"{start_time.strftime('%H:%M')} - {end_time.strftime('%H:%M')} ({hours}ч {minutes}м)"


def parse_arguments():
    """Парсит аргументы командной строки."""
    parser = argparse.ArgumentParser(
        description="Поиск свободных слотов в Mac календаре для планирования встреч"
    )
    
    parser.add_argument(
        "--start-hour", 
        type=int, 
        default=8,
        help="Начало рабочего дня (по умолчанию: 8)"
    )
    
    parser.add_argument(
        "--end-hour", 
        type=int, 
        default=19,
        help="Конец рабочего дня (по умолчанию: 19)"
    )
    
    parser.add_argument(
        "--weeks", 
        type=int, 
        default=2,
        help="Количество недель для анализа (по умолчанию: 2)"
    )
    
    parser.add_argument(
        "--start-date", 
        type=str,
        help="Начальная дата в формате YYYY-MM-DD"
    )
    
    parser.add_argument(
        "--end-date", 
        type=str,
        help="Конечная дата в формате YYYY-MM-DD"
    )
    
    parser.add_argument(
        "--min-duration", 
        type=int, 
        default=30,
        help="Минимальная длительность слота в минутах (по умолчанию: 30)"
    )
    
    parser.add_argument(
        "--include-weekends", 
        action="store_true",
        help="Включить выходные дни"
    )
    
    parser.add_argument(
        "--verbose", 
        action="store_true",
        help="Показать подробную статистику"
    )
    
    parser.add_argument(
        "--no-copy", 
        action="store_true",
        help="Не копировать результаты в буфер обмена"
    )
    
    parser.add_argument(
        "--clean-copy", 
        action="store_true",
        help="Копировать в буфер без эмоджи (чистый текст)"
    )
    
    return parser.parse_args()


def main():
    """Основная функция программы."""
    args = parse_arguments()
    
    if args.verbose:
        print("🗓️  Mac Calendar Free Slots Finder")
        print("=" * 50)
    
    if not HAS_EVENTKIT:
        print("❌ EventKit не найден. Установите зависимости:")
        if args.verbose:
            print("   pip install pyobjc-framework-EventKit")
        return
    
    # Создаем конфигурацию на основе аргументов
    config = CalendarConfig()
    config.working_hours_start = args.start_hour
    config.working_hours_end = args.end_hour
    config.weeks_count = args.weeks
    config.min_slot_duration = args.min_duration
    
    if args.include_weekends:
        config.working_days = [0, 1, 2, 3, 4, 5, 6]  # Все дни недели
    
    if args.start_date:
        config.start_date = datetime.datetime.strptime(args.start_date, "%Y-%m-%d").date()
    
    if args.end_date:
        config.end_date = datetime.datetime.strptime(args.end_date, "%Y-%m-%d").date()
    
    # Показываем настройки только в подробном режиме
    if args.verbose:
        print(f"⚙️  Настройки:")
        print(f"   • Рабочий день: {config.working_hours_start}:00 - {config.working_hours_end}:00")
        print(f"   • Рабочие дни: {', '.join(config.get_working_days_names())}")
        print(f"   • Минимальная длительность слота: {config.min_slot_duration} минут")
        print()
    
    try:
        # Инициализируем менеджер календаря
        calendar_manager = MacCalendarManager()
        
        # Проверяем доступ к календарю
        if not calendar_manager.access_granted:
            print("❌ Не удается получить доступ к календарю")
            if args.verbose:
                print("💡 Перезапустите скрипт после предоставления доступа")
                print("💡 Также проверьте Настройки → Приватность и защита → Календари")
            return
        
        finder = FreeSlotsFinder(config)
        
        # Получаем диапазон дат
        start_date, end_date = finder.get_date_range()
        
        if args.verbose:
            print(f"📅 Анализируем период с {start_date.strftime('%d.%m.%Y')} по {end_date.strftime('%d.%m.%Y')}")
            print()
        
        # Получаем все события за период
        start_datetime = datetime.datetime.combine(start_date, datetime.time(0, 0))
        end_datetime = datetime.datetime.combine(end_date, datetime.time(23, 59))
        
        if args.verbose:
            print("🔍 Получаем события из календаря...")
        events = calendar_manager.get_events_for_date_range(start_datetime, end_datetime)
        
        if args.verbose:
            print(f"📊 Найдено {len(events)} событий")
            print()
        
        # Разбиваем на недели
        weeks = finder.get_weeks_in_range(start_date, end_date)
        
        total_free_slots = 0
        total_free_hours = 0
        
        # Список для сбора результатов для копирования
        clipboard_lines = []
        
        # Анализируем каждую неделю
        for week_num, (week_start, week_end) in enumerate(weeks, 1):
            if args.verbose:
                print(f"📆 НЕДЕЛЯ {week_num}")
                print(f"   {week_start.strftime('%d.%m.%Y')} - {week_end.strftime('%d.%m.%Y')}")
                print("-" * 40)
            
            # Анализируем каждый день недели
            current_date = week_start
            week_slots = 0
            week_hours = 0
            
            while current_date <= week_end:
                if finder.is_working_day(current_date):
                    day_name = current_date.strftime('%A')
                    day_names = {
                        'Monday': 'Понедельник',
                        'Tuesday': 'Вторник', 
                        'Wednesday': 'Среда',
                        'Thursday': 'Четверг',
                        'Friday': 'Пятница',
                        'Saturday': 'Суббота',
                        'Sunday': 'Воскресенье'
                    }
                    
                    # Находим свободные слоты
                    free_slots = finder.find_free_slots(events, current_date)
                    
                    if free_slots:
                        day_header = f"🗓️  {day_names.get(day_name, day_name)} ({current_date.strftime('%d.%m.%Y')})"
                        print(f"\n{day_header}")
                        
                        # Добавляем заголовок дня в буфер (с эмоджи по умолчанию, без эмоджи для --clean-copy)
                        if clipboard_lines:  # Добавляем пустую строку между днями
                            clipboard_lines.append("")
                        
                        if args.clean_copy:
                            clipboard_lines.append(f"{day_names.get(day_name, day_name)} ({current_date.strftime('%d.%m.%Y')})")
                        else:
                            clipboard_lines.append(day_header)
                        
                        for start_time, end_time in free_slots:
                            slot_info = finder.format_time_slot(start_time, end_time)
                            print(f"   • {slot_info}")
                            
                            # Добавляем слот в буфер (с эмоджи по умолчанию, без эмоджи для --clean-copy)
                            if args.clean_copy:
                                clipboard_lines.append(f"   {slot_info}")
                            else:
                                clipboard_lines.append(f"   ✅ {slot_info}")
                            
                            # Подсчитываем статистику для verbose режима
                            if args.verbose:
                                duration = end_time - start_time
                                hours = duration.total_seconds() / 3600
                                week_hours += hours
                                total_free_hours += hours
                            
                        if args.verbose:
                            week_slots += len(free_slots)
                            total_free_slots += len(free_slots)
                    elif args.verbose:
                        print(f"\n🗓️  {day_names.get(day_name, day_name)} ({current_date.strftime('%d.%m.%Y')})")
                        print("   ❌ Нет свободных слотов для встреч")
                
                current_date += timedelta(days=1)
            
            if args.verbose:
                print(f"\n📊 Итого на неделе: {week_slots} слотов, {week_hours:.1f} часов")
                print()
        
        # Копируем результаты в буфер обмена (если не отключено)
        if not args.no_copy and clipboard_lines:
            clipboard_text = "\n".join(clipboard_lines)
            if copy_to_clipboard(clipboard_text):
                if args.clean_copy:
                    print(f"\n📋 Свободные слоты скопированы в буфер обмена (чистый текст)!")
                else:
                    print(f"\n📋 Свободные слоты скопированы в буфер обмена!")
                if args.verbose:
                    print("💡 Теперь можно вставить результаты в любое приложение (Cmd+V)")
            else:
                if args.verbose:
                    print("❌ Не удалось скопировать в буфер обмена")
        elif args.no_copy and args.verbose:
            print("\n💡 Копирование в буфер отключено параметром --no-copy")
        
        # Общая статистика только в подробном режиме
        if args.verbose:
            print("\n📈 ОБЩАЯ СТАТИСТИКА:")
            print("-" * 40)
            print(f"🔢 Всего свободных слотов: {total_free_slots}")
            print(f"⏰ Общее свободное время: {total_free_hours:.1f} часов")
            print(f"📅 Средняя загрузка: {((config.weeks_count * len(config.working_days) * (config.working_hours_end - config.working_hours_start)) - total_free_hours) / (config.weeks_count * len(config.working_days) * (config.working_hours_end - config.working_hours_start)) * 100:.1f}%")
            
            # Итоговая информация
            if total_free_slots > 0:
                print("✅ Готово! Показаны все свободные интервалы для планирования встреч")
            else:
                print("❌ Нет свободных интервалов для встреч в указанном периоде")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main() 