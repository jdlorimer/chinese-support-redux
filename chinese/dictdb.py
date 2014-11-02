# -*- coding: utf-8 -*-
#
# Copyright © 2014 Thomas TEMPÉ, <thomas.tempe@alysse.org>
# 
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
#
#COPYRIGHT AND PERMISSION NOTICE

#Copyright © 1991-2012 Unicode, Inc. All rights reserved. Distributed under the Terms of Use in http://www.unicode.org/copyright.html.

#Permission is hereby granted, free of charge, to any person obtaining a copy of the Unicode data files and any associated documentation (the "Data Files") or Unicode software and any associated documentation (the "Software") to deal in the Data Files or Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, and/or sell copies of the Data Files or Software, and to permit persons to whom the Data Files or Software are furnished to do so, provided that (a) the above copyright notice(s) and this permission notice appear with all copies of the Data Files or Software, (b) both the above copyright notice(s) and this permission notice appear in associated documentation, and (c) there is clear notice in each modified Data File or in the Software as well as in the documentation associated with the Data File(s) or Software that the data or software has been modified.

#THE DATA FILES AND SOFTWARE ARE PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT OF THIRD PARTY RIGHTS. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR HOLDERS INCLUDED IN THIS NOTICE BE LIABLE FOR ANY CLAIM, OR ANY SPECIAL INDIRECT OR CONSEQUENTIAL DAMAGES, OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THE DATA FILES OR SOFTWARE.

#Except as contained in this notice, the name of a copyright holder shall not be used in advertising or otherwise to promote the sale, use or other dealings in these Data Files or Software without prior written authorization of the copyright holder.


"""Interface to the db/chinese_dict.sql SQLite database containing the local dictionaries

Available dictionaries:
* Chinese characters (Unihan)
* Chinese words (CEDICT), including:
  * simplified and traditional spellings
  * pinyin and Taiwan variant pronunciations
  * English, German and French translations


unihan table structure:
["cp", "kMandarin", "kCantonese", "kFrequency", "kHangul", "kJapaneseKun", "kSimplifiedVariant", "kTraditionalVariant", "Vietnamese"]

cidian table structure:
["traditional", "simplified", "pinyin", "pinyin_taiwan", "classifiers", "alternates", "english", "german", "french", "spanish"]

"""

import sqlite3
import os.path


class DictDB:
    conn = None
    c = None

    def __init__(self):
        try:
            from aqt import mw
            db_file = os.path.join(mw.pm.addonFolder(), "chinese", "db", "chinese_dict.sqlite")
        except: #Used for local debugging
            db_file = "db/chinese_dict.sqlite"

        self.conn=sqlite3.connect(db_file)
        self.c = self.conn.cursor()

        #Create the DB indexes. 
        #Only works the first time.
        #These indexes are removed from the distribution files, in order to save space
        try:
            self.c.execute("create index isimplified on cidian ( simplified );")
            self.c.execute("create unique index itraditional on cidian ( traditional, pinyin );")
            self.conn.commit()
        except:
            pass


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
    
    def _get_word_pinyin(self, w, taiwan=False):
        """Returns the pinyin transcription of a word, from CEDICT.
        If it's not in the dictionary, returns None.
        If there are multiple possibilities, returns one at random.

        if taiwan==True then prefer Taiwan variant
        """

        self.c.execute("select pinyin, pinyin_taiwan from cidian where traditional=? or simplified=?;", (w, w))
        try:
            pinyin, taiwan_pinyin = self.c.fetchone()
            if taiwan and taiwan_pinyin is not None:  
                return taiwan_pinyin
            else:
                return pinyin
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

    def get_classifiers(self, txt):
        r = []
        self.c.execute("select distinct classifiers from cidian where (traditional=? or simplified=?);", (txt, txt))
        try:
            #fetchall returns a list of tuples, converts to a list of strings
            return filter(lambda a:a, map(lambda a:a[0], self.c.fetchall()))
        except:
            return []

    def get_alt_spellings(self, txt):
        self.c.execute("select distinct alternates from cidian where (traditional=? or simplified=?);", (txt, txt))
        try:
            #fetchall returns a list of tuples, converts to a list of strings
            return filter(lambda a:a, map(lambda a:a[0], self.c.fetchall()))
        except:
            return []
        


def add_with_space(a, b):
    if len(a)>0 and " " != a[-1]:
        return a+" "+b
    return a+b

