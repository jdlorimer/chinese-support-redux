# Copyright © 2012-2014 Thomas TEMPÉ <thomas.tempe@alysse.org>
# Copyright © 2017-2018 Joseph Lorimer <joseph@lorimer.me>
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
        db_path = join(dirname(realpath(__file__)), 'db', 'chinese.db')
        self.conn = connect(db_path)
        self.c = self.conn.cursor()

    def create_indices(self):
        self.c.execute(
            'CREATE INDEX IF NOT EXISTS isimplified ON cidian (simplified)')
        self.c.execute(
            'CREATE UNIQUE INDEX IF NOT EXISTS itraditional ON cidian '
            '(traditional, pinyin)')
        self.conn.commit()

    def _get_char_pinyin(self, c):
        """returns the pinyin transcription of a given Hanzi from Unihan.
        If it's not in the dictionary, return the original text.

        If there are multiple possibilities, returns one at random.
        """
        self.c.execute("select kMandarin from hanzi where cp = ?;", (c,) )
        try:
            (pinyin,) = self.c.fetchone()
            return pinyin
        except:
            return None

    def _get_word_pinyin(self, w, taiwan=False, ignoreVariants=True):
        """Returns the pinyin transcription of a word, from CEDICT.
        If it's not in the dictionary, returns None.
        If there are multiple possibilities, returns one at random.

        if taiwan==True then prefer Taiwan variant
        """
        selectStatement = "select pinyin, pinyin_taiwan from cidian where (traditional=? or simplified=?) "
        if ignoreVariants:
            selectStatement += "and ((english not like '%variant%' or english is null) " \
                               "and (german not like '%variante%' or german is null) " \
                               "and (french not like '%variante%' or french is null) " \
                               "and (spanish not like '%variante%' or spanish is null)); "

        self.c.execute(selectStatement, (w, w))
        try:
            pinyin, taiwan_pinyin = self.c.fetchone()
            if taiwan and taiwan_pinyin is not None:
                return taiwan_pinyin
            elif pinyin is not None:
                return pinyin
            elif ignoreVariants:
                return _get_word_pinyin(self, w, taiwan, False)
        except:
            #Not in dictionary
            return None

    def get_pinyin(self, w, taiwan=False, wl=4):
        """Returns the full pinyin transcription of a string.
        Use CEDICT wherever possible. Use Unihan to fill in.

        if taiwan==True then prefer Taiwan variant
        """

        p = self._get_word_pinyin(w, taiwan)
        if p:
            return p #one word, in dictionary
        if len(w)==1:
            return self._get_char_pinyin(w) #single character

        #We're looking up a string that's not in the dictionary
        #We'll try each 4-character sequence in turn, then 3-sequence, then 2-sequence and if those fails, do unit lookup.
        #transcription = u""
        transcription = u""
        w = w[:]
        last_was_pinyin = False
        while len(w)>0:
            word_was_found = False
            word_len = wl

            while word_len > 1:
                p = self._get_word_pinyin(w[:word_len], taiwan)
                if p:
                    transcription = add_with_space(transcription, p)
                    w = w[word_len:]
                    last_was_pinyin = True
                    word_was_found = True
                    break
                word_len -= 1

            if word_was_found == False:
                p = self._get_char_pinyin(w[0])
                if p:
                    transcription = add_with_space(transcription, p)
                    last_was_pinyin = True
                else:
                    #add character directly.
                    #Pad with spaces appropriately
                    if last_was_pinyin:
                        transcription+=" "
                    transcription+=w[0]
                    last_was_pinyin = False
                w = w[1:]
        return transcription

    def get_cantonese(self, w, only_one=True):
        """Returns a character-by-character cantonese transcription."""
        t = u""
        for c in w:
            self.c.execute("select kCantonese from hanzi where cp = ?;", (c,) )
            try:
                (k,) = self.c.fetchone()
                if only_one:
                    k = k.split(" ")[0]
                else:
                    k = k.replace(" ", "|")
                t = add_with_space(t, k)
            except:
                t+=c
        return t

    def _get_char_traditional(self, c):
        """Uses Unihan to find a traditional variant"""
        self.c.execute("select kTraditionalVariant from hanzi where cp = ?;", (c,) )
        try:
            (k,) = self.c.fetchone()
            return k
        except:
            return None

    def _get_word_traditional(self, w):
        """Uses CEDICT to find a traditional variant"""
        self.c.execute("select traditional from cidian where traditional=? or simplified=?;", (w, w) )
        try:
            (k,) = self.c.fetchone()
            return k
        except:
            return None

    def get_traditional(self, w, wl=4):
        """Returns the full traditional form of a string.
        Use CEDICT wherever possible. Use Unihan to fill in.
        """

        p = self._get_word_traditional(w)
        if p:
            return p #one word, in dictionary
        if len(w)==1:
            return self._get_char_traditional(w) #single character

        #We're looking up a string that's not in the dictionary
        #We'll try each 4-character sequence in turn, then 3-sequence, then 2-sequence and if those fails, do unit lookup.
        traditional = u""
        w = w[:]
        while len(w)>0:
            word_was_found = False
            word_len = wl

            while word_len > 1:
                p = self._get_word_traditional(w[:word_len])
                if p:
                    traditional += p
                    w = w[word_len:]
                    word_was_found = True
                    break
                word_len -= 1

            if word_was_found == False:
                p = self._get_char_traditional(w[0])
                if p:
                    traditional += p
                else:
                    #add character directly.
                    traditional+=w[0]
                w = w[1:]

        return traditional

    def _get_char_simplified(self, c):
        """Uses Unihan to find a simplified variant"""
        self.c.execute("select kSimplifiedVariant from hanzi where cp = ?;", (c,) )
        try:
            (k,) = self.c.fetchone()
            return k
        except:
            return None

    def _get_word_simplified(self, w):
        """Uses CEDICT to find a traditional variant"""
        self.c.execute("select simplified from cidian where traditional=? or simplified=?;", (w, w) )
        try:
            (k,) = self.c.fetchone()
            return k
        except:
            return None

    def get_simplified(self, w, wl=4):
        """Returns the full traditional form of a string.
        Use CEDICT wherever possible. Use Unihan to fill in.
        """

        p = self._get_word_simplified(w)
        if p:
            return p #one word, in dictionary
        if len(w)==1:
            return self._get_char_simplified(w) #single character

        #We're looking up a string that's not in the dictionary
        #We'll try each 4-character sequence in turn, then 3-sequence, then 2-sequence and if those fails, do unit lookup.
        simplified = u""
        w = w[:]
        while len(w)>0:
            word_was_found = False
            word_len = wl

            while word_len > 1:
                p = self._get_word_simplified(w[:word_len])
                if p:
                    simplified += p
                    w = w[word_len:]
                    word_was_found = True
                    break
                word_len -= 1

            if word_was_found == False:
                p = self._get_char_simplified(w[0])
                if p:
                    simplified += p
                else:
                    #add character directly.
                    simplified+=w[0]
                w = w[1:]

        return simplified

    def get_definitions(self, w, lang):
        '''Returns all definitions for a given language.
        Lang should be one of en, de, fr, es.

        returns a list of
        each one in the format (pinyin, definition, classifier, alt_spelling)
        '''
        langs = {"en":"english", "de":"german", "fr":"french", "es":"spanish"}
        self.c.execute("select distinct pinyin, %s as definition, classifiers, alternates from cidian where (traditional=? or simplified=?) and length(definition)>0 order by pinyin;" % langs[lang], (w, w))
        try:
            return self.c.fetchall()
        except:
            return []

    def get_classifiers(self, word):
        if not word:
            return []
        self.c.execute(
            ('SELECT DISTINCT classifiers FROM cidian '
             'WHERE (traditional = :word or simplified = :word)'),
            {'word': word}
        )
        cs = list(filter(None, [c for (c,) in self.c.fetchall()]))
        return ','.join(cs).split(',') if cs else []

    def get_alt_spellings(self, word):
        self.c.execute(
            ('SELECT DISTINCT alternates FROM cidian '
             'WHERE (traditional = :word or simplified = :word);'),
            {'word': word}
        )
        alts = list(filter(None, [a for (a,) in self.c.fetchall()]))
        return ','.join(alts).split(',') if alts else []
