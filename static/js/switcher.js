// toggle.js

// Функция для инициализации переключателя
function initToggle(selector) {
  // Получаем элемент переключателя
  const toggle = document.querySelector(selector);

  // Если элемент не найден, выходим
  if (!toggle) {
    console.error('Переключатель не найден!');
    return;
  }

  // Восстановление состояния из localStorage
  const savedState = localStorage.getItem('toggleState');
  if (savedState !== null) {
    toggle.checked = savedState === 'true';
  }

  // Обработчик изменения состояния
  toggle.addEventListener('change', function () {
    // Сохраняем состояние в localStorage
    localStorage.setItem('toggleState', this.checked);

    // Выводим новое состояние в консоль
    console.log('Переключатель:', this.checked ? 'Включен' : 'Выключен');
  });
}

// Инициализация переключателя
initToggle('#toggleSwitch');