  document.addEventListener('DOMContentLoaded', () => {
    // Находим элемент <select>
    const selecter = document.querySelector('.selecter');

    // Пытаемся получить сохраненное значение из localStorage
    const savedValue = localStorage.getItem('selectedOption');

    // Если значение есть, устанавливаем его в <select>
    if (savedValue !== null) {
      selecter.value = savedValue;
    }

    // Добавляем обработчик события изменения выбора
    selecter.addEventListener('change', (event) => {
      // Получаем выбранное значение
      const selectedValue = event.target.value;

      // Сохраняем выбранное значение в localStorage
      localStorage.setItem('selectedOption', selectedValue);

      // Выводим выбранное значение в консоль (или выполняем другую логику)
      console.log('Выбрано значение:', selectedValue);

      // Пример логики в зависимости от выбранного значения
      switch (selectedValue) {
        case '0':
          console.log('Показать всех пользователей');
          break;
        case '1':
          console.log('Показать только друзей');
          break;
        case '2':
          console.log('Показать игроков с 100 и более побед');
          break;
        case '3':
          console.log('Показать игроков с 250 и более матчей');
          break;
        case '4':
          console.log('Показать игроков с 10 уровнем и выше');
          break;
        case '5':
          console.log('Показать игроков без MFP в профиле');
          break;
        case '6':
          console.log('Никого не показывать');
          break;
        default:
          console.log('Неизвестное значение');
      }
    });
  });