import requests
import time
from bs4 import BeautifulSoup

n = 0
while n < 100:
    # для того чтобы длина строки не превышала нужную нам длину
    # ссылку и формат документа переносим на следующую строку
    url = "https://www.google.com/search?q=google+filetype:docx&newwindow=1&" \
          "sxsrf=ALeKk01QHfWV0nYu2wVQLF1TCf0LvRHazA:1600013361904&ei=MUReX9n" \
          f"PNs_1qwHg642oDw&start={n}&sa=N&ved=2ahUKEwiZrMmgwubrAhXP-ioK" \
          "HeB1A_U4ChDy0wN6BAgEDA&biw=1422&bih=642"
    doc = 'application/vnd.openxmlformats-' \
          'officedocument.wordprocessingml.document'
    # соединяем строки получая целую ссылку
    url = "".join(url)
    # соединяем строки получая целый документ
    doc = "".join(doc)
    # объявляем ссылку
    href = ''
    # чтобы не было много запросов используем функцию ожидания
    # котрая останавливает выполнение программы на 5 секунд
    time.sleep(5)

    # отправим get-запрос на сайт и сохраним ответ в переменную
    response = requests.get(url)
    # прогоняем документ через bs4, это дает нам объект bs4
    # он представляет собой документ в виде вложенной структуры "html.parser"
    soup = BeautifulSoup(response.text, 'html.parser')
    # с помощью функции поиска bs4 находим
    # и берем нужные теги div в ходе страницы запроса и в них находим теги a
    for div in soup.find_all("div", class_="kCrYT"):
        for a in div.find_all("a"):
            # если тег не содержит class h3 берем ссылку
            z = a.find('h3')
            if z is not None:
                href = a.get('href')

                # объявляем массив для записи правильных букв
                print_letters = []
                # для вывода ссылки только один раз объявим переменную output
                output = 0

                # для вывода правильной ссылки
                # удаляем из начала ссылки часть "/url?q="
                # идем по буквам и удаляем всё что есть после &
                deleted_start = href[7:]
                for letter in deleted_start:
                    if letter == '&' and output != 1:
                        url = ''.join(print_letters)  # делаем строку из списка
                        output = +1
                    else:
                        print_letters.append(letter)

                # чтобы не было много запросов используем функцию ожидания
                # котрая останавливает выполнение программы на 5 секунд
                time.sleep(5)

                # отправим get-запрос на сайт и сохраним ответ в переменную
                response = requests.get(url)
                # если в заголовках, есть mime-тип который нужен
                # берем название файла
                # для этого находим последний слэш и место где он находится
                # берем все что есть после него
                if response.headers['Content-Type'].find(doc) != -1:
                    find_symbol = '/'
                    number = url.rfind(find_symbol)
                    title = url[number:]
                    title = 'files' + title

                    # скачиваем файл
                    with open(title, 'wb') as f:
                        f.write(response.content)
                    f.close()

    # добавим 10 чтобы перейти на следующую страницу
    n += 10
