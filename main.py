import speech_recognition
from gtts import gTTS
from io import BytesIO
import os
import sounddevice as sd
import soundfile as sf
import random
import subprocess
import webbrowser
import pygetwindow as gw
import pyautogui

sr = speech_recognition.Recognizer()
sr.pause_threshold = 0.9

repeat_after_me = False

jarvis_status = 0

commands_back = ['отбой','забыли','перехотел', 'всё давай назад', 'вернись назад', 'больше не хочу', "больше не надо", "назад", "отмена", "нет отмена", "отменяем", "передумал", "откат"]

commands_dict = {
    'commands':{
        'repeat_mode_on':["джарвис повторение", "джарвис повторяй за мной", 'начинай повторение','повтори за мной', 'повторяй за мной', 'режим повторения', 'включить режим повторения', 'начать повторение', 'повторение', 'начать режим повторения'],
        'repeat_mode_off':['заканчивай повторять','хватит повторять', 'выключить режим повторения', 'конец повторения'],
        'greetings':['здорово джарвис','приветик джонс','приветик джарвис','привет','приветик','привет джарвис','джарвис привет','приветствую', 'приветствую джарвис','приветики','приветики пистолетики'],
        'run_work_programs':["запусти project для работы", "программа для работы", "джарвис включи проги для работы", "джарвис открой проги для работы", 'джарвис открывай проги для работы','заводим мотор',"для работы",'нужны программы для','скоро работа запускай программу','запускай праги до работы', 'запускай праге', 'запускай проги для работы', 'запусти проги для работы', 'проги для работы', 'запуск прог для работы', 'программы ребутика', 'программы для работы', 'запусти программы для работы', 'запусти проги для ребутики'],
        'run_youtube':["джарвис youtube", "джарвис открой youtube", "джарвис открой топчик", "джарвис запусти youtube", "youtube чик", "включай ютубчик", "запускай ютубчик", "давай включай youtube", "джарвис давай youtube","запусти youtube", "запусти ютубчик", "включи ютубчик", "открой youtube", "дождь заглянем", 'давай посмотрим на юту','давай что-то на ютуби посмотрим','давай посмотрим на','давай глянем в юту','давай посмотрим юту','включи youtube','давай смотреть youtube','давай что-то глянем','давай что-то посмотрим','давай что-то посмотрю','давай посмотрю youtube','давай глянем ютубчик','давай посмотрим youtube','давай глянем в youtube','давай играем в youtube','давай глянем youtube','запускай youtube','youtube','включай youtube','давай посмотрим ютубчик'],
        'jarvis_sleep':["джарвис спя", "java спящий", "джонни спящий режим", "джарвис спящий режим", "джарвис сонный режим","уходи в режим с", "джарвис со", "уходи в покой","отдыхай джарвис",  "засыпай джарвис", "джарвис уходи в по", "засыпай","джарвис переходи в по","уходи в покой",  "отдыхай джа", 'джарвис переходи в покой','джарвис режим покоя',"джарвис споки-ноки", 'джарвис засыпай','джарвис сон','джарвис режим сна','джарвис споки ноки','джарвис уходи в покой', 'джарвис отдыхай'],
        'jarvis_unsleep':['джарвис активный режим','джарвис pc памяти','джарвис просыпаемся','джарвис ты тут','джарвис ты мне нужен', "просыпаемся", 'пожалуйста мне нужен','джарвис просыпайся','джарвис вставай','джарвис пора просыпаться'],
        'jarvis_exit':["на сегодня всё", "молодец сегодня всё", "отлично молодец сегодня всё", "хорошо на сегодня всё","молодец джарвис сегодня всё", 'джарвис сегодня всё молодец','на сегодня всё джарвис','джарвис на сегодня всё','джарвис сегодня всё','джарвис пока','джарвис выключение','джарвис выключайся','джарвис пора выключаться'],
        'check_notes':["покажи заметки моей джарвис","подскажи мои заметки", "какие у меня есть дела", "расскажи мои дела", "джарвис заметки", "расскажи замет", "расскажи заметки", "какие заметки","покажи заметки", "ну-ка покажи заметки", "посмотри заметки","какие есть за", "подскажи заметки", "какие есть заметки", "проверь заметки", "давай проверим за", "напомни мои дела", "что нового в за", "напомни заметки","какие последние заметки"],
        'make_notes':["джарвис добавь заметку", "давай добавим за","добавь ещё заметку", "добавь ещё одну заметку", "давай ещё заметку", "давай добавим замет", "давай добавим заметку", "давай сделаем заметку", "новая заметка","добавь новое дело", "добавь новую заметку", "добавь заметку", "запиши в заметки", "сделай заметку", "добавь ко мне в", "добавь ко мне в заметки"],
        'delete_notes':["джарвис удали заметку", "давай удалим заметку", "удалить заметку", "надо удалить за", "надо удалить заметку", "удали заметку", "надо убрать заметку", "убери заметку", "удаляем за", "удаляем заметку","вычеркнуть заметку", "вычеркнуть дело", "убрать одно дело", "удалить дело"],
        'make_search':["джарвис запрос", "джаред запрос", "джарвис помоги мне", "джаред найди для меня", "джарвис запрос", "джарвис найди для меня кое-что", "джарвис помоги мне кое-что", "джарвис есть вопрос", "есть вопрос джарвис", "загуглить на меня кое-что", "найди для меня кое", "поиск в гугле", "поиск", "запрос", "найди кое-что", "найди для меня кое-что", "есть вопрос", "задам вопрос", "джарвис вопрос", "джарвис загугли каи", "джарвис загугли каи", "джарвис загугли каи", "джарвис найди для меня", "джарвис вопрос", "джарвис поиск", "джарвис ищи"],
        'window_control':["джарвис с управлением окнами", "управлять окнами", "управление", "джарвис управление ок", "управление ок", "управление окнами", "джарвис управление окнами", "режим управления окнами", "джарвис режим управления", "джарвис управлять окнами", "управлять окном"],
        'fast_commands':['джарвис','эй джарвис','алло джарвис', 'джарвис есть работа', 'джарвис есть задание']
    }
}

