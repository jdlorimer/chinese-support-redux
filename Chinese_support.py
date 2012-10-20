# -*- coding: utf-8 ; mode: python -*-

# Chinese support addon for Anki2
########################################################################
"""
A Plugin for the Anki2 Spaced Repition learning system,
<http://ankisrs.net/>

   Copyright © 2012 by Roland Sieker, <ospalh@gmail.com> 
   Copyright © 2012 by Thomas TEMPÉ, <thomas.tempe@alysse.org>

   Using parts of the Japanese plugin,
   written by Damien Elms.

   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

# WARNING
########################################################################
#
# This add-on is still in development. It's full of got missing
# features and bugs. Moreover, cards created with this version may
# stop working with the next release of this plug-in.
#
# You should not use it other than for testing.
# Please wait a few weeks before using Anki2 to learn Chinese.
# 

# Getting started
########################################################################
# 
# Run Anki2, then click on the "Add" button, to add a new word.
# 
# On the top of the "Add" window, click on the "Type" button, then on
# "Manage". Add a new node type based on model "Chinese word", select
# it for your new card, and validate.
# 
# In the "Add note" window, you should now see a list of fields that
# start with "Hanzi1", "Meaning"... You can now type Chinese
# characters in any of the "Hanzi" fields, and they should be
# converted automatically to ruby notation (eg: 你[).

# How to use
########################################################################
# 
# You can add main Hanzi word in the Hanzi1 field, and its translation in 
# the Meaning1 field. If you have comments (antonym, context) or pictures 
# that you wish to add to the note, it's best to put them in the "Notes 
# and pictures" field.
# 
# As you progress in Chinese, you will find many things have multiple
# names.  Chinese support helps you keep track of chinese words with
# multiple synonyms or alternate writing. You can add them in the
# "Hanzi2", "Hanzi3"... fields.
# 
# For example, if your note looks like this :
# Hanzi1 : 汉[han4]语[yu3]
# Hanzi2 : 中[zhong1]文[wen2]
# Hanzi3 : 中[zhong1]国[guo2]话[hua4]
# Meaning : Chinese language
# Notes and pictures : More general than 普同话 putong hua
# 
# Here, we recognize that the 3 Hanzi fields have the same meaning (or
# that, for now, you won't be bothering to learn their distinction).
# 
# Chinese support will generate 6 different cards (3 recall cards to
# train your active vocabulary, and three recognition cards to train
# your passive vocabulary and reading skill).


# Learning tips
###########################################################################
#
# Be careful when mixing synonyms in Chineses and your own
# language. You can only use "Meaning1" and "Meaning2" if all the
# hanzi have both meanings. There is no simple way to represent the
# complex relationships words have in different languages. Most of the
# time, it's better to just create two notes.
#
# Sometimes, you'll want to learn to produce just one word of a given
# note, but be able to recognize the other ones. In that case, it's
# best to suspend the corresponding cards from the "Browse" window.
#
# If you want pronounciation support, you should install the
# AwesomeTTS Anki add-on [work in progress!].
# 
# It's better to have very simple, short "meaning" fields, that you
# can relate to. More than a line, and you're sure to get lost.
#
# Until you know 500 or 1000 characters, it's a good idea to use Anki
# together with a notepad, and learn to write down each character from
# memory on each recall card. It takes more time, but the knowledge
# sinks in much faster, and you'll find yourself wasting less time on
# failed cards.
#
# It may be tempting to download a ready-made dictionary or deck, but
# it's much more efficient to input your own cards yourself, as you
# run into new words. If you're on a trip to China, write new words
# down on a notepad to input them into Anki later. Shared deck are a
# great feature to have, but they don't work that well for vocabulary
# acquisition.
#

# Upcoming changes
###########################################################################
#
# Here's what's coming. If you can program, you're welcome to join in
# on the development or add you own ideas.
# This plugin is hosted on http://github.com as chinese-support-addon,
# so it's easy to fork or modify.
#
# Automatic translation from Chinese to your own language
# Integration with AwesomeTTS for pronounciation support
# Chinese-specific statistics (in complement with the Hanzi Stats addon)
# Streamlined transition from Anki1.2

# Changelog
###########################################################################
#
# Version 0.1
# Initial design, with support for pinyin
# insertion, ruby notation and colorization.
#
# Version 0.2
# Added support for synonyms


# Start of configuration section
###########################################################################

# Chinese support addon configuration.

# Choose your language.
# Currently supported values : "cantonese" or "mandarin"

language = "mandarin"

# To avoid messing up anki 1 decks with similarly-named fields,
# restrict edition features only to notes whose name is listed below
# (exact match, case-sensitive)

# The beginning of the name of fields that contain Chinese characters.
# Those fields will be expanded to include transcription in ruby notation.
# Modify the list to adapt to an existing deck. (list of regexp)

possible_hanzi_field_names = [ u'Hanzi', u'汉字' ]

# The beginning of the name of fields that contain translation.
# The 1st of those will receive results from automatic translation.
# Modify the list to adapt to an existing deck. (list of regexp)

possible_meaning_field_names = [ u'Meaning' ]

# Enable automatic transaltion with Google Translate ?
# True : yes
# False : no translation

use_network_translation = False #this feature does not work yet

# Destination language
# The language to translate into.
# For more language codes, see below

translation_language='en'

# Afrikaans    = [af]  
# Albaniaan    = [sq]  
# Arabic       = [ar]  
# Belarusian   = [be]   
# Bulgarian    = [bg]  
# Catalan      = [ca]   
# Chinese Si=[zh -CN]  
# Chinese Tr=[zh -TW]  
# Czech        = [cs]  
# Danish       = [da]  
# Dutch        = [nl]  
# English      = [en]  
# Estonian     = [et]  
# Filipino     = [tl]  
# Finnish      = [fi]  
# French       = [fr]  
# Galician     = [gl]  
# German       = [de]  
# Greek        = [el]  
# Haitian C    = [ht]
# Hebrew       = [iw]
# Hindi        = [hi]
# Hungarian    = [hu]
# Icelandic    = [is]
# Indonesian   = [id]
# Irish        = [ga]
# Italian      = [it]
# Japanese     = [ja]
# Korean       = [ko]
# Latvian      = [lv]
# Lithuanian   = [lt]
# Macedonian   = [mk]
# Maltese      = [mt]
# Norwegian    = [no]
# Polish       = [pl]
# Portuguese   = [pt]
# Romanian     = [ro]
# Russian      = [ru]
# Serbian      = [sr]
# Slovak       = [sk]
# Slovenian    = [sl]
# Spanish      = [es]
# Swahili      = [sw]
# Swedish      = [sv]
# Thai         = [th]
# Thurkish     = [tr]
# Ukrainian    = [uk]
# Viatnamese   = [vi]
# Welsh        = [cy]
# Yiddish      = [yi]


# End of configuration section
###########################################################################


model_name_word = 'Chinese'
model_type_word = 'Chinese support add-ond, word, version.1'

#import chinese.model
import chinese.templates.ruby ; chinese.templates.ruby.install()
import chinese.templates.chinese ; chinese.templates.chinese.install()
import chinese.edit
import chinese.model

