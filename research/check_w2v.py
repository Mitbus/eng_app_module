
files = [
('Американский сленг.txt', 1, 2),
('Английские идиомы с переводом и примерами.txt', 1, 3),
('Английские пословицы и поговорки.txt', 1, 2),
('Английские разговорные словосочетания и выражения.txt', 1, 2),
('Английский сленг.txt', 1, 2),
('Глаголы для описания приготовления пищи.txt', 1, 2),
('Лексика по теме Автомобиль.txt', 1, 3),
('Лексика по теме Анатомия.txt', 1, 3),
('Лексика по теме Археология.txt', 2, 3),
('Лексика по теме Архитектура.txt', 2, 3),
('Лексика по теме Аэропорт.txt', 1, 3),
('Лексика по теме Внешность.txt', 1, 3),
('Лексика по теме Выборы.txt', 1, 3),
('Лексика по теме Город.txt', 2, 3),
('Лексика по теме Гостиница.txt', 1, 2),
('Лексика по теме Грамматика.txt', 2, 2),
('Лексика по теме Деревья.txt', 2, 2),
('Лексика по теме Дом.txt', 1, 3),
('Лексика по теме Еда.txt', 2, 2),
('Лексика по теме Животные.txt', 1, 3),
('Лексика по теме Здоровье, части тела.txt', 2, 3),
('Лексика по теме Имущество.txt', 1, 2),
('Лексика по теме Искусство.txt', 1, 2),
('Лексика по теме Карты (игральные).txt', 1, 3),
('Лексика по теме Карьера.txt', 1, 2),
('Лексика по теме Кино.txt', 1, 2),
('Лексика по теме Компьютер.txt', 1, 2),
('Лексика по теме Кустарники.txt', 2, 2),
('Лексика по теме Магазины.txt', 2, 2),
('Лексика по теме Мебель.txt', 2, 2),
('Лексика по теме Медицина.txt', 1, 2),
('Лексика по теме Мобильный телефон.txt', 1, 2), ##
('Лексика по теме Музыка.txt', 1, 3),
('Лексика по теме Насекомые.txt', 2, 2),
('Лексика по теме Одежда.txt', 1, 3),
('Лексика по теме Олимпийские виды спорта.txt', 1, 3),
('Лексика по теме Профессии.txt', 1, 2),
('Лексика по теме Птицы.txt', 2, 3),
('Лексика по теме Путешествие.txt', 2, 2),
('Лексика по теме Рыбы.txt', 1, 2),
('Лексика по теме Семья и родственники.txt', 2, 3),
('Лексика по теме Спорт.txt', 1, 2),
('Лексика по теме Строительство.txt', 2, 2),
('Лексика по теме Футбол.txt', 2, 2),
('Лексика по теме Характер.txt', 2, 3),
('Лексика по теме Химия.txt', 2, 3),
('Лексика по теме Хобби.txt', 1, 2),
('Лексика по теме Хоккей.txt', 2, 2),
('Лексика по теме Художественные промыслы.txt', 2, 2),
('Лексика по теме Цвета.txt', 1, 3),
('Лексика по теме Шахматы.txt', 1, 3),
('Лексика по теме Экология.txt', 1, 2),
('Лексика по теме Экономика.txt', 2, 3)
]

import random
import lib
times = 100

d=lib.Db()
d.init_db()

acc = 0
total = 0
tp = fp = tn = fn = 0

for user_id in range(times):
    theme = random.randint(0, len(files)-1)
    total_words = set()
    theme_words = set()
    for i, f in enumerate(files):
        with open('words/clear_dict/' +f[0]) as ff:
            for el in ff.read().split('\n'):
                if theme == i:
                    theme_words.add(el)
                total_words.add(el)
    t = True
    f = False
    u = lib.unit(*(
            [(w, t, t) for w in random.sample(theme_words,len(theme_words) // 2) if w != ""] + \
            [(w, f, f) for w in random.sample(total_words,len(theme_words) // 4) if w != ""]
        )
    )
    try:
        # d.create_user(user_id + 1, u)
        d.add_unit(user_id + 1, u)
        less = d.get_lesson(user_id + 1)
    except Exception as e:
        print(e)
        continue
    t_tp = t_fp = t_tn = t_fn = 0
    for l in less:
        if l[0] not in total_words:
            continue
        if l[0] in theme_words:
            t_tp += 1
            acc += 1
        else:
            t_fp += 1
        total += 1
    t_fn = len(less) - t_tp - t_fp # тr
    t_tn = len(total_words) - len(theme_words) - t_fp
    tp += t_tp
    fp += t_fp
    tn += t_tn
    fn += t_fn

recall = tp / (tp + fn)
presision = tp / (tp + fp)

print(acc/total) # accuracy
print((recall * presision) / (recall + presision)) # f1

print(tp, fp) # conflusion matrix
print(fn, tn)
