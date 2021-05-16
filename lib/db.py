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
        self.w2v_model = Word2vec()
        self.translator = Translator()
        self.vocab_dict = {
            w: i
            for i, w in enumerate(self.w2v_model.vocab)
        }
        self.conn = connect(filename)
        self.cursor = self.conn.cursor()

    def __del__(self):
        if hasattr(self, 'conn'):
            self.conn.close()

    def init_db(self):
        self.__define_tables__()
        self.__init_word_table__()

    def __define_tables__(self):
        # TODO: добавить в отчет сравнение векторного хранения и хранения с индексами. В среднем юзер изнает 1к-5к слов (3000*(32+32+1)), а в аблице 250к (250000*1+32)слов
        self.cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS user (
                id UNSIGNED INTEGER PRIMARY KEY NOT NULL,
                last_unit_id UNSIGNED SMALLINT NOT NULL,
                lesson TEXT,
                difficult UNSIGNED SMALLINT
            );
            ''')
        self.cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS known_words (
                user_id UNSIGNED INTEGER NOT NULL,
                word_id UNSIGNED MEDIUMINT NOT NULL,
                value TINYINT NOT NULL CHECK(value IN (0, 1)),
                PRIMARY KEY (user_id, word_id)
            );
            ''')
        self.cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS interesting_words (
                user_id UNSIGNED INTEGER NOT NULL,
                word_id UNSIGNED MEDIUMINT NOT NULL,
                value TINYINT NOT NULL CHECK(value IN (0, 1)),
                PRIMARY KEY (user_id, word_id)
            );
            ''')
        self.cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS units (
                user_id UNSIGNED INTEGER NOT NULL,
                unit_id UNSIGNED SMALLINT NOT NULL,
                words_list text,
                PRIMARY KEY (user_id, unit_id)
            );
            ''')
        self.cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS words (
                value TEXT NOT NULL,
                id UNSIGNED MEDIUMINT PRIMARY KEY NOT NULL
            );
            ''')
    
    def __init_word_table__(self):
        self.cursor.executemany(
            '''
            INSERT INTO words VALUES (?, ?)
            ''',
            list(self.vocab_dict.items())
        )
    
    def change_diff(self, user_id: int, diff: int) -> None:
        if type(user_id) != int or type(user_id) != int:
            raise 'Invalid type'
        self.cursor.execute(
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
            raise 'Invalid type'
        self.cursor.execute(
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
        if word not in self.vocab_dict:
            raise f'Udefined word {word}'
        self.cursor.execute(
            f'''
            SELECT value FROM {table_name}
            WHERE user_id = ? AND word_id = ?
            ''',
            [user_id, self.vocab_dict[word]]
        )
        value = self.cursor.fetchall()
        if len(value) == 0:
            self.cursor.execute(
                f'''
                INSERT INTO {table_name} VALUES (?, ?, ?)
                ''',
                [user_id, self.vocab_dict[word], status]
            )
        elif value[0] != status:
            self.cursor.execute(
                f'''
                UPDATE {table_name}
                SET value = ?
                WHERE user_id = ? AND word_id = ?
                ''',
                [status, user_id, self.vocab_dict[word]]
            )

    def __user_list__(self) -> List[int]:
        self.cursor.execute(
            '''
            SELECT id FROM user
            '''
        )
        return list(map(lambda x: x[0], self.cursor.fetchall()))

    @property
    def __total_users__(self):
        if not hasattr(self, '___total_users__'):
            self.___total_users__ = len(self.__user_list__())
        return self.___total_users__

    @__total_users__.setter
    def __total_users__(self, value):
        self.___total_users__ = value

    def get_recomendation(self, user_id: int, max_users: int, min_accuracy: int):
        '''
        Подбирает рекомендации на основе интересов пользователей, которые наиболее похожи на данного
        Значение схожести и количество похожих пользователей подбирается эмпириеским путем (default: n=1, min_accuracy=0.1)
        Данные рекомендации полезны, если пользователь хочет "попробовать что-то новое". Мы можем делать такие выводы исходя из того, что пользователь
        начал редко пользоваться приложением или ставить плохие оценки изученным словам
        '''
        if type(user_id) != int or type(max_users) != int or type(min_accuracy) != float:
            raise 'Invalid type'
        if max_users <= 0 or min_accuracy < 0 or min_accuracy > 1:
            raise 'Invalid parameter value'
        most_similar = self.__get_most_similar__(user_id, n=max_users)
        most_similar_ids = list(map(lambda x: x[1], filter(lambda x: x[0] >= min_accuracy, most_similar)))
        if len(most_similar_ids) == 0:
            raise 'There is no similar users'
        in_format = ('?, ' * len(most_similar_ids))[:-2]
        self.cursor.execute(
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
        res = self.cursor.fetchall()
        res = list(
            map(
                lambda x: [x, self.translator.translate_en_ru(x)], 
                map(
                    lambda x: self.w2v_model.vocab[x[0]], 
                    res)))
        if len(res) == 0:
            raise 'There is no new words from other users'  # Нет слов других пользователей, которыми бы не увлекался данный пользователь
        size = self.__get_difficult__(user_id)
        if len(res) <= size:
            shuffle(res)
            return res
        return sample(res, k=size)

    def __get_most_similar__(self, user_id: int, n=1):
        '''
        Проводит сравнительный анализ веторов,
        возвращает пару (accuracy, индекс) n наиболее похожих по интересам (interesting_words) пользователей.
        Если значение n больше, чемм кол-во пользователей, то выдает ошибку
        '''
        if self.__total_users__ - 1 < n:
            raise 'Not enough users in database'
        self.cursor.execute(
            '''
            SELECT word_id, value FROM interesting_words
            WHERE user_id = ?
            ''', [user_id]
        )
        target = self.cursor.fetchall()
        target_len = len(target)
        target = dict(target)
        best_n = []
        for other_id in self.__user_list__():
            if other_id == user_id:
                continue
            self.cursor.execute(
                '''
                SELECT word_id, value FROM interesting_words
                WHERE user_id = ?
                ''', [other_id]
            )
            other = dict(self.cursor.fetchall())
            both_values = 0  # Количество совпадений в interesting_words
            same_interesting = 0  # Количество общих интересов (совпадает и ключ и значение)
            for el in target:
                if el in other:
                    both_values += 1
                    if target[el] == other[el]:
                        same_interesting += 1
            accuracy = same_interesting / (len(other) + target_len - both_values)
            best_n.append((accuracy, other_id))
        return nlargest(n, best_n)

    def get_lesson(self, user_id: int):
        if type(user_id) != int:
            raise 'Invalid type'
        self.cursor.execute(
            '''
            SELECT lesson FROM user
            WHERE id = ?
            ''', [user_id]
        )
        lesson = self.cursor.fetchall()[0][0]
        return jloads(lesson)

    def add_unit(self, user_id: int, unit: Unit) -> None:
        if type(user_id) != int or type(unit) != Unit:
            raise 'Invalid type'
        for uw in unit:
            if uw.word not in self.vocab_dict:
                raise f'Word {uw.word} doesn\'t contains in vocab'
        self.cursor.execute(
            '''
            SELECT last_unit_id FROM user
            WHERE id = ?
            ''',
            [user_id]
        )
        cur_unit_id = self.cursor.fetchall()[0][0] + 1
        for uw in unit:
            self.__update_known_words__(user_id, uw.word, uw.known)
            self.__update_interesting_words__(user_id, uw.word, uw.interesting)
        words_ids = [self.vocab_dict[uw.word] for uw in unit]
        self.cursor.execute(
            '''
            INSERT INTO units VALUES (?, ?, ?)
            ''',
            [user_id, cur_unit_id, jdumps(words_ids)]
        )
        self.cursor.execute(
            '''
            UPDATE user
            SET last_unit_id = ?
            WHERE id = ?
            ''',
            [cur_unit_id, user_id]
        )
        # Добавление нового занятия наперед
        lesson = self.__get_lesson_forward__(user_id)
        self.cursor.execute(
            '''
            UPDATE user
            SET lesson = ?
            WHERE id = ?
            ''',
            [jdumps(lesson), user_id]
        )

    def __get_last_unit_words__(self, user_id: int) -> List[int]:
        self.cursor.execute(
            '''
            SELECT last_unit_id FROM user
            WHERE id = ?
            ''',
            [user_id]
        )
        unit_id = self.cursor.fetchall()[0][0]
        self.cursor.execute(
            '''
            SELECT words_list FROM units
            WHERE user_id = ? AND unit_id = ?
            ''', [user_id, unit_id]
        )
        words = self.cursor.fetchall()[0][0]
        return jloads(words)

    def __get_difficult__(self, user_id: int):
        self.cursor.execute(
            '''
            SELECT difficult FROM user
            WHERE id = ?
            ''', [user_id]
        )
        return self.cursor.fetchall()[0][0]

    def __is_word_known__(self, user_id: int, word_id: int) -> int:
        '''
        Если значения нет в таблице, то будет возвращено None
        '''
        self.cursor.execute(
            '''
            SELECT value FROM known_words
            WHERE user_id = ? AND word_id = ?
            ''', [user_id, word_id]
        )
        res = self.cursor.fetchall()
        if len(res) == 0:
            return None
        return res[0][0]

    def __is_word_interesting__(self, user_id: int, word_id: int) -> int:
        '''
        Если значения нет в таблице, то будет возвращено None
        '''
        self.cursor.execute(
            '''
            SELECT value FROM interesting_words
            WHERE user_id = ? AND word_id = ?
            ''', [user_id, word_id]
        )
        res = self.cursor.fetchall()
        if len(res) == 0:
            return None
        return res[0][0]

    def __get_lesson_forward__(self, user_id: int):
        '''
        Вычисляется наперед, после каждого add_unit
        Генерирует список английских слов, которые попадут в урок
        '''
        if type(user_id) != int:
            raise f'Unexpected user_id type. Expected {int} but got {type(user_id)}'
        words = self.__get_last_unit_words__(user_id)
        if len(words) == 0:
            raise 'Error'
        in_format = ('?, ' * len(words))[:-2]
        self.cursor.execute(
            f'''
            SELECT word_id, value FROM interesting_words
            WHERE user_id = ? AND word_id IN ({in_format})
            ''', [user_id, *words]
        )
        interesting_words = set(
            map(
                lambda w: self.w2v_model.vocab[w[0]] , 
                filter(
                    lambda w: w[1] == 1, 
                    self.cursor.fetchall())))
        size = self.__get_difficult__(user_id)
        gen = []
        for w in map(lambda i: self.w2v_model.vocab[i], words):
            if w in interesting_words:
                gen.append(self.w2v_model.predict_by_word(w))
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
            ru = self.translator.translate_en_ru(res_i)
            res_i_id = self.vocab_dict[res_i]
            # Двойное отрицание при проверке поскольку нельзя быть увереным насчет интереса к новому слову
            if self.__is_word_interesting__(user_id, res_i_id) != 0 and self.__is_word_known__(user_id, res_i_id) != 1 and (res_i, ru) not in res:
                size -= 1
                res.append([res_i, ru])
        return res
