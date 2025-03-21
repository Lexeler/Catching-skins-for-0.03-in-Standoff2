# Catching skins for 0.03 in Standoff 2

Этот проект представляет собой автоматизированный скрипт для работы с графическим интерфейсом, который использует библиотеку `pyautogui` для управления мышью и клавиатурой, а также `easyocr` для распознавания текста на экране.

## Функциональность

- Мониторинг изменения цены запроса на скин.
- Автоматическое обновление предложений и создание запроса на 0.01 голды меньше текущей минимальной цены.
- Ловля скинов за 0.03 путем временного создания запроса и его отмены через 1.5 секунды.
- Поддержка русского и английского языков для OCR.

## Установка

1. Убедитесь, что у вас установлен Python 3.7 или выше.
2. Установите необходимые зависимости:
   ```bash
   pip install pyautogui easyocr pillow numpy
   ```
3. Убедитесь, что у вас настроен GPU для ускорения работы `easyocr` (опционально).

## Настройка

Перед использованием скрипта необходимо настроить координаты и регионы в словаре `COORDS` в файле `main.py`. Эти координаты зависят от разрешения вашего экрана и расположения элементов интерфейса.

Пример:
```python
COORDS = {
    "price_region": [1319, 116, 225, 78],      # Область для детекции цены
    "price_input_region": [1331, 412, 186, 56],  # Область для считывания цены для ввода
    "double_click": [1045, 346],                 # Координаты для двойного клика
    "target_click": [1726, 156],                 # Координаты кнопки "заказать"
    "second_click": [982, 430],                  # Координаты для второго клика
    "extra_click": [960, 705],                   # Дополнительный клик
    "final_click": [1694, 264]                   # Финальный клик
}
```

## Использование

1. Запустите скрипт:
   ```bash
   python main.py
   ```
2. Скрипт начнет мониторить изменения цены и выполнять действия в зависимости от условий.

## Примечания

- Убедитесь, что окно приложения, с которым работает скрипт, открыто и находится в фокусе.
- Ловля скинов за 0.03 возможна только при наличии активных запросов и минимальной цены.
