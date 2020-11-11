from bs4 import BeautifulSoup
import requests
import logging
import os
import time

logging.basicConfig(filename='log.txt', filemode='a',
                    format='%(asctime)s %(msecs)d- %(process)d -%(levelname)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S %p',
                    level=logging.DEBUG)

# добавляем 10 чтобы перейти на следующую страницу
for n in range(0, 100, 10):
    logging.info("cycle start")
    print(n)
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
        for div in soup.find_all("div", class_="yuRUbf"):
            for a in div.find_all("a"):

                # если тег не содержит class h3 берем ссылку
                if a.find('h3') is not None:
                    url = a.get('href')

                    # изменим headers
                    headers.update({'Accept-Encoding': 'gzip, deflate, br'})
                    # отправим get-запрос на сайт, сохраним ответ в переменную
                    response = requests.get(url, timeout=25, headers=headers)

                    # если в заголовках, есть Content-Type
                    # и mime-тип который нужен берем название файла
                    # для этого находим последний слэш и место где он находится
                    # берем все что есть после него
                    if response.headers.get('Content-Type') is not None:
                        if doc in response.headers['Content-Type']:

                            # создаем папку files
                            if not os.path.isdir("files"):
                                os.mkdir("files")

                            # создаем название файла
                            for span_class in a.find_all("span", class_="dyjrff qzEoUe"):
                                for span in span_class.find_all("span"):
                                    name = ' '.join(span.contents)
                                    # удаляем из начала ссылки часть
                                    title = name[name.rfind('›') + len('> '):]
                                    if '/' in title:
                                        title = title.replace('/', '.')

                                    # если в названии ссылки есть '...'
                                    # и в ссылке нет '%'
                                    # то стараемся привести ее к виду без '...'
                                    if '...' in title:
                                        if '%' not in url:
                                            title = url[url.rfind('/') + len('/'):]

                                    # добавляем в конец файла расширение
                                    # если расширения нету
                                    if not title.endswith('.docx'):
                                        title = title + '.docx'

                                    # если скаченный файл существует
                                    # то новый будет иметь название файл(1) или файл(2) и т.д.
                                    num = 0
                                    repeat_title = title
                                    while os.path.exists('files/' + title):
                                        num += 1
                                        title = f"{repeat_title[:repeat_title.rfind('.')]} ({num}).docx"
                                    print(title)

                                    # скачиваем файл
                                    with open('files/' + title, 'wb') as f:
                                        f.write(response.content)
                                    f.close()

    except requests.exceptions.ReadTimeout:
        # переподключение к серверу
        time.sleep(3)
        logging.error('Error. Read timeout occured.')

    except requests.exceptions.ConnectionError:
        # переподключение к серверу
        time.sleep(3)
        logging.error('Error. Connection timeout occured.')

    except Exception:
        logging.error('Unknown error.')

logging.info("end of program")
