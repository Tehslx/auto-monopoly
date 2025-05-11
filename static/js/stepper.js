document.addEventListener('DOMContentLoaded', () => {
  const stepperContainer = document.querySelector('.stepper-container');
  const stepperVal = stepperContainer.querySelector('.stepper-val');
  const stepperBtns = stepperContainer.querySelectorAll('.stepper-btn');
  const inputStepper = document.querySelector('.stepper-input');

  // Минимальное и максимальное значение
  const min = parseInt(inputStepper.min) || 2;
  const max = parseInt(inputStepper.max) || 5;

  // Начальное значение (пробуем получить из localStorage, иначе используем значение из HTML)
  let currentValue = parseInt(localStorage.getItem('stepperValue')) || parseInt(stepperVal.textContent);

  // Функция для обновления значения
  function updateValue(newValue) {
    // Проверяем, чтобы значение было в пределах min и max
    if (newValue < min) newValue = min;
    if (newValue > max) newValue = max;

    // Обновляем значение
    currentValue = newValue;
    stepperVal.textContent = currentValue;
    inputStepper.value = currentValue;

    // Сохраняем значение в localStorage
    localStorage.setItem('stepperValue', currentValue);
  }

  // Обработчик кликов на кнопки
  stepperBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const action = btn.getAttribute('data-action');

      if (action === 'increase') {
        updateValue(currentValue + 1);
        console.log('Значение увеличено:', currentValue); // Логируем только при изменении
      } else if (action === 'decrease') {
        updateValue(currentValue - 1);
        console.log('Значение уменьшено:', currentValue); // Логируем только при изменении
      }
    });
  });

  // Обработчик изменения значения в input
  inputStepper.addEventListener('change', () => {
    const newValue = parseInt(inputStepper.value);
    if (!isNaN(newValue)) {
      updateValue(newValue);
      console.log('Значение изменено через input:', currentValue); // Логируем только при изменении
    }
  });

  // Инициализация значения при загрузке страницы (без вывода в консоль)
  updateValue(currentValue);
});