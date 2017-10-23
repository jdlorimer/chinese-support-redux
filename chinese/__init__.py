# -*- coding: utf-8 ; mode: python -*-
# © 2012: Roland Sieker <ospalh@gmail.com>
# © 2012: Thomas Tempé <thomas.tempe@alysse.org>
#
# License: GNU AGPL, version 3 or later; http://www.gnu.org/copyleft/agpl.html

import chinese.edit
import chinese.graph
import chinese.models.advanced
import chinese.models.basic
# import chinese.models.compatibility
# import chinese.models.ruby
# import chinese.models.ruby_synonyms
import chinese.templates.chinese
import chinese.templates.ruby
import chinese.ui

chinese.templates.ruby.install()
chinese.templates.chinese.install()
