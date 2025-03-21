import time
import pyautogui as pag
import numpy as np
from PIL import ImageEnhance
import easyocr

# Словарь координат и регионов это нужно менять под свой компьютер
COORDS = {
    "price_region": [1319, 116, 225, 78],      # Область для детекции цены текущего запроса(x-верхнего угла,y верхнего угла,ширина,высота)
    "price_input_region": [1331, 412, 186, 56],  # Область для считывания цены для ввода(x-верхнего угла,y верхнего угла,ширина,высота
    "double_click": [1045, 346],                 # Координаты для двойного клика(галочка рядом с надписью: c наклейками)
    "target_click": [1726, 156],                 # Координаты Кнопки заказать
    "second_click": [982, 430],                  # Вторая координата клика после Кнопка на облась где написана изменяема цена после нажатия на кнопку заказать
    "extra_click": [960, 705],                   # Вторая кнопка заказать
    "final_click": [1694, 264]                   # Финальный клик(отмен запроса на покупку)
}

# Инициализация easyocr с поддержкой русского и английского языков (с использованием GPU, если доступно)
reader = easyocr.Reader(['en', 'ru'], gpu=True)

def read_price_from_region(region):
    """
    Делает скриншот указанного региона, переводит изображение в чёрно-белый формат,
    повышает контраст, отбрасывает последние два символа распознанного текста
    (например, обозначение валюты) и возвращает числовое значение.
    """
    x, y, w, h = region
    img = pag.screenshot(region=(x, y, w, h)).convert('L')
    img = ImageEnhance.Contrast(img).enhance(2.0)
    price_np = np.array(img)
    results = reader.readtext(price_np, detail=0, paragraph=False)
    if results:
        try:
            # Отбрасываем два последних символа
            text = results[0].strip()[:-2]
            text = text.replace(',', '.').replace('$', '').replace('€', '')
            return float(text)
        except ValueError:
            return None
    return None

def main():
    time.sleep(1)  # Задержка перед запуском цикла
    previous_price = None
    while True:
        current_price = read_price_from_region(COORDS['price_region'])
        if current_price is not None:
            if previous_price is not None and (current_price - previous_price) > 0.01:
                print(f"Цена возросла с {previous_price} до {current_price}.")
                # Выполняем двойной клик по заданным координатам
                pag.click(*COORDS['double_click'])
                pag.click(*COORDS['double_click'])
                time.sleep(0.1)  # Небольшая задержка для обновления экрана

                # Считываем цену для ввода после двойного клика
                input_price = read_price_from_region(COORDS['price_input_region'])
                print(f"Считанная цена для ввода: {input_price}")

                # Проверяем минимальную цену (например, 0.03)
                if input_price is not None and input_price > 0.03:
                    # Выполняем клик по первой точке (target_click)
                    pag.click(*COORDS['target_click'])
                    time.sleep(0.05)
                    # Выполняем второй клик
                    pag.click(*COORDS['second_click'])

                    # Вводим цену, уменьшенную на 0.01
                    final_price = input_price - 0.01
                    if current_price < final_price:
                        final_final_price = current_price + 0.01
                    else:
                        final_final_price = final_price

                    pag.write(f"{final_final_price:.2f}")

                    # Дополнительные клики: по (960,705), задержка 1.5 секунды, затем по (1694,264)
                    pag.click(*COORDS['extra_click'])
                    time.sleep(1.5)  # Увеличиваем задержку до 1.5 секунд
                    pag.click(*COORDS['final_click'])
                else:
                    print("Ошибка: минимальная цена слишком низкая или не распознана.")
            else:
                print(f"Цена: {current_price}")
            previous_price = current_price
        else:
            print("Ошибка считывания цены для детекции.")
        time.sleep(0.2)  # Задержка между итерациями

if __name__ == "__main__":
    main()
