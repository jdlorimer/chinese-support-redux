# -*- mode: python; coding: utf-8 -*-
#
# Copyright © 2012 Roland Sieker, ospalh@gmail.com
# Inspiration and source of the URL: Tymon Warecki
# Adapted by Thomas TEMPE, thomas.tempe@alysse.org
#
# License: AGNU GPL, version 3 or later; http://www.gnu.org/copyleft/agpl.html


'''
Download pronunciations from GoogleTTS
'''

import tempfile
import urllib
import urllib2
import os
import re
import os.path
from aqt import mw


download_file_extension = u'.mp3'

url_gtts = 'http://translate.google.com/translate_tts?'

user_agent_string = 'Mozilla/5.0'


def get_word_from_google(source, language="zh"):
    filename, fullpath =get_filename(source, download_file_extension)
    if os.path.exists(fullpath):
	    return filename
    get_url = build_query_url(source, language)
    # This may throw an exception
    request = urllib2.Request(get_url)
    request.add_header('User-agent', user_agent_string)
    response = urllib2.urlopen(request)
    if 200 != response.code:
        raise ValueError(str(response.code) + ': ' + response.msg)
    temp_file = tempfile.NamedTemporaryFile(delete=False,
                                            suffix=download_file_extension)
    temp_file.write(response.read())
    temp_file.close()
    extras = dict(source='GoogleTTS')
    try:
        return process_audio(temp_file.name, source, download_file_extension)
    except:
        return unmunge_to_mediafile(temp_file.name, source,
                                    download_file_extension)


def build_query_url(source, language):
        qdict = {}
        qdict['tl'] = language.encode('utf-8')
        qdict['q'] = source.encode('utf-8')
        return url_gtts + urllib.urlencode(qdict)

# IAR. Variables before imports. The packages we import are rather
# obscure. Don't fail when they aren't there.
sox_fail = None
pydub_fail = None

try:
    import pysox
except ImportError as ie:
    sox_fail = ie

try:
    from pydub import AudioSegment
except ImportError as ie:
    pydub_fail = ie


### Use a format here that sox can write and that Anki can play. Only
### formats that your Anki can read are useful. If in doubt, use
### ".wav". (Typically sox can write about any audio file format, or
### any audio file format but mp3.)
## Small, lossy, otherwise nice but may not work with your Anki
# output_format = ".ogg"
## Safe, but large files.
output_format = ".wav"
## Lossy. Should work with Anki. May not work with your sox
# output_format = ".mp3"
## Not quite as big as .wav, lossless, rather nice but may not work
## with your Anki
# output_format = ".flac"


def process_audio(temp_file_name, base_name, suffix,
                  silence_percent=0.1, silence_end_percent=None):
    """
    Process audio.

    Take the audio file with file_name, convert mono to stereo, clip
    silence at the begining and end, normalize, convert to format
    indicated by output_format, put in the media folder with a
    suitable file name and return that base name.
    """
    if sox_fail:
        # unmunge_to_mediafile(temp_file_name, base_name, suffix)
        raise sox_fail
    # Note: Typical errors of the form_NNs: EOFError: file is not mp3
    # IOError: no such file
    # Typical error of CSoxSTream constructur: UnicodeEncodeError:
    # File is perfectly all right, but not English (i.e., with a pure
    # ASCII name). We have to work around files with non-ascii names.
    # And now we just
    try:
        sox_in_file = pysox.CSoxStream(temp_file_name)
    except IOError:
        if pydub_fail or not '.mp3' == suffix:
            # We can't do anything about the error after all.  (We CAN
            # save mp3 files with pydub. Some soxes can't handle
            # mp3s. Those that can should not raise the IOError.)
            raise
        # So use pydub to convert mp3s to wavs.
        segments = AudioSegment.from_mp3(temp_file_name)
        wav_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
        wav_file.close()
        segments.export(wav_file.name, format='wav')
        os.remove(temp_file_name)
        temp_file_name = wav_file.name
        sox_in_file = pysox.CSoxStream(temp_file_name)
        # Now we should be pretty much at the point we were at the
        # except IOError. With the data in the sox_in_file object.
    # Now do the processing with pysox.
    tof = tempfile.NamedTemporaryFile(delete=False, suffix=output_format)
    temp_out_file_name = tof.name
    tof.close()
    sox_signal = sox_in_file.get_signal()
    # We want to pull up mono to stereo, but not downmix more-channel
    # stuff to two channels.  Looks like we have to change the signal
    # as well as use the channels effect.
    in_channels = sox_signal.get_signalinfo()['channels']
    if 1 == in_channels:
        sox_signal.set_param(channels=2)
    sox_out_file = pysox.CSoxStream(temp_out_file_name, 'w', sox_signal)
    sox_chain = pysox.CEffectsChain(sox_in_file, sox_out_file)
    sox_chain.add_effect(
        pysox.CEffect('silence', [b'1', b'0', '{}%'.format(silence_percent)]))
    # Trick: to automatically remove silence at the end, reverse,
    # remove at the front and reverse.
    sox_chain.add_effect(pysox.CEffect('reverse', []))
    if not silence_end_percent:
        silence_end_percent = silence_percent
    sox_chain.add_effect(
        pysox.CEffect('silence',
                      [b'1', b'0', '{}%'.format(silence_end_percent)]))
    sox_chain.add_effect(pysox.CEffect('reverse', []))
    sox_chain.add_effect(pysox.CEffect('gain', [b'-n']))
    if 1 == in_channels:
        # Work around what appears a bug in pysox. Looks like we need
        # to duplicate the samples. And to do that, we have to pretend
        # to go from 2 channels to 4 channels. In reality we go from 1
        # channel to 2. (pysox's development status is alpha, so i'm
        # not complaining)
        sox_chain.add_effect(pysox.CEffect('channels', [b'4']))
    sox_chain.flow_effects()
    sox_out_file.close()
    os.remove(temp_file_name)
    return unmunge_to_mediafile(temp_out_file_name,
                                base_name, output_format)


def get_filename(base, end):
    """Return the media filename for the given title.
    """
    # Basically stripping the 'invalidFilenameChars'. (Not tested too much).
    base = re.sub('[\\/:\*?"<>\|]', '', base)
    mdir = mw.col.media.dir()
    return base+end, os.path.join(mdir, base + end)


def unmunge_to_mediafile(temp_file_name, media_base_name, suffix):
    """
    Copy content of temp_file_name to a file in the media directory.

    Copy content of temp_file_name to a file in the media directory
    with a name based on . media_base_name and suffix.
    """
    media_file_name, media_fullname = get_filename(media_base_name, suffix)
    tfile = open(temp_file_name, "rb")
    mfile = open(media_fullname, 'wb')
    mfile.write(tfile.read())
    tfile.close()
    mfile.close()
    os.remove(temp_file_name)
    return media_file_name
