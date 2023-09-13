document.addEventListener("DOMContentLoaded", function () {
    const calendarContent = document.getElementById("calendarContent");

    // URL к файлу calendar.ics
    const icsFileURL = 'https://wdho.ru/b4V3/calendar.ics';

    // Загружаем содержимое файла
    fetch(icsFileURL)
        .then(response => {
            if (!response.ok) {
                throw new Error('Не удалось загрузить файл calendar.ics.');
            }
            return response.text();
        })
        .then(data => {
            // Выводим содержимое файла на странице
            calendarContent.textContent = data;
        })
        .catch(error => {
            console.error(error.message);
            calendarContent.textContent = 'Произошла ошибка: ' + error.message;
        });
});
