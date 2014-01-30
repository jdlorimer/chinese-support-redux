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


class ChineseDB:
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
            self.c.execute("create unique index itraditional on cidian ( traditional );")
            self.conn.commit()
        except:
            pass


    def _get_char_pinyin(self, c):
        """returns the pinyin transcription of a given Hanzi from Unihan.
        If it's not in the dictionary, return the original text"""
        self.c.execute("select kMandarin from hanzi where cp = ?;", (c,) )
        try:
            (pinyin,) = self.c.fetchone()
            return pinyin
        except:
            return c
        
    def _get_word_pinyin(self, w, taiwan=False):
        """Returns the pinyin transcription of a word, from CEDICT.
        If it's not in the dictionary, return None

        if taiwan==True then prefer Taiwan variant
        """

        self.c.execute("select pinyin, pinyin_taiwan from cidian where traditional=? or simplified=?;", (w, w))
        try:
            pinyin, taiwan_pinyin = self.c.fetchone()
            if taiwan and len(taiwan_pinyin):
                return taiwan_pinyin
            else:
                return pinyin
        except:
            return None

    def get_pinyin(self, w, taiwan=False):
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
        #We'll try each 2-character sequence in turn, and if it fails, do unit lookup.
        transcription = u""
        w = w[:]
        while len(w)>0:
            p = self._get_word_pinyin(w[:2], taiwan)
            if p:
                transcription+=p+" "
                w = w[2:]
            else:
                transcription+=self._get_char_pinyin(w[0])+" "
                w = w[1:]
        return transcription



db = ChineseDB()


print db._get_char_pinyin(u"了")
print db.get_pinyin(u"吃过了没有？")
