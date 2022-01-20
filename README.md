# Скачивание случайного комикса и публикация его во Вконтакте

Программа позволяет скачивать комиксы с сайта [xkcd.com](https://xkcd.com) и публиковать их во Вконтакте.  

### Как установить

Для указания папки, куда необходимо сохранять скаченный комикс, используйте переменную окружения `PATH_TO_IMAGES`, если не указана, используется путь по умолчанию `./images/`.  
Для публикации комиксов на сайте Вконтакте с использованием [API](https://api.vk.com), необходимо сделать следующие:  
Получить ACCESS_TOKEN и сохранить его в переменную окружения `VK_TOKEN_ID`.  
Для отправки комиксов в группу, необходимо получить ID группы и сохранить его переменную окружения `VK_GROUP_ID`.  

Python3 должен быть уже установлен.
Затем используйте `pip` (или `pip3`, есть конфликт с Python2) для установки зависимостей:
```
pip install -r requirements.txt
```

### Как запускать
```
python3 main.py
```

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).