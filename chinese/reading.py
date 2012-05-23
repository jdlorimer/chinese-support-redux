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
pinynFields = ['Reading', 'Pinyin']
tonesFields = ['tones']

modelTag = 'chinese'

class Pinyin(Object):
    pass


# Focus lost hook
##########################################################################

def onFocusLost(flag, n, fidx):
    from aqt import mw
    src = None
    dst = None
    # japanese model?
    if modelTag not in n.model()['name'].lower():
        return flag
    # have hanzi, pinyin and readings fields?
    for c, name in enumerate(mw.col.models.fieldNames(n.model())):
        for f in srcFields:
            if name == f:
                src = f
                srcIdx = c
        for f in dstFields:
            if name == f:
                dst = f
    if not src or not dst:
        return flag
    # dst field already filled?
    if n[dst]:
        return flag
    # event coming from src field?
    if fidx != srcIdx:
        return flag
    # grab source text
    srcTxt = mw.col.media.strip(n[src])
    if not srcTxt:
        return flag
    # update field
    n[dst] = cjklib.reading(srcTxt)
    return True

# Init
##########################################################################

cjklib = CJKLib()

addHook('editFocusLost', onFocusLost)

# Tests
##########################################################################

if __name__ == "__main__":
    expr = u"カリン、自分でまいた種は自分で刈り取れ"
    print mecab.reading(expr).encode("utf-8")
    expr = u"昨日、林檎を2個買った。"
    print mecab.reading(expr).encode("utf-8")
    expr = u"真莉、大好きだよん＾＾"
    print mecab.reading(expr).encode("utf-8")
    expr = u"彼２０００万も使った。"
    print mecab.reading(expr).encode("utf-8")
    expr = u"彼二千三百六十円も使った。"
    print mecab.reading(expr).encode("utf-8")
    expr = u"千葉"
    print mecab.reading(expr).encode("utf-8")
