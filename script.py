from flask import Flask, render_template
from ics import Calendar
import arrow
from datetime import timedelta

app = Flask(__name__)

# Словарь для соответствия номера месяца его названию на русском
month_names = {
    1: 'января',
    2: 'февраля',
    3: 'марта',
    4: 'апреля',
    5: 'мая',
    6: 'июня',
    7: 'июля',
    8: 'августа',
    9: 'сентября',
    10: 'октября',
    11: 'ноября',
    12: 'декабря',
}

@app.route('/')
def display_schedule():
    try:
        with open('calendar.ics', 'r', encoding='utf-8') as file:
            cal = Calendar(file.read())
    except FileNotFoundError:
        return "Файл 'calendar.ics' не найден."
    except Exception as e:
        return f"Произошла ошибка при чтении файла: {str(e)}"

    # Создайте словарь для хранения событий по дням
    schedule_data = {}

    # Получаем текущую дату и время с помощью Arrow
    current_datetime = arrow.now()

    for event in cal.events:
        # Прибавляем 3 часа к времени начала и конца события
        start_time = (event.begin + timedelta(hours=3)).strftime('%H:%M')
        end_time = (event.end + timedelta(hours=3)).strftime('%H:%M')

        # Извлекаем день, месяц и год события
        day = event.begin.day
        month = event.begin.month
        year = event.begin.year

        # Форматируем дату в "день месяц год"
        formatted_date = f"{day} {month_names[month]} {year}"

        # Создаем объект Arrow для события
        event_datetime = arrow.get(event.begin.datetime)

        # Проверяем, не прошло ли событие
        if event_datetime < current_datetime:
            continue  # Пропускаем прошедшие события

        # Если день уже есть в словаре, добавляем событие к нему, иначе создаем новый список событий для этого дня
        if formatted_date in schedule_data:
            schedule_data[formatted_date].append({
                'summary': event.name,
                'time_range': f"{start_time} - {end_time}",  # Отображение времени в формате "8:30 - 10:05"
                'location': event.location,
                'description': event.description
            })
        else:
            schedule_data[formatted_date] = [{
                'summary': event.name,
                'time_range': f"{start_time} - {end_time}",  # Отображение времени в формате "8:30 - 10:05"
                'location': event.location,
                'description': event.description
            }]

    # Создаем список дат и сортируем его
    sorted_dates = sorted(schedule_data.keys(), key=lambda x: arrow.get(x, "D MMMM YYYY", locale='ru'))

    # Создаем отсортированный словарь расписания
    sorted_schedule = {date: schedule_data[date] for date in sorted_dates}

    return render_template('schedule.html', schedule=sorted_schedule)

if __name__ == '__main__':
    app.run(debug=True)
