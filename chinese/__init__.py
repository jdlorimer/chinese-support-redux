# -*- coding: utf-8 ; mode: python -*-
# © 2012: Roland Sieker <ospalh@gmail.com>
# © 2012: Thomas Tempé <thomas.tempe@alysse.org>
#
# License: GNU AGPL, version 3 or later; http://www.gnu.org/copyleft/agpl.html

#from pinyin import Pinyinizer, is_han_character, on_focus_lost

#This should stay written exactly this way, and keep the same parenthesis
#format, as it is parsed by a very simple regexp to check for next
#release info from github, in config.py
__version__ = """0.8.0"""
release_info = """<ul>
<li><b>Improved local dictionaries</b>: no need to download them separately, hanzi in definition have tone colors, corrected Mornir's bug.</li>
<li><b>Improved pinyin transcription</b>: now using cidian-based transcription on sentences too, even when using an on-line dictionary.</li>
<li><b>Improved editor display</b>: now showing colors while editing notes.</li>
<li><b>Added Taiwan pronunciation</b>; removed Wade-Giles and Yale transcriptions, retaining limited support for Cantonese-Yale.</li>
<li><b>Improved model</b>: classifier and alternate spelling now appear in their own fields (if you create them). Added optional ruby and silhouette fields support.</li>
<li><b>Major code cleanup</b>, reducing download size by 25% and removing multiple external dependencies.</li>
<li><b>Some bugs fixed</b> (many thanks to Christian and Lili for reporting)</li></ul>
"""
