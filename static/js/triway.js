// triway.js

// Функция для инициализации переключателя
function initTriway(selector) {
  // Получаем элемент переключателя
  const triway = document.querySelector(selector);

  // Если элемент не найден, выходим
  if (!triway) {
    console.error('Переключатель не найден!');
    return;
  }

  // Восстановление состояния из localStorage
  const savedValue = localStorage.getItem('triwayState');
  if (savedValue) {
    triway.setAttribute('design-value', savedValue);
  }

  // Обработчик клика
  triway.addEventListener('click', function (event) {
    // Получаем текущее значение
    let currentValue = parseInt(this.getAttribute('design-value'));

    // Определяем, в какую часть переключателя был клик
    const rect = this.getBoundingClientRect();
    const clickX = event.clientX - rect.left; // Позиция клика относительно переключателя
    const thirdWidth = rect.width / 3; // Ширина одной трети переключателя

    // Определяем следующее состояние
    let nextValue;
    if (clickX < thirdWidth) {
      // Клик в левой трети
      nextValue = -1;
    } else if (clickX > 2 * thirdWidth) {
      // Клик в правой трети
      nextValue = 1;
    } else {
      // Клик в средней трети
      nextValue = 0;
    }

    // Устанавливаем новое значение
    this.setAttribute('design-value', nextValue);

    // Сохраняем состояние в localStorage
    localStorage.setItem('triwayState', nextValue);

    // Выводим новое состояние в консоль
    console.log('Новое состояние:', nextValue);
  });
}

// Инициализация переключателя
initTriway('.triway');