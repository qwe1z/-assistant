import json
import os
import webbrowser
from tkinter import *
from tkinter import scrolledtext

import pyaudio
from vosk import Model, KaldiRecognizer

model = Model('model-small')
rec = KaldiRecognizer(model, 16000)
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=16000,
                input=True,
                frames_per_buffer=8000)
stream.start_stream()


def listen():
    pass
    while True:
        data = stream.read(4000, exception_on_overflow=False)
        if (rec.AcceptWaveform(data)) and (len(data) > 0):
            answer = json.loads(rec.Result())
            if answer['text']:
                yield answer['text']


def number(a):
    words_to_numbers = {
        'один': 1,
        'одна': 1,
        'две': 2,
        'два': 2,
        'три': 3,
        'четыре': 4,
        'пять': 5,
        'шесть': 6,
        'семь': 7,
        'восемь': 8,
        'девять': 9,
        'десять': 10,
        'одиннадцать': 11,
        'двенадцать': 12,
        'тринадцать': 13,
        'четырнадцать': 14,
        'пятнадцать': 15,
        'шестнадцать': 16,
        'семнадцать': 17,
        'восемнадцать': 18,
        'девятнадцать': 19,
        'двадцать': 20,
        'тридцать': 30,
        'сорок': 40,
        'пятьдесят': 50,
        'шестьдесят': 60,
        'семьдесят': 70,
        'восемьдесят': 80,
        'девяносто': 90,
        'сто': 100,
        'двести': 200,
        'триста': 300,
        'четыреста': 400,
        'пятьсот': 500,
        'шестьсот': 600,
        'семьсот': 700,
        'восемьсот': 800,
        'девятьсот': 900,
    }

    x = a.split()
    number = 0
    final_number = 0
    for i in range(len(x)):
        if (x[i] == 'миллион') or (x[i] == 'миллиона') or (x[i] == 'миллионов'):
            if number == 0:
                final_number += 1000000
            number *= 1000000
            final_number += number
            number = 0

        elif (x[i] == 'тысяча') or (x[i] == 'тысячи') or (x[i] == 'тысяч'):
            if number == 0:
                final_number += 1000
            number *= 1000
            final_number += number
            number = 0
        else:
            number += words_to_numbers[x[i]]

    final_number += number
    return final_number


def volume(str):
    for text in listen():
        str = str.split()
        volume_1 = number(str[len(str) - 1])
        if ('увеличь' in text) or ('увеличить' in text):
            os.system('setvol +{}'.format(volume_1))
        elif ('уменьши' in text) or ('уменьшить' in text):
            os.system('setvol -{}'.format(volume_1))
        return 'громкость измена'


def plus(str):
    words = str.split()
    x1 = ''
    x2 = ''
    flag = 0
    for i in range(len(words)):
        if words[i] == 'плюс':
            flag = 1
        elif flag != 1:
            if x1 == '':
                x1 += words[i]
            else:
                x1 += ' ' + words[i]
        else:
            if x2 == '':
                x2 += words[i]
            else:
                x2 += ' ' + words[i]
    return number(x1) + number(x2)


def start():
    for text in listen():
        print(text)
        if ((text == "открой диспетчер задач")
                or (text == "диспетчер задач")
                or (text == "открой пожалуйста диспетчер задач")
                or (text == "открой диспетчер задач пожалуйста")
                or (text == "диспетчер задач открой")):
            os.system('taskmgr')

        elif ((text == "найди в интернете")
              or (text == "открой в интернете")
              or (text == "открой пожалуйста панель управления")):
            webbrowser.open_new_tab(text[18:])

        elif ((text == "открой панель управления")
              or (text == "открой панель управления")
              or (text == "открой пожалуйста панель управления")
              or (text == "открой панель управления пожалуйста")
              or (text == "панель управления")):
            os.system('control')

        elif "плюс" in text:
            print(plus(text))

        elif ((text == "открой файл хвост")
              or (text == "открой хвост файл")
              or (text == "открой пожалуйста файл хвост")
              or (text == "открой хвост файл пожалуйста")
              or (text == "файл хвост")):
            os.system('notepad.exe C:\Windows\System32\drivers\etc\hosts')

        elif ((text == "выход")
              or (text == "закройся")
              or (text == "выключись")
              or (text == "выключайся")):
            exit()

        elif "громкость" in text:
            print(volume(text))


tk = Tk()
tk.title(u"Асистент")
tk.resizable(False, False)

w = tk.winfo_screenwidth()
h = tk.winfo_screenheight()
w = w // 2  # середина экрана
h = h // 2
w = w - 200  # смещение от середины
h = h - 200
tk.geometry(f'300x400+{w}+{h}')


def info():
    window = Tk()
    msg = Message(window, text='''
    Асиситент способен.
    1.Открыть диспетчера задач.
    2.Открыть Панели управления.
    3.Искать в интернете.
    4.Закрытие голосового ассистента.
    5.Открыть файл hosts в блокноте.
    6.Уменьшить/Увеличить громкость на N
    7.Сложить два чисел
    ''')
    msg.pack()


Button(tk, text='Info', command=info).pack()

txt = scrolledtext.ScrolledText(tk, width=35, height=15, bg="gray46")
txt.pack()

canvas = Canvas(tk, width=300, height=400, bg="gray46", highlightthickness=0)
canvas.pack()
button = PhotoImage(file="C:/Users/Lol22/PycharmProjects/Assistant/picture/micro2.png")
button = button.subsample(8, 8)
Button(tk, command=start, image=button, highlightthickness=0, bg="gray56").place(x=125, y=280)

tk.mainloop()
