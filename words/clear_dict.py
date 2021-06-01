import lib.models.word2vec as wv
m = wv.Word2vec()

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

del_counter = 0
includes = 0
vocab_set = set(m.vocab)
for f in files:
    with open('words/dict/' +f[0]) as ff:
        res = set()
        for el in ff.read().split('\n'):
            if el in vocab_set:
                res.add(el)
                includes += 1
            else:
                del_counter += 1
    with open('words/clear_dict/' + f[0], 'w') as fff:
        for r in res:
            fff.write(r+'\n')