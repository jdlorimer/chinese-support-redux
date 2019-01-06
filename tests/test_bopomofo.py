# Copyright © 2018-2019 Joseph Lorimer <luoliyan@posteo.net>
#
# This file is part of Chinese Support Redux.
#
# Chinese Support Redux is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# Chinese Support Redux is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along with
# Chinese Support Redux.  If not, see <https://www.gnu.org/licenses/>.

from unittest import skip

from chinese.bopomofo import bopomofo
from tests import ChineseTest


class Bopomofo(ChineseTest):
    def test_pinyin_no_tone(self):
        self.assertEqual(bopomofo(['zhu yin']), ['ㄓㄨ ㄧㄣ'])
        self.assertEqual(bopomofo(['zhu', 'yin']), ['ㄓㄨ', 'ㄧㄣ'])
        self.assertEqual(bopomofo(['zhuyin']), ['ㄓㄨㄧㄣ'])

    def test_pinyin_tone_numbers(self):
        self.assertEqual(
            bopomofo(['ni3', 'ne5', 'ru2guo3 zhu4 yin1']),
            ['ㄋㄧˇ', 'ㄋㄜ˙', 'ㄖㄨˊㄍㄨㄛˇ ㄓㄨˋ ㄧㄣ'],
        )

        self.assertEqual(bopomofo(['mei2 you3']), ['ㄇㄟˊ ㄧㄡˇ'])

    @skip
    def test_pinyin_tone_mark(self):
        self.assertEqual(bopomofo(['zhù', 'yīn']), ['ㄓㄨˋ', 'ㄧㄣ'])

    @skip
    def test_joined_word(self):
        self.assertEqual(bopomofo(['zhùyīn']), ['ㄓㄨˋ ㄧㄣ'])

    def test_pinyin_syllables_a(self):
        self.assertEqual(bopomofo(['ba']), ['ㄅㄚ'])
        self.assertEqual(bopomofo(['pa']), ['ㄆㄚ'])
        self.assertEqual(bopomofo(['ma']), ['ㄇㄚ'])
        self.assertEqual(bopomofo(['fa']), ['ㄈㄚ'])
        self.assertEqual(bopomofo(['da']), ['ㄉㄚ'])
        self.assertEqual(bopomofo(['ta']), ['ㄊㄚ'])
        self.assertEqual(bopomofo(['na']), ['ㄋㄚ'])
        self.assertEqual(bopomofo(['la']), ['ㄌㄚ'])
        self.assertEqual(bopomofo(['za']), ['ㄗㄚ'])
        self.assertEqual(bopomofo(['ca']), ['ㄘㄚ'])
        self.assertEqual(bopomofo(['sa']), ['ㄙㄚ'])
        self.assertEqual(bopomofo(['zha']), ['ㄓㄚ'])
        self.assertEqual(bopomofo(['cha']), ['ㄔㄚ'])
        self.assertEqual(bopomofo(['sha']), ['ㄕㄚ'])
        self.assertEqual(bopomofo(['ga']), ['ㄍㄚ'])
        self.assertEqual(bopomofo(['ka']), ['ㄎㄚ'])
        self.assertEqual(bopomofo(['ha']), ['ㄏㄚ'])
        self.assertEqual(bopomofo(['a']), ['ㄚ'])

    def test_pinyin_syllables_o(self):
        self.assertEqual(bopomofo(['bo']), ['ㄅㄛ'])
        self.assertEqual(bopomofo(['po']), ['ㄆㄛ'])
        self.assertEqual(bopomofo(['mo']), ['ㄇㄛ'])
        self.assertEqual(bopomofo(['fo']), ['ㄈㄛ'])
        self.assertEqual(bopomofo(['o']), ['ㄛ'])

    def test_pinyin_syllables_e(self):
        self.assertEqual(bopomofo(['me']), ['ㄇㄜ'])
        self.assertEqual(bopomofo(['de']), ['ㄉㄜ'])
        self.assertEqual(bopomofo(['te']), ['ㄊㄜ'])
        self.assertEqual(bopomofo(['ne']), ['ㄋㄜ'])
        self.assertEqual(bopomofo(['le']), ['ㄌㄜ'])
        self.assertEqual(bopomofo(['ze']), ['ㄗㄜ'])
        self.assertEqual(bopomofo(['ce']), ['ㄘㄜ'])
        self.assertEqual(bopomofo(['se']), ['ㄙㄜ'])
        self.assertEqual(bopomofo(['zhe']), ['ㄓㄜ'])
        self.assertEqual(bopomofo(['che']), ['ㄔㄜ'])
        self.assertEqual(bopomofo(['she']), ['ㄕㄜ'])
        self.assertEqual(bopomofo(['re']), ['ㄖㄜ'])
        self.assertEqual(bopomofo(['ge']), ['ㄍㄜ'])
        self.assertEqual(bopomofo(['ke']), ['ㄎㄜ'])
        self.assertEqual(bopomofo(['he']), ['ㄏㄜ'])
        self.assertEqual(bopomofo(['e']), ['ㄜ'])

    def test_pinyin_syllables_syllabic_consonant(self):
        self.assertEqual(bopomofo(['zi']), ['ㄗ'])
        self.assertEqual(bopomofo(['ci']), ['ㄘ'])
        self.assertEqual(bopomofo(['si']), ['ㄙ'])
        self.assertEqual(bopomofo(['zhi']), ['ㄓ'])
        self.assertEqual(bopomofo(['chi']), ['ㄔ'])
        self.assertEqual(bopomofo(['shi']), ['ㄕ'])
        self.assertEqual(bopomofo(['ri']), ['ㄖ'])

    def test_pinyin_syllable_er(self):
        self.assertEqual(bopomofo(['er']), ['ㄦ'])

    def test_pinyin_syllables_ai(self):
        self.assertEqual(bopomofo(['bai']), ['ㄅㄞ'])
        self.assertEqual(bopomofo(['pai']), ['ㄆㄞ'])
        self.assertEqual(bopomofo(['mai']), ['ㄇㄞ'])
        self.assertEqual(bopomofo(['dai']), ['ㄉㄞ'])
        self.assertEqual(bopomofo(['tai']), ['ㄊㄞ'])
        self.assertEqual(bopomofo(['nai']), ['ㄋㄞ'])
        self.assertEqual(bopomofo(['lai']), ['ㄌㄞ'])
        self.assertEqual(bopomofo(['zai']), ['ㄗㄞ'])
        self.assertEqual(bopomofo(['cai']), ['ㄘㄞ'])
        self.assertEqual(bopomofo(['sai']), ['ㄙㄞ'])
        self.assertEqual(bopomofo(['zhai']), ['ㄓㄞ'])
        self.assertEqual(bopomofo(['chai']), ['ㄔㄞ'])
        self.assertEqual(bopomofo(['gai']), ['ㄍㄞ'])
        self.assertEqual(bopomofo(['kai']), ['ㄎㄞ'])
        self.assertEqual(bopomofo(['hai']), ['ㄏㄞ'])
        self.assertEqual(bopomofo(['ai']), ['ㄞ'])

    def test_pinyin_syllables_ei(self):
        self.assertEqual(bopomofo(['bei']), ['ㄅㄟ'])
        self.assertEqual(bopomofo(['pei']), ['ㄆㄟ'])
        self.assertEqual(bopomofo(['mei']), ['ㄇㄟ'])
        self.assertEqual(bopomofo(['fei']), ['ㄈㄟ'])
        self.assertEqual(bopomofo(['dei']), ['ㄉㄟ'])
        self.assertEqual(bopomofo(['nei']), ['ㄋㄟ'])
        self.assertEqual(bopomofo(['lei']), ['ㄌㄟ'])
        self.assertEqual(bopomofo(['zei']), ['ㄗㄟ'])
        self.assertEqual(bopomofo(['zhei']), ['ㄓㄟ'])
        self.assertEqual(bopomofo(['shei']), ['ㄕㄟ'])
        self.assertEqual(bopomofo(['gei']), ['ㄍㄟ'])
        self.assertEqual(bopomofo(['kei']), ['ㄎㄟ'])
        self.assertEqual(bopomofo(['hei']), ['ㄏㄟ'])
        self.assertEqual(bopomofo(['ei']), ['ㄟ'])

    def test_pinyin_syllables_ao(self):
        self.assertEqual(bopomofo(['bao']), ['ㄅㄠ'])
        self.assertEqual(bopomofo(['pao']), ['ㄆㄠ'])
        self.assertEqual(bopomofo(['mao']), ['ㄇㄠ'])
        self.assertEqual(bopomofo(['dao']), ['ㄉㄠ'])
        self.assertEqual(bopomofo(['tao']), ['ㄊㄠ'])
        self.assertEqual(bopomofo(['nao']), ['ㄋㄠ'])
        self.assertEqual(bopomofo(['lao']), ['ㄌㄠ'])
        self.assertEqual(bopomofo(['zao']), ['ㄗㄠ'])
        self.assertEqual(bopomofo(['cao']), ['ㄘㄠ'])
        self.assertEqual(bopomofo(['sao']), ['ㄙㄠ'])
        self.assertEqual(bopomofo(['zhao']), ['ㄓㄠ'])
        self.assertEqual(bopomofo(['chao']), ['ㄔㄠ'])
        self.assertEqual(bopomofo(['shao']), ['ㄕㄠ'])
        self.assertEqual(bopomofo(['rao']), ['ㄖㄠ'])
        self.assertEqual(bopomofo(['gao']), ['ㄍㄠ'])
        self.assertEqual(bopomofo(['kao']), ['ㄎㄠ'])
        self.assertEqual(bopomofo(['hao']), ['ㄏㄠ'])
        self.assertEqual(bopomofo(['ao']), ['ㄠ'])

    def test_pinyin_syllables_ou(self):
        self.assertEqual(bopomofo(['pou']), ['ㄆㄡ'])
        self.assertEqual(bopomofo(['mou']), ['ㄇㄡ'])
        self.assertEqual(bopomofo(['fou']), ['ㄈㄡ'])
        self.assertEqual(bopomofo(['dou']), ['ㄉㄡ'])
        self.assertEqual(bopomofo(['tou']), ['ㄊㄡ'])
        self.assertEqual(bopomofo(['nou']), ['ㄋㄡ'])
        self.assertEqual(bopomofo(['lou']), ['ㄌㄡ'])
        self.assertEqual(bopomofo(['zou']), ['ㄗㄡ'])
        self.assertEqual(bopomofo(['sou']), ['ㄙㄡ'])
        self.assertEqual(bopomofo(['zhou']), ['ㄓㄡ'])
        self.assertEqual(bopomofo(['chou']), ['ㄔㄡ'])
        self.assertEqual(bopomofo(['shou']), ['ㄕㄡ'])
        self.assertEqual(bopomofo(['rou']), ['ㄖㄡ'])
        self.assertEqual(bopomofo(['gou']), ['ㄍㄡ'])
        self.assertEqual(bopomofo(['kou']), ['ㄎㄡ'])
        self.assertEqual(bopomofo(['hou']), ['ㄏㄡ'])
        self.assertEqual(bopomofo(['ou']), ['ㄡ'])

    def test_pinyin_syllables_an(self):
        self.assertEqual(bopomofo(['ban']), ['ㄅㄢ'])
        self.assertEqual(bopomofo(['pan']), ['ㄆㄢ'])
        self.assertEqual(bopomofo(['man']), ['ㄇㄢ'])
        self.assertEqual(bopomofo(['fan']), ['ㄈㄢ'])
        self.assertEqual(bopomofo(['dan']), ['ㄉㄢ'])
        self.assertEqual(bopomofo(['tan']), ['ㄊㄢ'])
        self.assertEqual(bopomofo(['nan']), ['ㄋㄢ'])
        self.assertEqual(bopomofo(['lan']), ['ㄌㄢ'])
        self.assertEqual(bopomofo(['zan']), ['ㄗㄢ'])
        self.assertEqual(bopomofo(['can']), ['ㄘㄢ'])
        self.assertEqual(bopomofo(['san']), ['ㄙㄢ'])
        self.assertEqual(bopomofo(['zhan']), ['ㄓㄢ'])
        self.assertEqual(bopomofo(['chan']), ['ㄔㄢ'])
        self.assertEqual(bopomofo(['shan']), ['ㄕㄢ'])
        self.assertEqual(bopomofo(['ran']), ['ㄖㄢ'])
        self.assertEqual(bopomofo(['gan']), ['ㄍㄢ'])
        self.assertEqual(bopomofo(['kan']), ['ㄎㄢ'])
        self.assertEqual(bopomofo(['han']), ['ㄏㄢ'])
        self.assertEqual(bopomofo(['an']), ['ㄢ'])

    def test_pinyin_syllables_en(self):
        self.assertEqual(bopomofo(['ben']), ['ㄅㄣ'])
        self.assertEqual(bopomofo(['pen']), ['ㄆㄣ'])
        self.assertEqual(bopomofo(['men']), ['ㄇㄣ'])
        self.assertEqual(bopomofo(['fen']), ['ㄈㄣ'])
        self.assertEqual(bopomofo(['den']), ['ㄉㄣ'])
        self.assertEqual(bopomofo(['nen']), ['ㄋㄣ'])
        self.assertEqual(bopomofo(['zen']), ['ㄗㄣ'])
        self.assertEqual(bopomofo(['cen']), ['ㄘㄣ'])
        self.assertEqual(bopomofo(['sen']), ['ㄙㄣ'])
        self.assertEqual(bopomofo(['zhen']), ['ㄓㄣ'])
        self.assertEqual(bopomofo(['chen']), ['ㄔㄣ'])
        self.assertEqual(bopomofo(['shen']), ['ㄕㄣ'])
        self.assertEqual(bopomofo(['ren']), ['ㄖㄣ'])
        self.assertEqual(bopomofo(['gen']), ['ㄍㄣ'])
        self.assertEqual(bopomofo(['ken']), ['ㄎㄣ'])
        self.assertEqual(bopomofo(['hen']), ['ㄏㄣ'])
        self.assertEqual(bopomofo(['en']), ['ㄣ'])

    def test_pinyin_syllables_ang(self):
        self.assertEqual(bopomofo(['bang']), ['ㄅㄤ'])
        self.assertEqual(bopomofo(['pang']), ['ㄆㄤ'])
        self.assertEqual(bopomofo(['mang']), ['ㄇㄤ'])
        self.assertEqual(bopomofo(['fang']), ['ㄈㄤ'])
        self.assertEqual(bopomofo(['dang']), ['ㄉㄤ'])
        self.assertEqual(bopomofo(['tang']), ['ㄊㄤ'])
        self.assertEqual(bopomofo(['nang']), ['ㄋㄤ'])
        self.assertEqual(bopomofo(['lang']), ['ㄌㄤ'])
        self.assertEqual(bopomofo(['zang']), ['ㄗㄤ'])
        self.assertEqual(bopomofo(['cang']), ['ㄘㄤ'])
        self.assertEqual(bopomofo(['sang']), ['ㄙㄤ'])
        self.assertEqual(bopomofo(['zhang']), ['ㄓㄤ'])
        self.assertEqual(bopomofo(['shang']), ['ㄕㄤ'])
        self.assertEqual(bopomofo(['rang']), ['ㄖㄤ'])
        self.assertEqual(bopomofo(['gang']), ['ㄍㄤ'])
        self.assertEqual(bopomofo(['kang']), ['ㄎㄤ'])
        self.assertEqual(bopomofo(['hang']), ['ㄏㄤ'])
        self.assertEqual(bopomofo(['ang']), ['ㄤ'])

    def test_pinyin_syllables_eng(self):
        self.assertEqual(bopomofo(['beng']), ['ㄅㄥ'])
        self.assertEqual(bopomofo(['peng']), ['ㄆㄥ'])
        self.assertEqual(bopomofo(['meng']), ['ㄇㄥ'])
        self.assertEqual(bopomofo(['feng']), ['ㄈㄥ'])
        self.assertEqual(bopomofo(['deng']), ['ㄉㄥ'])
        self.assertEqual(bopomofo(['teng']), ['ㄊㄥ'])
        self.assertEqual(bopomofo(['neng']), ['ㄋㄥ'])
        self.assertEqual(bopomofo(['leng']), ['ㄌㄥ'])
        self.assertEqual(bopomofo(['zeng']), ['ㄗㄥ'])
        self.assertEqual(bopomofo(['ceng']), ['ㄘㄥ'])
        self.assertEqual(bopomofo(['seng']), ['ㄙㄥ'])
        self.assertEqual(bopomofo(['zheng']), ['ㄓㄥ'])
        self.assertEqual(bopomofo(['sheng']), ['ㄕㄥ'])
        self.assertEqual(bopomofo(['reng']), ['ㄖㄥ'])
        self.assertEqual(bopomofo(['geng']), ['ㄍㄥ'])
        self.assertEqual(bopomofo(['keng']), ['ㄎㄥ'])
        self.assertEqual(bopomofo(['heng']), ['ㄏㄥ'])
        self.assertEqual(bopomofo(['eng']), ['ㄥ'])

    def test_pinyin_syllables_ong(self):
        self.assertEqual(bopomofo(['dong']), ['ㄉㄨㄥ'])
        self.assertEqual(bopomofo(['tong']), ['ㄊㄨㄥ'])
        self.assertEqual(bopomofo(['nong']), ['ㄋㄨㄥ'])
        self.assertEqual(bopomofo(['long']), ['ㄌㄨㄥ'])
        self.assertEqual(bopomofo(['zong']), ['ㄗㄨㄥ'])
        self.assertEqual(bopomofo(['cong']), ['ㄘㄨㄥ'])
        self.assertEqual(bopomofo(['song']), ['ㄙㄨㄥ'])
        self.assertEqual(bopomofo(['zhong']), ['ㄓㄨㄥ'])
        self.assertEqual(bopomofo(['rong']), ['ㄖㄨㄥ'])
        self.assertEqual(bopomofo(['gong']), ['ㄍㄨㄥ'])
        self.assertEqual(bopomofo(['kong']), ['ㄎㄨㄥ'])
        self.assertEqual(bopomofo(['hong']), ['ㄏㄨㄥ'])

    def test_pinyin_syllables_yi(self):
        self.assertEqual(bopomofo(['bi']), ['ㄅㄧ'])
        self.assertEqual(bopomofo(['pi']), ['ㄆㄧ'])
        self.assertEqual(bopomofo(['mi']), ['ㄇㄧ'])
        self.assertEqual(bopomofo(['di']), ['ㄉㄧ'])
        self.assertEqual(bopomofo(['ti']), ['ㄊㄧ'])
        self.assertEqual(bopomofo(['ni']), ['ㄋㄧ'])
        self.assertEqual(bopomofo(['li']), ['ㄌㄧ'])
        self.assertEqual(bopomofo(['ji']), ['ㄐㄧ'])
        self.assertEqual(bopomofo(['qi']), ['ㄑㄧ'])
        self.assertEqual(bopomofo(['xi']), ['ㄒㄧ'])
        self.assertEqual(bopomofo(['yi']), ['ㄧ'])

    def test_pinyin_syllables_ya(self):
        self.assertEqual(bopomofo(['lia']), ['ㄌㄧㄚ'])
        self.assertEqual(bopomofo(['jia']), ['ㄐㄧㄚ'])
        self.assertEqual(bopomofo(['qia']), ['ㄑㄧㄚ'])
        self.assertEqual(bopomofo(['xia']), ['ㄒㄧㄚ'])
        self.assertEqual(bopomofo(['ya']), ['ㄧㄚ'])

    def test_pinyin_syllables_ye(self):
        self.assertEqual(bopomofo(['bie']), ['ㄅㄧㄝ'])
        self.assertEqual(bopomofo(['pie']), ['ㄆㄧㄝ'])
        self.assertEqual(bopomofo(['mie']), ['ㄇㄧㄝ'])
        self.assertEqual(bopomofo(['die']), ['ㄉㄧㄝ'])
        self.assertEqual(bopomofo(['tie']), ['ㄊㄧㄝ'])
        self.assertEqual(bopomofo(['nie']), ['ㄋㄧㄝ'])
        self.assertEqual(bopomofo(['lie']), ['ㄌㄧㄝ'])
        self.assertEqual(bopomofo(['jie']), ['ㄐㄧㄝ'])
        self.assertEqual(bopomofo(['qie']), ['ㄑㄧㄝ'])
        self.assertEqual(bopomofo(['xie']), ['ㄒㄧㄝ'])
        self.assertEqual(bopomofo(['ye']), ['ㄧㄝ'])

    def test_pinyin_syllables_yao(self):
        self.assertEqual(bopomofo(['biao']), ['ㄅㄧㄠ'])
        self.assertEqual(bopomofo(['piao']), ['ㄆㄧㄠ'])
        self.assertEqual(bopomofo(['miao']), ['ㄇㄧㄠ'])
        self.assertEqual(bopomofo(['diao']), ['ㄉㄧㄠ'])
        self.assertEqual(bopomofo(['tiao']), ['ㄊㄧㄠ'])
        self.assertEqual(bopomofo(['niao']), ['ㄋㄧㄠ'])
        self.assertEqual(bopomofo(['liao']), ['ㄌㄧㄠ'])
        self.assertEqual(bopomofo(['jiao']), ['ㄐㄧㄠ'])
        self.assertEqual(bopomofo(['qiao']), ['ㄑㄧㄠ'])
        self.assertEqual(bopomofo(['xiao']), ['ㄒㄧㄠ'])
        self.assertEqual(bopomofo(['yao']), ['ㄧㄠ'])

    def test_pinyin_syllables_you(self):
        self.assertEqual(bopomofo(['miu']), ['ㄇㄧㄡ'])
        self.assertEqual(bopomofo(['diu']), ['ㄉㄧㄡ'])
        self.assertEqual(bopomofo(['niu']), ['ㄋㄧㄡ'])
        self.assertEqual(bopomofo(['liu']), ['ㄌㄧㄡ'])
        self.assertEqual(bopomofo(['jiu']), ['ㄐㄧㄡ'])
        self.assertEqual(bopomofo(['qiu']), ['ㄑㄧㄡ'])
        self.assertEqual(bopomofo(['xiu']), ['ㄒㄧㄡ'])
        self.assertEqual(bopomofo(['you']), ['ㄧㄡ'])

    def test_pinyin_syllables_yan(self):
        self.assertEqual(bopomofo(['bian']), ['ㄅㄧㄢ'])
        self.assertEqual(bopomofo(['pian']), ['ㄆㄧㄢ'])
        self.assertEqual(bopomofo(['mian']), ['ㄇㄧㄢ'])
        self.assertEqual(bopomofo(['dian']), ['ㄉㄧㄢ'])
        self.assertEqual(bopomofo(['tian']), ['ㄊㄧㄢ'])
        self.assertEqual(bopomofo(['nian']), ['ㄋㄧㄢ'])
        self.assertEqual(bopomofo(['lian']), ['ㄌㄧㄢ'])
        self.assertEqual(bopomofo(['jian']), ['ㄐㄧㄢ'])
        self.assertEqual(bopomofo(['qian']), ['ㄑㄧㄢ'])
        self.assertEqual(bopomofo(['xian']), ['ㄒㄧㄢ'])
        self.assertEqual(bopomofo(['yan']), ['ㄧㄢ'])

    def test_pinyin_syllables_yin(self):
        self.assertEqual(bopomofo(['bin']), ['ㄅㄧㄣ'])
        self.assertEqual(bopomofo(['pin']), ['ㄆㄧㄣ'])
        self.assertEqual(bopomofo(['min']), ['ㄇㄧㄣ'])
        self.assertEqual(bopomofo(['nin']), ['ㄋㄧㄣ'])
        self.assertEqual(bopomofo(['lin']), ['ㄌㄧㄣ'])
        self.assertEqual(bopomofo(['jin']), ['ㄐㄧㄣ'])
        self.assertEqual(bopomofo(['qin']), ['ㄑㄧㄣ'])
        self.assertEqual(bopomofo(['xin']), ['ㄒㄧㄣ'])
        self.assertEqual(bopomofo(['yin']), ['ㄧㄣ'])

    def test_pinyin_syllables_yang(self):
        self.assertEqual(bopomofo(['niang']), ['ㄋㄧㄤ'])
        self.assertEqual(bopomofo(['liang']), ['ㄌㄧㄤ'])
        self.assertEqual(bopomofo(['jiang']), ['ㄐㄧㄤ'])
        self.assertEqual(bopomofo(['qiang']), ['ㄑㄧㄤ'])
        self.assertEqual(bopomofo(['xiang']), ['ㄒㄧㄤ'])
        self.assertEqual(bopomofo(['yang']), ['ㄧㄤ'])

    def test_pinyin_syllables_ying(self):
        self.assertEqual(bopomofo(['bing']), ['ㄅㄧㄥ'])
        self.assertEqual(bopomofo(['ping']), ['ㄆㄧㄥ'])
        self.assertEqual(bopomofo(['ming']), ['ㄇㄧㄥ'])
        self.assertEqual(bopomofo(['ding']), ['ㄉㄧㄥ'])
        self.assertEqual(bopomofo(['ting']), ['ㄊㄧㄥ'])
        self.assertEqual(bopomofo(['ning']), ['ㄋㄧㄥ'])
        self.assertEqual(bopomofo(['ling']), ['ㄌㄧㄥ'])
        self.assertEqual(bopomofo(['jing']), ['ㄐㄧㄥ'])
        self.assertEqual(bopomofo(['qing']), ['ㄑㄧㄥ'])
        self.assertEqual(bopomofo(['xing']), ['ㄒㄧㄥ'])
        self.assertEqual(bopomofo(['ying']), ['ㄧㄥ'])

    def test_pinyin_syllables_yong(self):
        self.assertEqual(bopomofo(['jiong']), ['ㄐㄩㄥ'])
        self.assertEqual(bopomofo(['qiong']), ['ㄑㄩㄥ'])
        self.assertEqual(bopomofo(['xiong']), ['ㄒㄩㄥ'])
        self.assertEqual(bopomofo(['yong']), ['ㄩㄥ'])

    def test_pinyin_syllables_wu(self):
        self.assertEqual(bopomofo(['bu']), ['ㄅㄨ'])
        self.assertEqual(bopomofo(['pu']), ['ㄆㄨ'])
        self.assertEqual(bopomofo(['mu']), ['ㄇㄨ'])
        self.assertEqual(bopomofo(['fu']), ['ㄈㄨ'])
        self.assertEqual(bopomofo(['du']), ['ㄉㄨ'])
        self.assertEqual(bopomofo(['tu']), ['ㄊㄨ'])
        self.assertEqual(bopomofo(['nu']), ['ㄋㄨ'])
        self.assertEqual(bopomofo(['lu']), ['ㄌㄨ'])
        self.assertEqual(bopomofo(['zu']), ['ㄗㄨ'])
        self.assertEqual(bopomofo(['cu']), ['ㄘㄨ'])
        self.assertEqual(bopomofo(['su']), ['ㄙㄨ'])
        self.assertEqual(bopomofo(['zhu']), ['ㄓㄨ'])
        self.assertEqual(bopomofo(['chu']), ['ㄔㄨ'])
        self.assertEqual(bopomofo(['shu']), ['ㄕㄨ'])
        self.assertEqual(bopomofo(['ru']), ['ㄖㄨ'])
        self.assertEqual(bopomofo(['gu']), ['ㄍㄨ'])
        self.assertEqual(bopomofo(['ku']), ['ㄎㄨ'])
        self.assertEqual(bopomofo(['hu']), ['ㄏㄨ'])
        self.assertEqual(bopomofo(['wu']), ['ㄨ'])

    def test_pinyin_syllables_wa(self):
        self.assertEqual(bopomofo(['zhua']), ['ㄓㄨㄚ'])
        self.assertEqual(bopomofo(['chua']), ['ㄔㄨㄚ'])
        self.assertEqual(bopomofo(['shua']), ['ㄕㄨㄚ'])
        self.assertEqual(bopomofo(['gua']), ['ㄍㄨㄚ'])
        self.assertEqual(bopomofo(['kua']), ['ㄎㄨㄚ'])
        self.assertEqual(bopomofo(['hua']), ['ㄏㄨㄚ'])
        self.assertEqual(bopomofo(['wa']), ['ㄨㄚ'])

    def test_pinyin_syllables_wo(self):
        self.assertEqual(bopomofo(['duo']), ['ㄉㄨㄛ'])
        self.assertEqual(bopomofo(['tuo']), ['ㄊㄨㄛ'])
        self.assertEqual(bopomofo(['nuo']), ['ㄋㄨㄛ'])
        self.assertEqual(bopomofo(['luo']), ['ㄌㄨㄛ'])
        self.assertEqual(bopomofo(['zuo']), ['ㄗㄨㄛ'])
        self.assertEqual(bopomofo(['cuo']), ['ㄘㄨㄛ'])
        self.assertEqual(bopomofo(['suo']), ['ㄙㄨㄛ'])
        self.assertEqual(bopomofo(['zhuo']), ['ㄓㄨㄛ'])
        self.assertEqual(bopomofo(['chuo']), ['ㄔㄨㄛ'])
        self.assertEqual(bopomofo(['shuo']), ['ㄕㄨㄛ'])
        self.assertEqual(bopomofo(['ruo']), ['ㄖㄨㄛ'])
        self.assertEqual(bopomofo(['guo']), ['ㄍㄨㄛ'])
        self.assertEqual(bopomofo(['kuo']), ['ㄎㄨㄛ'])
        self.assertEqual(bopomofo(['huo']), ['ㄏㄨㄛ'])
        self.assertEqual(bopomofo(['wo']), ['ㄨㄛ'])

    def test_pinyin_syllables_wai(self):
        self.assertEqual(bopomofo(['zhuai']), ['ㄓㄨㄞ'])
        self.assertEqual(bopomofo(['chuai']), ['ㄔㄨㄞ'])
        self.assertEqual(bopomofo(['shuai']), ['ㄕㄨㄞ'])
        self.assertEqual(bopomofo(['guai']), ['ㄍㄨㄞ'])
        self.assertEqual(bopomofo(['kuai']), ['ㄎㄨㄞ'])
        self.assertEqual(bopomofo(['huai']), ['ㄏㄨㄞ'])
        self.assertEqual(bopomofo(['wai']), ['ㄨㄞ'])

    def test_pinyin_syllables_wei(self):
        self.assertEqual(bopomofo(['dui']), ['ㄉㄨㄟ'])
        self.assertEqual(bopomofo(['tui']), ['ㄊㄨㄟ'])
        self.assertEqual(bopomofo(['zui']), ['ㄗㄨㄟ'])
        self.assertEqual(bopomofo(['cui']), ['ㄘㄨㄟ'])
        self.assertEqual(bopomofo(['sui']), ['ㄙㄨㄟ'])
        self.assertEqual(bopomofo(['zhui']), ['ㄓㄨㄟ'])
        self.assertEqual(bopomofo(['chui']), ['ㄔㄨㄟ'])
        self.assertEqual(bopomofo(['shui']), ['ㄕㄨㄟ'])
        self.assertEqual(bopomofo(['rui']), ['ㄖㄨㄟ'])
        self.assertEqual(bopomofo(['gui']), ['ㄍㄨㄟ'])
        self.assertEqual(bopomofo(['kui']), ['ㄎㄨㄟ'])
        self.assertEqual(bopomofo(['hui']), ['ㄏㄨㄟ'])
        self.assertEqual(bopomofo(['wei']), ['ㄨㄟ'])

    def test_pinyin_syllables_wan(self):
        self.assertEqual(bopomofo(['duan']), ['ㄉㄨㄢ'])
        self.assertEqual(bopomofo(['tuan']), ['ㄊㄨㄢ'])
        self.assertEqual(bopomofo(['nuan']), ['ㄋㄨㄢ'])
        self.assertEqual(bopomofo(['luan']), ['ㄌㄨㄢ'])
        self.assertEqual(bopomofo(['zuan']), ['ㄗㄨㄢ'])
        self.assertEqual(bopomofo(['cuan']), ['ㄘㄨㄢ'])
        self.assertEqual(bopomofo(['suan']), ['ㄙㄨㄢ'])
        self.assertEqual(bopomofo(['zhuan']), ['ㄓㄨㄢ'])
        self.assertEqual(bopomofo(['chuan']), ['ㄔㄨㄢ'])
        self.assertEqual(bopomofo(['shuan']), ['ㄕㄨㄢ'])
        self.assertEqual(bopomofo(['ruan']), ['ㄖㄨㄢ'])
        self.assertEqual(bopomofo(['guan']), ['ㄍㄨㄢ'])
        self.assertEqual(bopomofo(['kuan']), ['ㄎㄨㄢ'])
        self.assertEqual(bopomofo(['huan']), ['ㄏㄨㄢ'])
        self.assertEqual(bopomofo(['wan']), ['ㄨㄢ'])

    def test_pinyin_syllables_wen(self):
        self.assertEqual(bopomofo(['dun']), ['ㄉㄨㄣ'])
        self.assertEqual(bopomofo(['tun']), ['ㄊㄨㄣ'])
        self.assertEqual(bopomofo(['lun']), ['ㄌㄨㄣ'])
        self.assertEqual(bopomofo(['zun']), ['ㄗㄨㄣ'])
        self.assertEqual(bopomofo(['cun']), ['ㄘㄨㄣ'])
        self.assertEqual(bopomofo(['sun']), ['ㄙㄨㄣ'])
        self.assertEqual(bopomofo(['zhun']), ['ㄓㄨㄣ'])
        self.assertEqual(bopomofo(['chun']), ['ㄔㄨㄣ'])
        self.assertEqual(bopomofo(['shun']), ['ㄕㄨㄣ'])
        self.assertEqual(bopomofo(['run']), ['ㄖㄨㄣ'])
        self.assertEqual(bopomofo(['gun']), ['ㄍㄨㄣ'])
        self.assertEqual(bopomofo(['kun']), ['ㄎㄨㄣ'])
        self.assertEqual(bopomofo(['hun']), ['ㄏㄨㄣ'])
        self.assertEqual(bopomofo(['wen']), ['ㄨㄣ'])

    def test_pinyin_syllables_wang(self):
        self.assertEqual(bopomofo(['zhuang']), ['ㄓㄨㄤ'])
        self.assertEqual(bopomofo(['chuang']), ['ㄔㄨㄤ'])
        self.assertEqual(bopomofo(['shuang']), ['ㄕㄨㄤ'])
        self.assertEqual(bopomofo(['guang']), ['ㄍㄨㄤ'])
        self.assertEqual(bopomofo(['kuang']), ['ㄎㄨㄤ'])
        self.assertEqual(bopomofo(['huang']), ['ㄏㄨㄤ'])
        self.assertEqual(bopomofo(['wang']), ['ㄨㄤ'])

    def test_pinyin_syllable_weng(self):
        self.assertEqual(bopomofo(['weng']), ['ㄨㄥ'])

    def test_pinyin_syllables_yu(self):
        self.assertEqual(bopomofo(['nü']), ['ㄋㄩ'])
        self.assertEqual(bopomofo(['lü']), ['ㄌㄩ'])
        self.assertEqual(bopomofo(['ju']), ['ㄐㄩ'])
        self.assertEqual(bopomofo(['qu']), ['ㄑㄩ'])
        self.assertEqual(bopomofo(['xu']), ['ㄒㄩ'])
        self.assertEqual(bopomofo(['yu']), ['ㄩ'])

    def test_pinyin_syllables_yue(self):
        self.assertEqual(bopomofo(['nüe']), ['ㄋㄩㄝ'])
        self.assertEqual(bopomofo(['lüe']), ['ㄌㄩㄝ'])
        self.assertEqual(bopomofo(['jue']), ['ㄐㄩㄝ'])
        self.assertEqual(bopomofo(['que']), ['ㄑㄩㄝ'])
        self.assertEqual(bopomofo(['xue']), ['ㄒㄩㄝ'])
        self.assertEqual(bopomofo(['yue']), ['ㄩㄝ'])

    def test_pinyin_syllables_yuan(self):
        self.assertEqual(bopomofo(['juan']), ['ㄐㄩㄢ'])
        self.assertEqual(bopomofo(['quan']), ['ㄑㄩㄢ'])
        self.assertEqual(bopomofo(['xuan']), ['ㄒㄩㄢ'])
        self.assertEqual(bopomofo(['yuan']), ['ㄩㄢ'])

    def test_pinyin_syllables_yun(self):
        self.assertEqual(bopomofo(['jun']), ['ㄐㄩㄣ'])
        self.assertEqual(bopomofo(['qun']), ['ㄑㄩㄣ'])
        self.assertEqual(bopomofo(['xun']), ['ㄒㄩㄣ'])
        self.assertEqual(bopomofo(['yun']), ['ㄩㄣ'])
