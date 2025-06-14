document.addEventListener('DOMContentLoaded', () => {
    // Верхняя навигация
    const navToggle = document.querySelector('.menu-button'); // Кнопка, которая раскрывает меню
    const navMenu = document.getElementById('categoryMenu'); // Меню, которое будет раскрыто

    navToggle.addEventListener('click', () => {
        navMenu.classList.toggle('active'); // Добавляем или удаляем класс active
    });

});
