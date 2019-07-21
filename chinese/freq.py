from aqt.utils import showInfo
from os.path import dirname, join, realpath
import codecs
import re
import os

def lookup_frequency(hanzi):

    # Complicated math by ernop
    levels={200:'very basic',
        100:'basic',
        50:'very common',
        25:'common',
        13:'uncommon',
        7:'rare',
        2:'very rare',
        0:'obscure'}

    slevels=sorted(levels.items(),key=lambda x:x[0]*-1)
    words=sorted([w.upper() for w in levels.values()],key=lambda x:-1*len(x))

    # Declare path to the corpus file
    corpus_path = join(dirname(realpath(__file__)), 'lib', 'num' , 'internet-zh.num')

    # Navigate to corpus file and open it or throw error if it doesn't exist
    if os.path.exists(corpus_path):
        blob=codecs.open(corpus_path,'r','utf8').read()
    else:
        showInfo('you need to copy the internet-zh.num file to %s , or edit the source file to point to the file.'%corpus_path)

    # Main logic here
    pat=re.compile('(.+ '+hanzi+')\n')
    try:
        res=pat.findall(blob)[0]
    except:
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
            frequency_html='Not found'
    else:
        description=''
        permillion=''
        frequency_html='<div class="frequency-note frequency-unknown">unknown</div>'
    return frequency_html