def say(t):
    text = t

    with BytesIO() as f:
        gTTS(text=text, lang='ru', slow=False).write_to_fp(f)
        f.seek(0)
        data, fs = sf.read(f)
        sd.play(data, fs, blocking=True)

def fast_commands():
    say('Да?')
    while True:
        query = listen_command()
        print(query)
        if query in commands_back:
            say('Хорошо, возвращаюсь назад!')
            return
        elif query in 'Не совсем поняла, повтори ещё раз':
            pass
        else:
            w_info = query.split(' ')
            if len(w_info) < 2:
                say('Повтори ')
                break
            else:
                w_name = ''
                w_command = ''
                for w in w_info:
                    if w.strip() == 'youtube' or w.strip() == 'ютубчик':
                        w_name = 'youtube'
                    if w.strip() == 'телеграм' or w.strip() == 'телегу' or w.strip() == 'telegram':
                        w_name = 'telegram'
                    if w.strip() == 'обсидиан' or w.strip() == 'obsidian' or w.strip() == 'обси':
                        w_name = 'obsidian'
                    if w.strip() == 'steam' or w.strip() == 'стим' or w.strip() == 'стимчик':
                        w_name = 'steam'
                    if w.strip() == 'google' or w.strip() == 'chrome' or w.strip() == 'гугл' or w.strip() == 'хром':
                        w_name = 'chrome'
                    if w.strip() == 'открой' or w.strip() == 'заупусти':
                        w_command = 'open'
                    if w.strip() == 'паузы' or w.strip() == 'пауза' or w.strip() == 'паузу' or w.strip() == 'стоп' or w.strip() == 'останови' or w.strip() == 'запаузи' or w.strip() == 'продолжение' or w.strip() == 'продолжай' or w.strip() == 'воспроизведение':
                        w_command = 'pause'
                    if w.strip() == 'полный' or w.strip() == 'полноэкранный' or w.strip() == 'полную' or w.strip() == 'разверни' or w.strip() == 'сверни' or w.strip() == 'уменьши' or w.strip() == 'увеличь':
                        w_command = 'minimize/maximize'

                path_to_programs = 'C:/Users/79782/Desktop/jarvis/PROGRAMS'
                chrome_path = os.path.join(path_to_programs, 'chrome.lnk')
                if w_name != '' and w_command != '':
                    if w_name == 'youtube':
                        if w_command == 'open':
                            youtube_file = os.path.join(path_to_programs, 'youtube.lnk')
                            os.startfile(chrome_path)
                            os.startfile(youtube_file)
                            say('Готово')
                            break
                        elif w_command == 'pause':
                            rez = change_all_youtube('space')
                            if rez:
                                say('Сделанно')
                                break
                            else:
                                say('У тебя нету окон с youtube')
                                break
                        elif w_command == 'minimize/maximize':
                            rez = change_all_youtube('f')
                            if rez:
                                say('Сделанно')
                                break
                            else:
                                say('У тебя нету окон с youtube')
                                break
                        else:
                            say('Не умею')
                    else:
                        if w_command == 'open':
                            try:
                                window_to_open = w_name+'.lnk'
                                file_open = os.path.join(path_to_programs, window_to_open)
                                os.startfile(file_open)
                                say('Готово')
                                break
                            except:
                                say('Пока не умею такое открывать')
                        elif w_command == 'pause':
                            pass
                        elif w_command == 'minimize/maximize':
                            pass
                        else:
                            pass
                else:
                    say('Не поняла, повтори')


