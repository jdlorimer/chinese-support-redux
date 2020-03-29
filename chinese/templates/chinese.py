# Copyright: Damien Elmes <anki@ichi2.net>
# Copyright 2012, Thomas TEMPE <thomas.tempe@alysse.org>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
# Based off Kieran Clancy's initial implementation.

# These templates complement the ruby.py module, and provide
# chinese-specific services. They should be used on fields containing
# chinese characters, with transcription formatted as in 吗[ma3].


try:
    from anki.template.hint import hint
    from .chinese_old import *
except (ImportError, ModuleNotFoundError):
    from .chinese_new import *
