# Copyright: Damien Elmes <anki@ichi2.net>
# Copyright 2012, Thomas TEMPE <thomas.tempe@alysse.org>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
# Based off Kieran Clancy's initial implementation.

# These templates complement the ruby.py module, and provide
# chinese-specific services. They should be used on fields containing
# chinese characters, with transcription formatted as in 吗[ma3].


import re
#from anki.hooks import addHook
from anki import hooks
from anki.utils import stripHTML
#from anki.template.hint import hint
from anki.template import TemplateRenderContext
from .ruby import ruby_top, ruby_top_text, ruby_bottom_text, no_sound

r = r' ?([^ >]+?)\[(.+?)\]'
ruby_re = r'<ruby><rb>\1</rb><rt>\2</rt></ruby>'

tone_info= [
    [u'[ɑ̄āĀáɑ́ǎɑ̌ÁǍàɑ̀À]', 'a'],
    [u'[ēĒéÉěĚèÈ]', 'e'],
    [u'[īĪíÍǐǏìÌ]', 'i'],
    [u'[ōŌóÓǒǑòÒ]', 'o'],
    [u'[ūŪúÚǔǓùÙ]', 'u'],
    [u'[ǖǕǘǗǚǙǜǛ]', 'v']
]


#def transcription_no_tones(txt, *args):
def transcription_no_tones(
    txt: str, field_name: str, filter_name: str, context: TemplateRenderContext,
) -> str:
    if not filter_name.startswith("transcription_no_tones"):
        # not our filter, return string unchanged
        return txt
    '''Returns only the transcription, with tone information removed, whether
    it is in the form 'nǐ' or 'ni2'.
    '''
    txt = ruby_top_text(txt)
    for a, b in tone_info:
        txt = re.sub(a, b, txt)
    txt = re.sub(r'(\[\s*[a-z]+?)[0-9]', r'\1 ', txt, flags=re.IGNORECASE)
    txt = re.sub(r'¹²³⁴', r' ', txt)
    return txt


#def hanzi_silhouette(txt, *args):
def hanzi_silhouette(
    txt: str, field_name: str, filter_name: str, context: TemplateRenderContext,
) -> str:
    if not filter_name.startswith("hanzi_silhouette"):
        # not our filter, return string unchanged
        return txt
    ''' Hides the chinese characters, ruby annotations and tone colorization.
    Eg: '又[you4]A又B' returns '_ A _ B'.
    '''
    if len(txt)<10:
        return re.sub(u'[\u4e00-\u9fff]', '_ ', ruby_bottom_text(txt))
    else:
        return ""


#def hanzi_context(txt, extra, context, tag, fullname):
def hanzi_context(
    txt: str, field_name: str, filter_name: str, context: TemplateRenderContext,
) -> str:
    if not filter_name.startswith("hanzi_context"):
        # not our filter, return string unchanged
        return txt
    '''
    For use on a Hanzi field.
    Return a list of all the other Hanzi synonyms, with the common characters hidden,
    to allow the user to identify the correct hanzi from a note.
    '''
    other_hanzi = []
    for k, v in context.iteritems():
        if re.match(r'Hanzi.*', k, flags=re.IGNORECASE) and v != txt :
            other_hanzi += [k]
    if len(other_hanzi)<1:
        return ""
    other_hanzi.sort()
    other_hanzi_values = []
    for v in other_hanzi:
        value = stripHTML(re.sub(r, r'\1', no_sound(context[v])))
        if len(value)>0:
            other_hanzi_values += [value]
    if len(other_hanzi_values)<1:
        return ""
    def concat(a, b):
        return a + " / " + b
    context_string = reduce(concat, other_hanzi_values)
    for h in txt:
        if  h >= u'\u4e00' and h <= u'\u9fff':
            context_string = re.sub(h, " _ ", context_string)
    context_string = re.sub("  ", " ", context_string)
    return context_string


#legacy
def hint_filter(txt: str, args, context, tag: str, fullname) -> str:
    if not txt.strip():
        return ""
    # random id
    domid = "hint%d" % id(txt)
    return """
<a class=hint href="#"
onclick="this.style.display='none';document.getElementById('%s').style.display='block';return false;">
%s</a><div id="%s" class=hint style="display: none">%s</div>
""" % (
        domid,
        _("Show %s") % tag,
        domid,
        txt,
    )


#def hint_transcription(txt, extra, context, tag, fullname):
def hint_transcription(
    txt: str, field_name: str, filter_name: str, context: TemplateRenderContext,
) -> str:
    if not filter_name.startswith("hint_transcription") or filter_name.startswith("hint_transcription_no_tones"):
        # not our filter, return string unchanged
        return txt
    return hint_filter(ruby_top(txt), filter_name, context, 'Transcription', field_name)


#def hint_transcription_no_tones(txt, extra, context, tag, fullname):
def hint_transcription_no_tones(
    txt: str, field_name: str, filter_name: str, context: TemplateRenderContext,
) -> str:
    if not filter_name.startswith("hint_transcription_no_tones"):
        # not our filter, return string unchanged
        return txt
    return hint_filter(transcription_no_tones(txt), filter_name, context, 'Transcription', field_name)


def install():
    #addHook('fmod_transcription_no_tones', transcription_no_tones)
    #addHook('fmod_hanzi_silhouette', hanzi_silhouette)
    #addHook('fmod_hanzi_context', hanzi_context)
    #addHook('fmod_hint_transcription', hint_transcription)
    #addHook('fmod_hint_transcription_no_tones', hint_transcription_no_tones)
    hooks.field_filter.append(transcription_no_tones)
    hooks.field_filter.append(hanzi_silhouette)
    hooks.field_filter.append(hanzi_context)
    hooks.field_filter.append(hint_transcription)
    hooks.field_filter.append(hint_transcription_no_tones)