def find_youtube_windows():
    youtube_windows = []

    for window in gw.getAllWindows():
        if window.title and "youtube" in window.title.lower():
            youtube_windows.append(window)

    return youtube_windows

def change_all_youtube(com):
    youtube_windows = find_youtube_windows()

    if not youtube_windows:
        return False

    for window in youtube_windows:
        try:
            window.activate()
            pyautogui.press(com)
        except Exception as e:
            try:
                w_h = window.width / 2
                h_h = window.height / 2
                x = window.left + w_h  # Кликнем не на самом краю
                y = window.top + h_h
                original_pos = pyautogui.position()
                pyautogui.click(x, y)
                time.sleep(0.1)
                pyautogui.moveTo(original_pos)
                pyautogui.press(com)
            except:
                pyautogui.press(com)

    return True

def window_control():
    say('Включен режим управления окнами')
    while True:
        query = listen_command()
        if query in commands_back:
            say('Хорошо, возвращаюсь назад!')
            return
        elif query in 'Не совсем поняла, повтори ещё раз':
            pass
        else:
            w_info = query.split(' ')
            if len(w_info) < 2:
                say('Не поняла, повтори ')
                break
            else:
                w_name = ''
                w_command = ''
                for w in w_info:
                    if w.strip() == 'youtube' or w.strip() == 'ютубчик':
                        w_name = 'youtube'
                    if w.strip() == 'паузу' or w.strip() == 'пауза' or w.strip() == 'стоп' or w.strip() == 'останови' or w.strip() == 'запаузи' or w.strip() == 'продолжение' or w.strip() == 'продолжай' or w.strip() == 'воспроизведение':
                        w_command = 'stop/play'
                    if w.strip() == 'полный' or w.strip() == 'полноэкранный' or w.strip() == 'полную' or w.strip() == 'разверни' or w.strip() == 'сверни' or w.strip() == 'уменьши' or w.strip() == 'увеличь':
                        w_command = 'minimize/maximize'

                if w_name != '' and w_command != '':
                    if w_name == 'youtube' and w_command == 'stop/play':
                        rez = change_all_youtube('space')
                        if rez:
                            say('Сделанно')
                            break
                        else:
                            say('У тебя нету окон с youtube')
                            break
                    elif w_name == 'youtube' and w_command == 'minimize/maximize':
                        rez = change_all_youtube('f')
                        if rez:
                            say('Сделанно')
                            break
                        else:
                            say('У тебя нету окон с youtube')
                            break
                    else:
                        say('Не нашла у нас такой команды, скажи ещё раз')
                else:
                    say('Не совсем поняла, повтори')


