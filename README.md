# VK_to_Yandex.Music
 Transfer all your songs from VK audios to Yandex.Music service.

##### HOW TO RUN
First, you need to install two libraries in your cmd:
`pip install yandex-music`
`pip install vk_api`

Thanks to MarshalX and "Python273". There their repos:
[yandex-music](https://github.com/MarshalX/yandex-music-api)
[vk-api](https://github.com/python273/vk_api)

Next, you must create `credentials.py` in folder with script, open it in your text editor and add these strings:
```
ya_email = 'your_login_email_for_yandex@gmail.com'
ya_passw = 'your_password_for_yandex'
vk_email = 'your_email_for_login_to_vk@email.com'  # or phone-number
vk_passw = 'your_password_for_vk'
vk_id = 1234567  # your id
```
Pay attention, emails and passwords must be entered **between apostrophes**. vk_id - without apostrophes.

1. Скрипт собирает твои аудиозаписи с ВК, 
2. Сохраняет их в текстовый файл all_songs.txt в папку со скриптом если за один сеанс все треки не перенести, чтобы потом не грузить ВК запросами.
3. Идёт по каждому треку из ВК и ищет его в Яндекс.музыке. 
3.1 Если названия артистов и трека идентичны, автоматически добавляет в лайкнутые в Яндексе. 
4.1. Если не одинаковы, то скрипт тебя спросит "Совпадают ли эти треки?" и выведет: Название в ВК, название в Яндексе, Длительность трека в ВК и длительность в Яндексе.
