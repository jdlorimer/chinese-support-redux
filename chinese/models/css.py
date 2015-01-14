# -*- coding: utf-8 -*-
#
# Copyright © 2012-2014 Thomas Tempe <thomas.tempe@alysse.org>
# Copyright © 2012 Roland Sieker <ospalh@gmail.com>

"""
CSS used by the different Chinese models.
"""

style = u'''\
.card { word-wrap: break-word; }
.win .chinese { font-family: "MS Mincho", "ＭＳ 明朝"; }
.mac .chinese { }
.linux .chinese { font-family: "Kochi Mincho", "東風明朝"; }
.mobile .chinese { font-family: "Hiragino Mincho ProN"; }
.chinese { font-size: 30px;}
.reading { font-size: 16px;}
.comment {font-size: 15px; color:grey;}
.tags {color:gray;text-align:right;font-size:10pt;}
.note {color:gray;font-size:12pt;margin-top:20pt;}
.hint {font-size:12pt;}
.answer { background-color:bisque; border:dotted;border-width:1px}

.tone1 {color: red;}
.tone2 {color: orange;}
.tone3 {color: green;}
.tone4 {color: blue;}
.tone5 {color: gray;}
'''