def make_search():
    phrases_search = ('Что для тебя найти?', 'С чем нужна помощь?', 'Какой у тебя вопрос?', 'что для тебя найти?', 'Что тебе подсказать?', 'С чем тебе помочь сегодня?', 'Что тебе подсказать?')
    say(random.choice(phrases_search))
    query = listen_command()
    if query in commands_back:
        say('Хорошо, возвращаюсь назад!')
        return
    elif query in 'Не совсем поняла, повтори ещё раз':
        pass
    else:
        webbrowser.open(f"https://www.google.com/search?q={query.replace(' ', '+')}")
        phrases_answer = ('Интересно вот что я нашла','Хорошо есть кое что','Вот, нашла для тебя','Хорошо, вот что нашлось','Да, нашла для тебя кое что','Вот что я для тебя откопала','Есть кое что по этому запросу','Вот что мне удалось найти')
        say(random.choice(phrases_answer))

def check_notes():
    say('Хорошо, вот твои последние заметки:')
    with open('notes.txt', 'r') as f:
        lines = f.readlines()
        for line in reversed(lines):
            say(line.strip())
    say('Это все дела которые у нас записаны')


def make_notes():
    phrases_make_notes = ('Что добавляем?','Какая новая заметка?','Что добавить в список дел?','Что нового добавить','Что будем добавлять?')
    say(random.choice(phrases_make_notes))
    while True:
        query = listen_command()
        print(f'"{query}", ')
        if query in commands_back:
            say('Хорошо, отменяю')
            break
        elif query in 'Не совсем поняла, повтори ещё раз':
            pass
        else:
            with open('notes.txt', 'a') as file:
                file.write(f'{query}\n')
            say(f'Задача: {query}, добавлена в список дел')
            break

def delete_notes():
    phrases_delete_notes = ('Что удаляем?','Какую заметку удалить?','Что удалить?','Что удаляем из списка дел','Что будем удалять?')
    say(random.choice(phrases_delete_notes))
    while True:
        query = listen_command()
        print(f'"{query}", ')
        if query in commands_back:
            say('Хорошо, отменяю')
            break
        elif query in 'Не совсем поняла, повтори ещё раз':
            pass
        else:
            check_corect_note = False
            with open('notes.txt', 'r') as f:
                lines = f.readlines()
                for line in reversed(lines):
                    if query in line.strip():
                        check_corect_note = True
                        break
            if check_corect_note:
                source_file = 'notes.txt'
                temp_file = 'notes_temp.txt'
                line_to_delete = query

                with open(source_file, 'r') as f_read, open(temp_file, 'w') as f_write:
                    for line in f_read:
                        if line.strip() != line_to_delete:
                            f_write.write(line)

                os.remove(source_file)
                os.rename(temp_file, source_file)
                say(f'Задача: {query}, удаленна из списка дел')
                break
            else:
                say('Не нашла такой, повтори ещё раз')

def jarvis_sleep():
    global jarvis_status
    phrase_to_sleep = ('Перехожу в состояние покоя. Если я понадоблюсь просто скажи: джарвис вставай', 'Хорошо! я буду отдыхать. Если я понадоблюсь просто скажи: эй джарвис', 'Хорошо я ухожу в режим сна. Ты можешь разбудить меня фразой: алло джарвис', 'Режим сна активирован. Если нужно вернуть меня в активный режим то скажи: джарвис активный режим', 'Хорошо, я буду рядом если понадоблюсь')
    say(random.choice(phrase_to_sleep))
    jarvis_status = 1

def jarvis_unsleep():
    global jarvis_status
    phrases_to_unsleep = ('Перехожу в активное состояние. Если надо перевести меня в состояние покоя скажи: джарвис засыпай', 'Я снова с тобой, чтобы меня выключить скажи: джарвис уходи в покой', 'Как приятно снова помогать тебе, что мне сделать?', 'Привет, я вышла из небытия! Да, Да, Я!', 'Включено активное состояние, для его отключения скажи: джарвис отдыхай')
    say(random.choice(phrases_to_unsleep))
    jarvis_status = 2

def jarvis_exit():
    global jarvis_status
    say('Хорошо, надеюсь я была сегодня полезной и помогла тебе!')
    jarvis_status = 0

