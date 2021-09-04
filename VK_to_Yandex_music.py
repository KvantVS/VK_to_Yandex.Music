from yandex_music import Client
from vk_api import VkApi
from vk_api.audio import VkAudio
from os.path import join, dirname, realpath, exists
import json
from credentials import *


def get_vk_songs():
    vk_sess = VkApi(login=vk_email, password=vk_passw, api_version='5.103')  #5.60
    vk_sess.auth()
    vk_aud = VkAudio(vk_sess)

    print('Получаем все песни...')
    songs = vk_aud.get(owner_id=vk_id)
    print('Треков:', len(songs))

    # Сохраняем JSON ответа со всеми треками в файл all_songs.txt:
    with open(songs_json_file_path, 'w', encoding='utf-8') as jsonfile:
        json.dump(songs, jsonfile, indent=4, sort_keys=False, ensure_ascii=False)
    return songs


# ya_email = 'your@email.ru'
# ya_passw = 'pass'

path_to_save = dirname(realpath(__file__))
songs_json_file_path = join(path_to_save, 'all_songs.txt')
# ------------------------------------------------------------------------------

client = Client.from_credentials(ya_email, ya_passw)

# Если существует файл all_songs.txt, то спросим пользователя, загрузить ли
# песни из него вместо подключения к VK
ans = 'asdasd'
from_where_to_start = 0
while ans not in ('y', 'n', ''):
    if exists(songs_json_file_path):
        ans = input('Есть файл песен all_songs.txt с предыдущей сессии. Загрузить его вместо подключения к VK? (y/n): ')

        if ans.lower().strip() == 'y' or ans.strip() == '':
            with open(songs_json_file_path, 'r', encoding='utf-8') as jsonfile:
                songs = json.load(jsonfile)

            if exists(join(path_to_save, 'from_where_to_start')):
                with open(join(path_to_save, 'from_where_to_start'), 'r') as f:
                    from_where_to_start = int(f.readline())

        elif ans.lower().strip() == 'n':
            songs = get_vk_songs()
        else:
            print('Принимаются только y, n или оставьте пустой и нажмите Enter для ответа по умолчанию (y)')
    else:
        songs = get_vk_songs()

not_founded_vk_songs = []  # список не найденых в Я.Музыке песен из ВК

