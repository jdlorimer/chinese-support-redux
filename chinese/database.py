# Copyright © 2012-2014 Thomas TEMPÉ <thomas.tempe@alysse.org>
# Copyright © 2017-2019 Joseph Lorimer <joseph@lorimer.me>
#
# This file is part of Chinese Support Redux.
#
# Chinese Support Redux is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# Chinese Support Redux is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along with
# Chinese Support Redux.  If not, see <https://www.gnu.org/licenses/>.

from os.path import dirname, join, realpath
from sqlite3 import connect

from .util import add_with_space


class Dictionary:
    def __init__(self):
        db_path = join(dirname(realpath(__file__)), 'data', 'db', 'chinese.db')
        self.conn = connect(db_path)
        self.c = self.conn.cursor()

    def create_indices(self):
        self.c.execute(
            'CREATE INDEX IF NOT EXISTS isimplified ON cidian (simplified)'
        )
        self.c.execute(
            'CREATE UNIQUE INDEX IF NOT EXISTS itraditional '
            'ON cidian (traditional, pinyin)'
        )
        self.conn.commit()

    def _get_word_pinyin(self, word, type_, prefer_tw=False, no_variants=True):
        from .transcribe import accentuate

        if type_ == 'trad':
            query = 'SELECT pinyin, pinyin_tw FROM cidian WHERE traditional=?'
        elif type_ == 'simp':
            query = 'SELECT pinyin, pinyin_tw FROM cidian WHERE simplified=?'
        else:
            raise ValueError(type_)

        if no_variants:
            query += """AND (english NOT LIKE '%variant%' OR english IS NULL)
                        AND (german NOT LIKE '%variant%' OR german IS NULL)
                        AND (french NOT LIKE '%variant%' OR french IS NULL)"""

        self.c.execute(query, (word,))
        res = self.c.fetchone()
        if not res:
            return None
        pinyin, pinyin_tw = res
        if prefer_tw and pinyin_tw:
            return ' '.join(
                accentuate(list(map(str.lower, pinyin_tw.split())), 'pinyin')
            )
        if pinyin:
            return ' '.join(
                accentuate(list(map(str.lower, pinyin.split())), 'pinyin')
            )
        if no_variants:
            s = self._get_word_pinyin(self, word, prefer_tw, False)
            return ' '.join(
                accentuate(list(map(str.lower, s.split())), 'pinyin')
            )

    def _get_word_jyutping(self, word, type_):
        if type_ == 'trad':
            query = 'SELECT jyutping FROM cidian WHERE traditional=?'
        elif type_ == 'simp':
            query = 'SELECT jyutping FROM cidian WHERE simplified=?'
        self.c.execute(query, (word,))
        res = self.c.fetchone()
        if not res:
            return None
        return res[0]

    def get_pinyin(self, word, type_, prefer_tw=False, word_len=4):
        p = self._get_word_pinyin(word, type_, prefer_tw)
        if p:
            return p
        if len(word) == 1:
            return self._get_char(word, 'pinyin')

        # Try each 4-character sequence in turn, then 3-sequence, then
        # 2-sequence and if those fails, do unit lookup.

        result = ''
        word = word[:]
        last_was_pinyin = False
        while len(word) > 0:
            word_was_found = False

            while word_len > 1:
                p = self._get_word_pinyin(word[:word_len], type_, prefer_tw)
                if p:
                    result = add_with_space(result, p)
                    word = word[word_len:]
                    last_was_pinyin = True
                    word_was_found = True
                    break
                word_len -= 1

            if not word_was_found:
                p = self._get_char(word[0], 'pinyin')
                if p:
                    result = add_with_space(result, p)
                    last_was_pinyin = True
                else:
                    if last_was_pinyin:
                        result += ' '
                    result += word[0]
                    last_was_pinyin = False
                word = word[1:]
        return result

    def get_cantonese(self, word, type_):
        return self._get_word_jyutping(word, type_)

    def get_traditional(self, word, word_len=4):
        return self.get_word(word, word_len, type_='trad')

    def get_simplified(self, word, word_len=4):
        return self.get_word(word, word_len, type_='simp')

    def get_word(self, word, word_len=4, type_='trad'):
        p = self._get_word(word, type_)
        if p:
            return p

        if len(word) == 1:
            return self._get_char(word, type_)

        # Try each 4-character sequence in turn, then 3-sequence, then
        # 2-sequence and if those fails, do unit lookup.

        result = ''
        word = word[:]
        while len(word) > 0:
            word_was_found = False

            while word_len > 1:
                p = self._get_word(word[:word_len], type_)
                if p:
                    result += p
                    word = word[word_len:]
                    word_was_found = True
                    break
                word_len -= 1

            if not word_was_found:
                p = self._get_char(word[0], type_)
                if p:
                    result += p
                else:
                    result += word[0]
                word = word[1:]

        return result

    def _get_char(self, c, type_):
        to_col = {
            'trad': 'kTraditionalVariant',
            'simp': 'kSimplifiedVariant',
            'pinyin': 'kMandarin',
            'canto': 'kCantonese',
        }

        self.c.execute('SELECT %s FROM hanzi WHERE cp = ?' % to_col[type_], c)
        try:
            (k,) = self.c.fetchone()
            return k
        except:
            return None

    def _get_word(self, word, type_):
        to_col = {'trad': 'traditional', 'simp': 'simplified'}

        self.c.execute(
            'SELECT %s FROM cidian '
            'WHERE traditional = :word '
            'OR simplified = :word' % to_col[type_],
            {'word': word},
        )
        try:
            (k,) = self.c.fetchone()
            return k
        except:
            return None

    def get_definitions(self, word, lang):
        to_full = {'en': 'english', 'de': 'german', 'fr': 'french'}

        self.c.execute(
            'SELECT DISTINCT pinyin, %s AS definition, classifiers, variants '
            'FROM cidian '
            'WHERE (traditional = :word OR simplified = :word) '
            'AND LENGTH(definition) > 0 '
            'ORDER BY pinyin' % to_full[lang],
            {'word': word},
        )
        try:
            return self.c.fetchall()
        except:
            return []

    def get_classifiers(self, word):
        if not word:
            return []
        self.c.execute(
            (
                'SELECT DISTINCT classifiers FROM cidian '
                'WHERE (traditional = :word OR simplified = :word)'
            ),
            {'word': word},
        )
        cs = list(filter(None, [c for (c,) in self.c.fetchall()]))
        return ','.join(cs).split(',') if cs else []

    def get_variants(self, word):
        self.c.execute(
            (
                'SELECT DISTINCT variants FROM cidian '
                'WHERE (traditional = :word OR simplified = :word)'
            ),
            {'word': word},
        )
        vars = list(filter(None, [a for (a,) in self.c.fetchall()]))
        return ','.join(vars).split(',') if vars else []