def run_youtube():
    phrases_to_youtube = ('Что сегодня смотрим?','Что хочешь посмотреть?','Какое у тебя настроение? что хочешь посмотреть?','Что сегодня будем смотреть?')
    say(random.choice(phrases_to_youtube))
    youtubers = {
        'Штефанова':['стефаново','стефанов','можно ште','хочу стаханова','можно штефана','сегодня хочу политику','хочу политику','пальто хочу','хочу плиту','шпанов','давай плету','полёт давай','хочу шпа', 'стефанова','давай стефанова','стефано','штефанов','политоту','политику','штефанова','хочу штефанова','давай политоту','давай штефанова'],
        'Рындыча':['рингтон','давай рэнди','давай наверное рындыч','рынды','давай рындыч','рындыча','давай рындыча','рындыч'],
        'Айтипедию':['ну давай сегодня шевцова','давай википеди','может википедию','давай лёха','википедия','го лёха шев','давай шев','шевцов','айтипедия','лёху шевцова','давай шевцова','го лёху шевцова', 'шевцова'],
        'Новости баскетбола':['basket','хочу баскет сегодня','хочу глянуть баскет','захотелось баскет глянуть','хочу баскетбол','давай баск','что там в баскете','давай новости баскет','баскет сегодня','баск','баскетбол','новости баскет','новости баски','давай новости баскета','баскет','новости баскетбола','давай баскет','хочу баскет'],
        'Просто Ютуб':['просто','давай просто youtube','ну давай просто youtube гля','ну давай просто','открой просто youtube','youtube хочу','давай просто ют','может просто youtube','давай просто юту','просто youtube','давай просто ютубчик','youtube','хочу youtube','ютубчик','просто ютубчик'],
        'Команду Запрос': ['давай поиск',"найди видео по запросу", "давай по запросу", "запрос", "найди мне видео", "найди видео","видео по поиску", "найди по поиску", "ищи по поиску", "поиск" ]
    }
    youtuber = ''
    while True:
        query = listen_command()
        print(query)
        if query in commands_back:
            say('Хорошо, возвращаюсь назад!')
            return
        elif query in 'Не совсем поняла, повтори ещё раз':
            pass
        else:
            check_youtuber = False
            for k,v in youtubers.items():
                if query in v:
                    check_youtuber = True
                    youtuber = k
                    break

            if check_youtuber:
                break
            else:
                say(f'Не помню такого, может ты имел в виду {random.choice(list(youtubers.keys()))}')

    print(youtuber)
    path_to_youtube = 'C:/Users/79782/Desktop/jarvis/YOUTUBE'
    chrome_path = os.path.join(path_to_youtube, 'Chrome.lnk')
    if youtuber == 'Команду Запрос':
        say('Какое видео найти для тебя?')
        while True:
            query1 = listen_command()
            if query1 in commands_back:
                say('Хорошо, возвращаюсь назад!')
                return
            elif query1 in 'Не совсем поняла, повтори ещё раз':
                pass
            else:
                webbrowser.open(f"https://www.youtube.com/results?search_query={query1.replace(' ', '+')}")
                break
    else:
        os.startfile(chrome_path)
        if youtuber == 'Штефанова':
            youtube_file1 = os.path.join(path_to_youtube, 'youtube_shtefanov1.lnk')
            youtube_file2 = os.path.join(path_to_youtube, 'youtube_shtefanov2.lnk')
            youtube_file3 = os.path.join(path_to_youtube, 'youtube_shtefanov3.lnk')
            os.startfile(youtube_file1)
            os.startfile(youtube_file2)
            os.startfile(youtube_file3)
        if youtuber == 'Айтипедию':
            youtube_file1 = os.path.join(path_to_youtube, 'youtube_shevzov1.lnk')
            youtube_file2 = os.path.join(path_to_youtube, 'youtube_shevzov2.lnk')
            youtube_file3 = os.path.join(path_to_youtube, 'youtube_shevzov3.lnk')
            os.startfile(youtube_file1)
            os.startfile(youtube_file2)
            os.startfile(youtube_file3)
        if youtuber == 'Новости баскетбола':
            youtube_file1 = os.path.join(path_to_youtube, 'youtube_basket1.lnk')
            youtube_file2 = os.path.join(path_to_youtube, 'youtube_basket2.lnk')
            os.startfile(youtube_file1)
            os.startfile(youtube_file2)
        if youtuber == 'Рындыча':
            youtube_file1 = os.path.join(path_to_youtube, 'youtube_ryndich')
            os.startfile(youtube_file1)
        if youtuber == 'Просто Ютуб':
            youtube_file1 = os.path.join(path_to_youtube, 'youtube')
            os.startfile(youtube_file1)


    phrases_to_youtube2 = ('Отлично запускаю','Прекрасный выбор','Хорошо, давай смотреть','Интересно, уже запускаю')
    say(random.choice(phrases_to_youtube2))


