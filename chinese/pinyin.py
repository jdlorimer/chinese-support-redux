# -*- coding: utf-8 -*-
#
# Copyricht © 2012 Roland Sieker, <ospalh@gmail.com>
# 
# Large portions of this file were originally written by
# Damien Elmes <anki@ichi2.net>
# and
#
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
#


from anki.utils import stripHTML, isWin, isMac
from anki.hooks import addHook

hanziFields = ['Chinese', 'Mandarin', 'Hanzi', u'汉字', u'漢字', 'Expression']
rubyFields = ['Reading', 'Ruby', 'Pinyin']
tonesFields = ['Tones']


modelName = 'chinese'
toneClasses =  {
    1 : 'tone1', 2 : 'tone2', 3 : 'tone3', 4 : 'tone4', 5 : 'tone5'
    }



def isHanCharacter(uchar):
    if uchar >= u'\u4e00' and uchar <= u'\u9fff':
        # The code from the JapaneseSupport plugin compares
        # ord(character) to a number. We compare one character with
        # another. Don't know which method is 'better'. (And we skip
        # u'\u2e00' to u'\u4dff', i guess the kana are somwhere in
        # there.)
        return True
    return False


def getHanCharacters(text):
    ret = u''
    # Maybe we got utf-8
    try:
        utext = unicode(text, 'utf-8')
    except TypeError:
        utext = text # Hope text is already unicode. If we put in
        # a number or something, we'll fail in one of the
        # next lines. EAFP
    for c in utext:
        if isHanCharacter(c):
            ret += c
    return ret

class Pinyinizer(object):
    
    def __init__(self):
        from cjklib import reading, characterlookup
        self.factory = reading.ReadingFactory()
        self.numOp = {'toneMarkType': 'numbers'}
        self.hanzilookup = characterlookup.CharacterLookup('C')

    def getPinyinData(self, hanzi):
        # There are fifty ways to^H^H for this to blow up.
        pinyin = self.hanzilookup.getReadingForCharacter(hanzi, 'Pinyin')[0]
        toneNumber = self._toneNumber(pinyin)
        ruby = u'{hanzi}[<span class="pinyin {tone}">{pinyin}</span>]'\
            .format(hanzi=hanzi, tone=toneClasses[toneNumber], pinyin=pinyin)
        return pinyin, ruby, toneNumber

    def _toneNumber(self, pinyin):
        # Another fifty ways to blow up.
        numberedPinyin = self.factory.convert(pinyin, 'Pinyin', 'Pinyin',\
                                                  targetOptions=self.numOp)
        return int(numberedPinyin[-1:])


pinyinize = Pinyinizer()

# Focus lost hook
##########################################################################

def onFocusLost(flag, n, fidx):
    from aqt import mw
    hanziField = None
    rubyField = None
    tonesField = None
    # japanese model?
    if modelName not in n.model()['name'].lower():
        return flag
    # Look for hanzi, ruby and tone fields.
    for c, name in enumerate(mw.col.models.fieldNames(n.model())):
        for f in hanziFields:
            if name == f:
                hanziField = f
                hanziIndex = c
        for f in rubyFields:
            if name == f:
                rubyField = f
        for f in tonesFields:
            if name == f:
                tonesField = f
    # We really want hanzi and ruby fields. (It’s OK if we have no
    # tones field.)
    if not hanziField or not rubyField:
        return flag
    # ruby field already filled?
    if n[rubyField]:
        return flag
    # event coming from hanzi field?
    if fidx != hanziIndex:
        return flag
    # grab hanzi
    hanzi = getHanCharacters(mw.col.media.strip(n[hanziField]))
    if not hanzi:
        return flag
    # update field
    ruby = u''
    tones = u''
    try:
        for h in hanzi:
            p, r, t = pinyinize.getPinyinData(h)
            ruby += r
            tones += unicode(t)
    except:
        return flag
    n[rubyField] = ruby
    # Check if we have a tones field
    if tonesField:
        # But clobber what is alread there
        n[tonesField] = tones
    return True


addHook('editFocusLost', onFocusLost)
