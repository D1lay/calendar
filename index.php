<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Расписание занятий</title>
    <!-- Подключение файла стилей -->
    <link rel="stylesheet" type="text/css" href="styles.css">
</head>
<body>
<h1>Расписание занятий</h1>

<?php
require 'vendor/autoload.php';
exec("/usr/bin/php www/d1lay.ru/script.php");
date_default_timezone_set('Europe/Moscow'); // Установка часового пояса "Europe/Moscow"

$icsFile = 'data.ics';
$vCalendar = \Sabre\VObject\Reader::read(file_get_contents($icsFile));

// Создаем массив для группировки пар по дням
$eventsByDay = [];

foreach ($vCalendar->VEVENT as $event) {
    $summary = $event->SUMMARY;

    // Изменения в этой части кода
    $start = new DateTime($event->DTSTART->getDateTime()->format('Y-m-d H:i:s'), new DateTimeZone('Europe/Moscow'));
    $end = new DateTime($event->DTEND->getDateTime()->format('Y-m-d H:i:s'), new DateTimeZone('Europe/Moscow'));

    // Добавляем смещение +3 часа
    $start->modify('+3 hours');
    $end->modify('+3 hours');

    // Получаем текущую дату и время
    $currentTime = new DateTime();

    // Проверяем, прошло ли событие
    if ($end < $currentTime) {
        continue; // Пропускаем прошедшие события
    }

    // Форматируем день недели и дату в нужный формат
    $formattedDate = $start->format('d.m');

    $dayOfWeek = $start->format('l'); // Английское название дня

    // Сопоставляем английские названия дней с русскими
    $daysTranslation = [
        'Monday' => 'Понедельник',
        'Tuesday' => 'Вторник',
        'Wednesday' => 'Среда',
        'Thursday' => 'Четверг',
        'Friday' => 'Пятница',
        'Saturday' => 'Суббота',
        'Sunday' => 'Воскресенье',
    ];

    $dayOfWeekRussian = $daysTranslation[$dayOfWeek];

    // Получаем аудиторию и преподавателя (если они есть)
    $location = isset($event->LOCATION) ? $event->LOCATION->__toString() : 'Не указано';
    $teacher = isset($event->DESCRIPTION) ? $event->DESCRIPTION->__toString() : 'Не указан';

    // Создаем запись для дня, включая дату, если её нет
    $dayKey = "$dayOfWeekRussian {$formattedDate}";
    if (!isset($eventsByDay[$dayKey])) {
        $eventsByDay[$dayKey] = [];
    }

    // Добавляем событие в соответствующий день
    $eventsByDay[$dayKey][] = [
        'summary' => $summary,
        'start' => $start->format('H:i'),
        'end' => $end->format('H:i'),
        'location' => $location,
        'teacher' => $teacher,
    ];
}

// Выводим информацию из файла update_info.txt
$updateInfo = file_get_contents('update_info.txt');
echo "<p><strong>Информация:</strong> $updateInfo</p>";

// Выводим события по дням
foreach ($eventsByDay as $day => $events) {
    echo "<div class='day'>"; // Добавлен контейнер для дня
    echo "<h2>$day</h2>";
    foreach ($events as $event) {
        echo "<div class='event'>";
        echo "<p><strong>Название:</strong> {$event['summary']}</p>";
        echo "<p><strong>Начало:</strong> {$event['start']}</p>";
        echo "<p><strong>Окончание:</strong> {$event['end']}</p>";
        echo "<p><strong>Аудитория:</strong> {$event['location']}</p>";
        echo "<p><strong></strong> {$event['teacher']}</p>";
        echo "</div>";
    }
    echo "</div>"; // Закрытие контейнера для дня
}
?>
<script>
</script>
</body>
</html>
