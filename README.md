# VK_to_Yandex.Music
 Transfer all your songs from VK audios to Yandex.Music service.

### How to run
First, you need to install two libraries in your cmd:
`pip install yandex-music`

`pip install vk_api`
Thanks to MarshalX and "Python273" for these libraries. There their repos:
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
Pay attention, emails and passwords must be entered **between apostrophes**.
`vk_id` - your VK user_id, without apostrophes. It can be find in address bar of your browser when you enter to your audios page. For example: https://vk.com/audios1234567. **1234567** - is your vk_id.

### Что делает скрипт
1. Скрипт собирает ваши аудиозаписи с ВК;
2. Сохраняет их в текстовый файл `all_songs.txt` в папку со скриптом чтобы потом при запуске скрипта была возможность загрузить треки из файла, вместо того, чтобы  грузить ВК запросами. Это на случай если за один сеанс все треки перенести не удаётся;
3. Идёт по каждому треку и ищет его в Яндекс.музыке; 
3. Если названия артистов и трека идентичны, то автоматически добавляет в лайкнутые в Яндексе; 
4. Если не одинаковы, то скрипт спросит "Совпадают ли эти треки?" и выведет название трека в ВК, название в Яндексе, длительность трека в ВК и длительность в Яндексе. Нужно будет ответить y/n. Пустой ответ считается за ответ "y".

