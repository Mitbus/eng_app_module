from .models.word2vec import Word2vec
from .models.translate import Translator
from .Unit import Unit, UnitWord as UWord
from json import (
    loads as jloads,
    dumps as jdumps
)
from sqlite3 import connect
from typing import List
from random import (
    randint,
    shuffle,
    sample
)
from heapq import nlargest


class Db:
    def __init__(self, filename='users_statistic.db'):
        self.__conn__ = connect(filename)
        self.__cursor__ = self.__conn__.cursor()
        self.c = self.__cursor__
        self.__translator__ = Translator()
        self.__w2v_model__ = Word2vec()
        self.__vocab_dict__ = {
            w: i
            for i, w in enumerate(self.__w2v_model__.vocab)
        }

    def __del__(self):
        if hasattr(self, '__conn__'):
            self.__conn__.close()

    def init_db(self):
        self.__define_tables__()
        self.__init_word_table__()

    def __define_tables__(self):
        self.__cursor__.execute(
            '''
            CREATE TABLE IF NOT EXISTS user (
                id UNSIGNED INTEGER PRIMARY KEY NOT NULL,
                last_unit_id UNSIGNED SMALLINT NOT NULL,
                lesson TEXT,
                difficult UNSIGNED SMALLINT
            );
            ''')
        self.__cursor__.execute(
            '''
            CREATE TABLE IF NOT EXISTS known_words (
                user_id UNSIGNED INTEGER NOT NULL,
                word_id UNSIGNED MEDIUMINT NOT NULL,
                value TINYINT NOT NULL CHECK(value IN (0, 1)),
                PRIMARY KEY (user_id, word_id)
            );
            ''')
        self.__cursor__.execute(
            '''
            CREATE TABLE IF NOT EXISTS interesting_words (
                user_id UNSIGNED INTEGER NOT NULL,
                word_id UNSIGNED MEDIUMINT NOT NULL,
                value TINYINT NOT NULL CHECK(value IN (0, 1)),
                PRIMARY KEY (user_id, word_id)
            );
            ''')
        self.__cursor__.execute(
            '''
            CREATE TABLE IF NOT EXISTS units (
                user_id UNSIGNED INTEGER NOT NULL,
                unit_id UNSIGNED SMALLINT NOT NULL,
                words_list text,
                PRIMARY KEY (user_id, unit_id)
            );
            ''')
        self.__cursor__.execute(
            '''
            CREATE TABLE IF NOT EXISTS words (
                value TEXT NOT NULL,
                id UNSIGNED MEDIUMINT PRIMARY KEY NOT NULL
            );
            ''')
    
    def __init_word_table__(self):
        self.__cursor__.executemany(
            '''
            INSERT INTO words VALUES (?, ?)
            ''',
            list(self.__vocab_dict__.items())
        )
    
    def change_diff(self, user_id: int, diff: int) -> None:
        if type(user_id) != int or type(user_id) != int:
            raise TypeError('Invalid parameter type')
        if diff < 1 or diff > 100:
            raise ValueError('The correct value for the "diff" parameter must be between 1 and 100')
        self.__cursor__.execute(
            f'''
            UPDATE user
            SET difficult = ?
            WHERE id = ?
            ''',
            [diff, user_id]
        )
        self.__get_lesson_forward__(user_id)  # Пересчитываем урок с учетом измененной сложности

    def create_user(self, id: int, unit: Unit) -> None:
        '''
        Перед регистрацией пользователя в базе должен быть проведен пробный урок,
        результаты которого уже записаны в бд
        '''
        if type(id) != int or type(unit) != Unit:
            raise TypeError('Invalid parameter type')
        self.__cursor__.execute(
            '''
            INSERT INTO user VALUES (?, 0, NULL, 10)
            ''',
            [id]
        )
        self.add_unit(id, unit)
        self.__total_users__ += 1

    def __update_known_words__(self, user_id: int, word: str, status: bool) -> None:
       self.__update_words__(user_id, word, status, 'known_words')

    def __update_interesting_words__(self, user_id: int, word: str, status: bool) -> None:
       self.__update_words__(user_id, word, status, 'interesting_words')

    def __update_words__(self, user_id: int, word: str, status: bool, table_name: str) -> None:
        if word not in self.__vocab_dict__:
            raise ValueError(f'Udefined word {word}')
        self.__cursor__.execute(
            f'''
            SELECT value FROM {table_name}
            WHERE user_id = ? AND word_id = ?
            ''',
            [user_id, self.__vocab_dict__[word]]
        )
        value = self.__cursor__.fetchall()
        if len(value) == 0:
            self.__cursor__.execute(
                f'''
                INSERT INTO {table_name} VALUES (?, ?, ?)
                ''',
                [user_id, self.__vocab_dict__[word], status]
            )
        elif value[0] != status:
            self.__cursor__.execute(
                f'''
                UPDATE {table_name}
                SET value = ?
                WHERE user_id = ? AND word_id = ?
                ''',
                [status, user_id, self.__vocab_dict__[word]]
            )

    def __user_list__(self) -> List[int]:
        self.__cursor__.execute(
            '''
            SELECT id FROM user
            '''
        )
        return list(map(lambda x: x[0], self.__cursor__.fetchall()))

    @property
    def __total_users__(self):
        if not hasattr(self, '__prop_total_users__'):
            self.__prop_total_users__ = len(self.__user_list__())
        return self.__prop_total_users__

    @__total_users__.setter
    def __total_users__(self, value):
        self.__prop_total_users__ = value

    def get_recomendation(self, user_id: int, max_users: int, min_accuracy: int):
        '''
        Подбирает рекомендации на основе интересов пользователей, которые наиболее похожи на данного
        Значение схожести и количество похожих пользователей подбирается эмпириеским путем (default: n=1, min_accuracy=0.1)
        Данные рекомендации полезны, если пользователь хочет "попробовать что-то новое". Мы можем делать такие выводы исходя из того, что пользователь
        начал редко пользоваться приложением или ставить плохие оценки изученным словам
        '''
        if type(user_id) != int or type(max_users) != int or type(min_accuracy) != float:
            raise TypeError('Invalid parameter type')
        if max_users <= 0:
            raise ValueError('Invalid max_users parameter value')
        if min_accuracy < 0 or min_accuracy > 1:
            raise ValueError('Invalid min_accuracy parameter value')
        most_similar = self.__get_most_similar__(user_id, n=max_users)
        most_similar_ids = list(map(lambda x: x[1], filter(lambda x: x[0] >= min_accuracy, most_similar)))
        if len(most_similar_ids) == 0:
            raise RuntimeError('There is no similar users')
        in_format = ('?, ' * len(most_similar_ids))[:-2]
        self.__cursor__.execute(
            f'''
            SELECT word_id FROM interesting_words
            WHERE 
                word_id NOT IN (
                    SELECT word_id FROM interesting_words
                    WHERE user_id = ?
                )
                AND value = 1
                AND user_id IN ({in_format})
            ''', [user_id, *most_similar_ids]
        )
        res = self.__cursor__.fetchall()
        res = list(
            map(
                lambda x: [x, self.__translator__.translate_en_ru(x)], 
                map(
                    lambda x: self.__w2v_model__.vocab[x[0]].replace('_', ' '), 
                    res)))
        if len(res) == 0:
            raise RuntimeError('There is no new words from other users')  # Нет слов других пользователей, которыми бы не увлекался данный пользователь
        size = self.__get_difficult__(user_id)
        if len(res) <= size:
            shuffle(res)
            return res
        return sample(res, k=size)

    def __get_most_similar__(self, user_id: int, n=1):
        '''
        Проводит сравнительный анализ веторов,
        возвращает пару (accuracy, индекс) n наиболее похожих по интересам (interesting_words) пользователей.
        Если значение n больше, чем кол-во пользователей, то выдает ошибку
        '''
        if self.__total_users__ - 1 < n:
            raise ValueError('Not enough users in database')
        self.__cursor__.execute(
            '''
            SELECT word_id, value FROM interesting_words
            WHERE user_id = ?
            ''', [user_id]
        )
        target = self.__cursor__.fetchall()
        target_len = len(target)
        target = dict(target)
        best_n = []
        for other_id in self.__user_list__():
            if other_id == user_id:
                continue
            self.__cursor__.execute(
                '''
                SELECT word_id, value FROM interesting_words
                WHERE user_id = ?
                ''', [other_id]
            )
            other = dict(self.__cursor__.fetchall())
            both_values = 0  # Количество совпадений в interesting_words
            same_interesting = 0  # Количество общих интересов (совпадает и ключ и значение)
            for el in target:
                if el in other:
                    both_values += 1
                    if target[el] == other[el]:
                        same_interesting += 1
            accuracy = same_interesting / (len(other) + target_len - both_values)  # фактически, accuracy совпадает с мерой Жаккара
            best_n.append((accuracy, other_id))
        return nlargest(n, best_n)

    def get_lesson(self, user_id: int):
        if type(user_id) != int:
            raise TypeError('Invalid parameter type')
        self.__cursor__.execute(
            '''
            SELECT lesson FROM user
            WHERE id = ?
            ''', [user_id]
        )
        res = self.__cursor__.fetchall()
        if res == []:
            raise ValueError('User with user_id = {user_id} doesn\'t exists')
        lesson = res[0][0]
        return jloads(lesson)

    def add_unit(self, user_id: int, unit: Unit) -> None:
        if type(user_id) != int or type(unit) != Unit:
            raise TypeError('Invalid parameter type')
        for uw in unit:
            if uw.word not in self.__vocab_dict__:
                raise ValueError(f'Word "{uw.word}" doesn\'t contains in vocab')
        self.__cursor__.execute(
            '''
            SELECT last_unit_id FROM user
            WHERE id = ?
            ''',
            [user_id]
        )
        cur_unit_id = self.__cursor__.fetchall()[0][0] + 1
        for uw in unit:
            self.__update_known_words__(user_id, uw.word, uw.known)
            self.__update_interesting_words__(user_id, uw.word, uw.interesting)
        words_ids = [self.__vocab_dict__[uw.word] for uw in unit]
        self.__cursor__.execute(
            '''
            INSERT INTO units VALUES (?, ?, ?)
            ''',
            [user_id, cur_unit_id, jdumps(words_ids)]
        )
        self.__cursor__.execute(
            '''
            UPDATE user
            SET last_unit_id = ?
            WHERE id = ?
            ''',
            [cur_unit_id, user_id]
        )
        # Добавление нового занятия наперед
        lesson = self.__get_lesson_forward__(user_id)
        self.__cursor__.execute(
            '''
            UPDATE user
            SET lesson = ?
            WHERE id = ?
            ''',
            [jdumps(lesson), user_id]
        )

    def __get_last_unit_words__(self, user_id: int) -> List[int]:
        self.__cursor__.execute(
            '''
            SELECT last_unit_id FROM user
            WHERE id = ?
            ''',
            [user_id]
        )
        unit_id = self.__cursor__.fetchall()[0][0]
        self.__cursor__.execute(
            '''
            SELECT words_list FROM units
            WHERE user_id = ? AND unit_id = ?
            ''', [user_id, unit_id]
        )
        words = self.__cursor__.fetchall()[0][0]
        return jloads(words)

    def __get_difficult__(self, user_id: int):
        self.__cursor__.execute(
            '''
            SELECT difficult FROM user
            WHERE id = ?
            ''', [user_id]
        )
        return self.__cursor__.fetchall()[0][0]

    def __is_word_known__(self, user_id: int, word_id: int) -> int:
        '''
        Если значения нет в таблице, то будет возвращено None
        '''
        self.__cursor__.execute(
            '''
            SELECT value FROM known_words
            WHERE user_id = ? AND word_id = ?
            ''', [user_id, word_id]
        )
        res = self.__cursor__.fetchall()
        if len(res) == 0:
            return None
        return res[0][0]

    def __is_word_interesting__(self, user_id: int, word_id: int) -> int:
        '''
        Если значения нет в таблице, то будет возвращено None
        '''
        self.__cursor__.execute(
            '''
            SELECT value FROM interesting_words
            WHERE user_id = ? AND word_id = ?
            ''', [user_id, word_id]
        )
        res = self.__cursor__.fetchall()
        if len(res) == 0:
            return None
        return res[0][0]

    def __get_lesson_forward__(self, user_id: int):
        '''
        Вычисляется наперед, после каждого add_unit
        Генерирует список английских слов, которые попадут в урок
        '''
        if type(user_id) != int:
            raise TypeError('Invalid parameter type')
        words = self.__get_last_unit_words__(user_id)
        if len(words) == 0:
            raise ValueError('User with user_id = {user_id} doesn\'t exists')
        in_format = ('?, ' * len(words))[:-2]
        self.__cursor__.execute(
            f'''
            SELECT word_id, value FROM interesting_words
            WHERE user_id = ? AND word_id IN ({in_format})
            ''', [user_id, *words]
        )
        interesting_words = set(
            map(
                lambda w: self.__w2v_model__.vocab[w[0]] , 
                filter(
                    lambda w: w[1] == 1, 
                    self.__cursor__.fetchall())))
        size = self.__get_difficult__(user_id)
        gen = []
        for w in map(lambda i: self.__w2v_model__.vocab[i], words):
            if w in interesting_words:
                gen.append(self.__w2v_model__.predict_by_word(w))
        # Выбираем лучшие слова из случайных итераторов, они попадают в ответ
        res = []
        while True:
            if len(gen) == 0 or size == 0:
                break
            idx = randint(0, len(gen) - 1)
            res_i = next(gen[idx], None)
            if res_i is None:
                gen.pop(idx)
                continue
            if res_i not in self.__vocab_dict__:
                continue
            res_i_id = self.__vocab_dict__[res_i]
            # Двойное отрицание при проверке поскольку нельзя быть увереным насчет интереса к новому слову
            if self.__is_word_interesting__(user_id, res_i_id) != 0 and self.__is_word_known__(user_id, res_i_id) != 1:
                res_i_repl = res_i.replace('_', ' ')
                # check if res_i not in res
                res_i_not_in_res = True
                for r in res:
                    if r[0] == res_i_repl:
                        res_i_not_in_res = False
                if res_i_not_in_res:
                    size -= 1
                    res.append([res_i_repl, self.__translator__.translate_en_ru(res_i_repl)])
        return res