def run_work_programs():
    phrases_to_work = ('Запускаю файлы для работы. Удачной работы Илюшка! Надеюсь сегодня ученики будут не так сильно тупить', 'Уже запускаю, желаю тебе удачи на работе сегодня', 'Запускаю. Желаю тебе удачи на работе Илюшка!', 'Они уже запускаются. Надеюсь сегодня работа будет лёгкой!')
    path_to_work = 'C:/Users/79782/Desktop/jarvis/WORK'
    path_to_work_site = 'C:/Users/79782/Desktop/jarvis/WORK/reb'
    rebotica_path = os.path.join(path_to_work_site, 'Rebotica.lnk')
    files = os.listdir(path_to_work)
    os.startfile(rebotica_path)
    for file in files:
        cur_file = os.path.join(path_to_work,file)
        if os.path.isfile(cur_file):
            os.startfile(cur_file)
        else:
            files_work = os.listdir(path_to_work_site)
            for file_w in files_work:
                cur_file_w = os.path.join(path_to_work_site, file_w)
                if os.path.isfile(cur_file_w):
                    os.startfile(cur_file_w)
    say(random.choice(phrases_to_work))

def repeat_mode_on():
    global repeat_after_me
    tt = ''
    if repeat_after_me:
        tt = 'Режим повторения уже Активирован. Чтобы его выключить скажи: хватит повторять'
    else:
        tt = 'Активирован режим повторения'
        repeat_after_me = True
    say(tt)


def repeat_mode_off():
    global repeat_after_me
    tt = ''
    if not repeat_after_me:
        tt = 'Режим повторения сейчас Отключен. Чтобы его активировать скажи: повтори за мной'
    else:
        tt = 'Режим повторения выключен'
        repeat_after_me = False
    say(tt)

def greetings():
    greets = ('Приветик я Джарвис, я личный помощник Илюши, чем могу помочь', 'Привет, я помощница Илюши, меня зовут Джарвис', 'Привет я Джарвис, как тебе помочь', 'Приветик, чем тебе может помочь ассистентка Илюши', 'Вам привет от Илюши, чем вам помочь', 'Привет я Джарвис, как я могу быть полезна')
    say(random.choice(greets))


def listen_command():
    try:
        with speech_recognition.Microphone() as mic:
            sr.adjust_for_ambient_noise(source=mic, duration=0.5)
            audio = sr.listen(source=mic)
            query = sr.recognize_google(audio_data=audio, language='ru-RU').lower()
        return query
    except speech_recognition.UnknownValueError:
        return 'Не совсем поняла, повтори ещё раз'

def main():
    query = listen_command()

    er = 'Не совсем поняла, повтори ещё раз'
    if query == er:
        pass
    else:
        if jarvis_status != 1:
            print(f'"{query}", ')
            for k,v in commands_dict['commands'].items():
                if query in v:
                    globals()[k]()
        else:
            if query in commands_dict['commands']['jarvis_unsleep']:
                jarvis_unsleep()

        if repeat_after_me:
            say(query)


    if jarvis_status == 0:
        return False
    else:
        return True

if __name__ == '__main__':
    while True:
        print('Это ассистент Джарвис созданый для того чтобы решать проблеммы Ильи')
        print('1. Включить ассистент    2. Выйти из программы')
        chs = input(' -> ')
        if chs == '1':
            jarvis_status = 2
            say('Привет! Это я твой личный ассистент Джарвис! чем могу быть полезна сегодня?')
            while True:
                if not main(): break
        elif chs == '2':
            print('Спасибо что пользовались моей программой ^_^!')
            break
        else:
            pass