# Идём по трекам
len_songs = len(songs)
for i, vk_track in enumerate(songs):
    # Перематываем до нужного номера, если загрузили номер из файла с прошлой
    # сессии
    if i < from_where_to_start:
        continue

    # Сохраняем номер трека для продолжения в другой раз
    with open(join(path_to_save, 'from_where_to_start'), 'w') as f:
        f.write(str(i))

    vk_songfullname = f"{vk_track['artist'].strip()} - {vk_track['title'].strip()}"
    vkdur = vk_track['duration']

    # ищем трек в Яндекс.музыке
    ya_search_result = client.search(text=vk_songfullname, nocorrect=True,
        type_='track', playlist_in_best=False)


    if not ya_search_result['tracks']:
        not_founded_vk_songs.append(vk_songfullname)
        print(f'({i+1} / {len_songs}) ', end='')
        print(f'[-]  {vk_songfullname} -- не найдена в Яндекс')
        continue

    ya_track = ya_search_result['tracks']['results'][0]
    artist = ', '.join([art['name'] for art in ya_track['artists']])
    ya_songfullname = f"{artist} - {ya_track['title']}"
    ydur = ya_track['duration_ms'] // 1000

    # Сравниваем песни по шаблону Артист - НазваниеПесни
    vk_songfullname_for_comparing = vk_songfullname.lower().strip().replace('ё', 'е')
    ya_songfullname_for_comparing = ya_songfullname.lower().strip().replace('ё', 'е')

    if vk_songfullname_for_comparing == ya_songfullname_for_comparing:
        print(f'({i+1} / {len_songs}) ', end='')
        print(f"[+]  {vk_songfullname}")
        client.users_likes_tracks_add(ya_track['id'])
        continue

    # --- Если песня не идентична ВКшной, выводим две строки VK трек и YA трек -
    # строка с дефисами
    print('-' * (5 + len(str(i)) + len(str(len_songs))))
    print(f'({i+1} / {len_songs}) ', end='')

    # Variant 1
    # (1 / 1966) Artist - Title (+)
    # (2 / 1966) Artist - Title (-)
    # (3 / 1966)
    # VK: Artist - Title
    # Ya: Artist - Title
    # VK длительность:     4:33
    # Yandex длительность: 4:34
    # Совпадают песни? (y/n)

    # Variant 2
    # (1 / 1966) (+) Artist - Title
    # (2 / 1966) (-) Artist - Title
    # (3 / 1966) (?) Artist - Title
    # Ya:            Artist - Title
    # VK длительность:     4:33
    # Yandex длительность: 4:34
    # Совпадают песни? (y/n)

    # Variant 3
    # (1 / 9) (+) Artist - Title
    # (2 / 9) (-) Artist - Title
    # -------
    # (3 / 9) (?) Artist - Title
    # Yandex:     Artist - Title
    # VK длительность:     4:33
    # Yandex длительность: 4:34
    # Совпадают песни? (y/n)

    # Variant 4
    # (1 / 9) (+) Artist - Title
    # (2 / 9) (-) Artist - Title
    # (3 / 9) (?) (4:33) Artist - Title
    # Yandex:     (3:34) Artist - Title
    # Совпадают песни? (y/n)

    # Variant 5
    # (10 / 900) [+]  Artist - Title
    # (20 / 900) [-]  Artist - Title
    # ----------
    # (30 / 900) [?]  (4:33) Artist - Title
    #    Yandex:      (3:34) Artist - Title
    #                 Совпадают песни? (y/n)

    # Подсчёт пробелов для форматирования яндекс-строки
    # (3 / 9) (?)   -- 10 символов + кол-во порядков в i + кол-во порядков в len(songs)
    # (566 / 1975) (?)   -- 17
    # Yandex:   -- len(Yandex:) = 8.   => 17-8 и -4 (это место под знаком [?])

    spaces_count_for_ya_string = 10 + len(str(i)) + len(str(len_songs)) - 12
    spaces_str = ' ' * spaces_count_for_ya_string

    # VK-строка
    print(f"[?]  ({vkdur // 60}:{vkdur % 60:02d}) {vk_songfullname}")

    # YA-строка
    yandex_template = f"{spaces_str}Yandex:      ({ydur // 60}:{ydur % 60:02d}) {ya_songfullname}"
    yandex_string = yandex_template + f" ({ya_track['version']})" if ya_track['version'] else yandex_template
    print(yandex_string)

    # Вопрос пользователю. Вначале считаем кол-во пробелов для красивого вывода
    spaces_count_for_question_string = 11 + len(str(i)) + len(str(len_songs))
    spaces_str = ' ' * spaces_count_for_question_string
    ans = 'asd'
    while ans not in ('y', 'n', ''):
        ans = input(spaces_str + 'Совпадают песни? (y/n) (нажатие Enter с пустым '
                    'ответом равно ответу "y"): ')
        if ans.lower().strip() == 'n':
            not_founded_vk_songs.append(vk_songfullname)
        elif ans.lower() == 'y' or ans.strip() == '':
            client.users_likes_tracks_add(ya_track['id'])
            pass
        else:
            print('Принимаются только y-Да, n-Нет (пропустить). Или оставь'
                  'те пустой и нажмите Enter для ответа по умолчанию (y)')
    # print('-------------')

# Сохраняем ненайденые в Яндексе песни в файл not_founded_vk_songs.txt
with open(join(path_to_save, 'not_founded_vk_songs.txt'), 'w', encoding='utf-8') as f:
    for song in not_founded_vk_songs:
        f.write(song + '\n')

print(f"Не перенеслось песен: {len(not_founded_vk_songs)}. Их список сохранен "
      f"в файле {path_to_save}\\not_founded_vk_songs.txt")
