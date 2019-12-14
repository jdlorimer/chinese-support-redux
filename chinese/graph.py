# Copyright 2013 Thomas TEMPÉ <thomas.tempe@alysse.org>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html

'''
This module draws two stats graphs in Anki's "stats" window, showing the
progress made on Chinese individual characters, and on Anki notes
containing Chinese characters, over time.

Here is what it counts:
* Only looks at the 1st field. Ignores all other fields.
* Selects chinese characters from the Unicode 4e00-9fff range.
This includes all Hanzi, but not Chinese punctuation.
It's also the same range used for Japanese Kanji.
* Only cards classified as young or mature are counted.
Learning mode or suspended cards are ignored.
* Suspended or deleted cards are not counted at all in the history,
even if they have been practiced in the past. This means the graph can
never show a decrease in your vocabulary.
* No distinction is made on note types. All notes are counted, either
from the whole collection, or from the active deck, depending on your
selection (bottom of the window).
'''

import re
import time

from anki.lang import _

now = time.mktime(time.localtime())


def addchars(chars, txt, date):
    "List each chinese character, with its earliest study date"
    try:
        for c in txt:
            try:
                if re.match( "[\u3400-\u9fff]", c):
                    chars[c] = max(date, chars[c])
            except:
                chars[c]=date
    except:
        pass


def addword(words, txt, date):
    "List each card containing at least one chinese character"
    try:
        if re.match(".*[\u3400-\u9fff]", txt):
            words[txt] = date
    except:
        pass


def history(data, chunks=None, chunk_size=1):
    #Compute history
    if not chunks:
        try:
            chunks=max(data.values())//chunk_size+1 #nb of periods to look back
        except:
            chunks = 1 #This happens if the deck contains no Chinese
    histogram = [0]*(chunks+1)
    cumul=[]
    delta=[]
    subtotal=0
    date=-chunks
    #Fill histogram, as a list. d = nb of days in the past (0=today).
    for d in list(data.values()):
        if d <= chunks*chunk_size:
            histogram[d//chunk_size] += 1
        else:
            subtotal+=1
    #Fill history, as a list of coordinates: [(relative_day, nb_values),...]
    while len(histogram):
        v=histogram.pop()
        subtotal +=v
        cumul.append((date, subtotal))
        delta.append((date, v))
        date+=1
    return cumul, delta


def chineseGraphs(self, chunks, chunk_size, chunk_name):
    txt=""
    chars = {} #dictionary, in the form { "character":earliest review date, ...}
    notes = {} #dictionary, in the form { "word":earliest review date, ...}

    for first_field, first_study_date in self.col.db.execute("select notes.sfld, min(revlog.id)/1000 as date from notes, cards, revlog where notes.id=cards.nid and cards.id=revlog.cid and cards.queue>0 and cards.did in %s group by notes.id;" % self._limit() ):
        relative_time= int((now-first_study_date)/86400) #in days
        addchars(chars, first_field, relative_time)
        addword(notes, first_field, relative_time)

    #Characters graph
    char_cumul, char_delta = history(chars, chunks, chunk_size)
    txt += self._title(
        _("Chinese characters"),
        _("The number of Chinese characters you have acquired over time"))

    data = [
        dict(data=char_cumul, color=3, yaxis=1, bars={'show':False}, lines={"show":True}),
        dict(data=char_delta, color=2, yaxis=2, bars={'show': True}, stack=False)]
    txt += self._graph(id="chinese_chars", data=data,
                       ylabel = "New chars per "+chunk_name,
                       ylabel2=_("Total characters"),
                       conf=dict(
            xaxis=dict(tickDecimals=0), yaxes=[dict(
                    tickDecimals=0, position="right")]))
    txt += "<div>%d known characters</div>" %(len(chars))

    #Notes graph
    note_cumul, note_delta = history(notes, chunks, chunk_size)
    txt += self._title(
        _("Chinese Vocabulary"),
        _("The number of notes containing Chinese that you have acquired over time"))

    data = [
        dict(data=note_cumul, color=4, yaxis=1, bars={'show':False}, lines={"show":True}),
        dict(data=note_delta, color=1, yaxis=2, bars={'show': True}, stack=False)]
    txt += self._graph(id="chinese_notes", data=data,
                       ylabel = "New notes per "+chunk_name,
                       ylabel2=_("Total notes"),
                       conf=dict(
            xaxis=dict(tickDecimals=0), yaxes=[dict(
                    tickDecimals=0, position="right")]))
    txt += "<div>%d known notes</div>" %(len(notes))

    return txt


def todayStats(self, _old):
    if self.type == 0:
        chunks = 30
        chunk_size = 1
        chunk_name='day'
    elif self.type == 1:
        chunks = 52
        chunk_size = 7
        chunk_name='week'
    else:
        chunks = None
        chunk_size = 30
        chunk_name='month'
    text = _old(self)
    text += chineseGraphs(self, chunks, chunk_size, chunk_name)
    return text
