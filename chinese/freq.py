# from aqt.utils import showInfo
from os.path import dirname, join, realpath
import codecs
import re
import os

levels={200:'very basic', #1-477                    = 500                          cum 500
    100:'basic',               #477-1016             = 500                          1000
    50:'very common',      #1017-2060           = 1000                        2000
    25:'common',               #2060-3760          = 1700                        3700
    13:'uncommon',           #3760-6313           = 2600                        6300
    7:'rare',                    #6300-10050         = 3750                        10000
    2:'very rare',           #10500-18600        = 8100                        18000
    0:'obscure'}              #18600-50000       = 31400                      50000

slevels=sorted(levels.items(),key=lambda x:x[0]*-1)
words=sorted([w.upper() for w in levels.values()],key=lambda x:-1*len(x))

# _get_abs_path = lambda path: os.path.normpath(os.path.join(os.getcwd(), path))
# corpus_path=_get_abs_path('chinese/num/internet-zh.num')
corpus_path = join(dirname(realpath(__file__)), 'lib', 'num' , 'internet-zh.num')

if os.path.exists(corpus_path):
    blob=codecs.open(corpus_path,'r','utf8').read()
else:
    showInfo('you need to copy the internet-zh.num file to %s , or edit the source file to point to the file.'%corpus_path)

def lookup_frequency(hanzi):
    pat=re.compile('(.+ '+hanzi+')\n')
    try:
        res=pat.findall(blob)[0]
    except:
        #~ showInfo('%s%s'%(repr(e),hanzi))
        #word did not exist in dict.
        return 'Not found'
    description=''
    frequency_html=''
    if res and type(res)!=tuple:
        order,permillion,chars=res.split()
        permillion=float(permillion)
        try:
            for num,name in slevels:
                if permillion>num:
                    description=name.upper()
                    frequency_html='<div class="frequency-note frequency-%s">%s</div>'%(name.replace(' ','-'), name)
                    break
        except:
            #~ showInfo(repr(e))
            frequency_html='Not found'
    else:
        description=''
        permillion=''
        frequency_html='<div class="frequency-note frequency-unknown">unknown</div>'
    return frequency_html
