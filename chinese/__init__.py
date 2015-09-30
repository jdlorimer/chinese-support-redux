# -*- coding: utf-8 ; mode: python -*-
# © 2012: Roland Sieker <ospalh@gmail.com>
# © 2012: Thomas Tempé <thomas.tempe@alysse.org>
#
# License: GNU AGPL, version 3 or later; http://www.gnu.org/copyleft/agpl.html

#from pinyin import Pinyinizer, is_han_character, on_focus_lost

#This should stay written exactly this way, and keep the same parenthesis
#format, as it is parsed by a very simple regexp to check for next
#release info from github, in config.py
__version__ = """0.10.10"""
ankiweb_number = "3448800906"
release_info = """This version fixes Google TTS sound generation.<br>
Thanks to Glutaminate for providing the fix."""

prev = """<ul>
<li>Improved Taiwan Pinyin and Bopomofo transcription.</li>
<li>Added "Fill missing" features.</li>
<li>Added Cantonese speech</li>
</ul>
Many thanks to <b>Varbird</b> for these improvements!
<br><b>If you are studying Cantonese or Taiwan Pinyin:</b> please rename your <tt>Pinyin</tt> field to <tt>Reading</tt>. From now on, transcription choice only applies to the <tt>Reading</tt> field. <tt>Pinyin</tt> will always be treated as Pinyin. This change allows you have both Pinyin and Bopomofo in the same note.

<br><b>Note to advanced users:</b> This version includes a rewritten <tt>edit_behavior.py</tt> function. If you did some customizations, you can keep using your version, but the new "fill missing" features will not work.</b>
"""
