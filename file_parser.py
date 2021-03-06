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

    # объявляем ссылку
    href = ''

    # зададим headers,отправим get-запрос на сайт и сохраним ответ в переменную
    headers = {
        # указываем программное обеспечение клиента и его характеристики
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv: 69.0) '
                      'Gecko/20100101 Firefox/69.0',
        # указываем список допустимых форматов ресурса
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;'
                  'q=0.8',
        # указываем один или несколько естественных языков содержимого
        'Accept-Language': 'ru,en-US;q=0.5',
        # указываем перечень поддерживаемых способов кодирования содержимого
        # сущности при передаче
        'Accept-Encoding': 'gzip, deflate',
        # указываем Do Not Track для отключения отслеживания веб - службами
        'DNT': '1',
        # указываем сведения о проведении соединения
        'Connection': 'keep-alive',
        # обновления небезопасных запросов до безопасной альтернативы
        # до того, как браузер их получит
        'Upgrade-Insecure-Requests': '1',
        # указываем особенные опции выполнения операции
        'Pragma': 'no-cache',
        # указываем основные директивы для управления кэшированием
        'Cache-Control': 'no-cache'
    }
    try:
        response = requests.get(url, headers=headers)

        # прогоняем документ через bs4, это дает нам объект bs4, который
        # представляет собой документ в виде вложенной структуры "html.parser"
        soup = BeautifulSoup(response.text, 'html.parser')

        # с помощью функции поиска bs4 находим и берем нужные теги div в коде
        # страницы запроса и в них находим теги a
        for div in soup.find_all("div", class_="r"):
            for a in div.find_all("a"):
                # если тег не содержит class h3 берем ссылку
                z = a.find('h3')
                if z is not None:
                    href = a.get('href')

                    # объявляем массив для записи правильных букв
                    print_letters = []
                    # для вывода ссылки один раз объявим переменную output
                    output = 0
                    url = []

                    # для вывода правильной ссылки
                    # идем по буквам и удаляем всё что есть после &
                    for letter in href:
                        if letter == '?' and output != 1:
                            output = +1
                        if output != 1:
                            print_letters.append(letter)
                    url = ''.join(print_letters)  # делаем строку из списка

                    # изменим headers
                    headers.update({'Accept-Encoding': 'gzip, deflate, br'})
                    # отправим get-запрос на сайт, сохраним ответ в переменную
                    response = requests.get(url, timeout=25, headers=headers)

                    # если в заголовках, есть Content-Type
                    # и mime-тип который нужен берем название файла
                    # для этого находим последний слэш и место где он находится
                    # берем все что есть после него
                    if response.headers.get('Content-Type') is not None:
                        if response.headers['Content-Type'].find(doc) != -1:
                            # если в названии ссылки нет ...
                            if url.find("...") == -1:
                                for spa in a.find_all("span", class_="eipWBe"):
                                    for span in spa.find_all("span"):
                                        name = " ".join(span.contents)
                                        find_symbol = '›'
                                        number = name.rfind(find_symbol)
                                        # удаляем из начала ссылки часть
                                        deleted_start = name[number + 2:]
                                        title = deleted_start[0:]
                                        if title.find('/'):
                                            title = title.replace('/', '.')
                                        title = 'files/' + title
                                        # добавляем в конец файла расширение
                                        # если расширения нету
                                        if title.find('.docx') == -1:
                                            title = title + '.docx'

                                        # скачиваем файл
                                        with open(title, 'wb') as f:
                                            f.write(response.content)
                                        f.close()
                            else:
                                find_symbol = '/'
                                number = url.rfind(find_symbol)
                                title = url[number:]
                                title = 'files' + title
                                # добавляем в конец файла расширение
                                # если расширения нету
                                if title.find('.docx') == -1:
                                    title = title + '.docx'
                                
                                # скачиваем файл
                                with open(title, 'wb') as f:
                                    f.write(response.content)
                                f.close()

    except requests.exceptions.ReadTimeout:
        # переподключение к серверу
        time.sleep(3)
    except requests.exceptions.ConnectionError:
        # переподключение к серверу
        time.sleep(3)

    # добавим 10 чтобы перейти на следующую страницу
    n += 10
