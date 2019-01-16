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

from chinese.hanzi import (
    has_hanzi,
    split_hanzi,
    get_silhouette,
    get_simp,
    get_trad,
)
from tests import Base


class HasHanzi(Base):
    def test_all_hanzi(self):
        self.assertTrue(has_hanzi('现在'))

    def test_no_hanzi(self):
        self.assertFalse(has_hanzi('now'))

    def test_mixed(self):
        self.assertTrue(has_hanzi('现在now'))


class Silhouette(Base):
    def test_hanzi_only(self):
        self.assertEqual(get_silhouette('以A为B'), '_A_B')

    def test_mixed_chars(self):
        self.assertEqual(get_silhouette('哈密瓜'), '_ _ _')


class Simplify(Base):
    def test_simplify(self):
        self.assertEqual(get_simp('繁體字'), '繁体字')

    def test_simplify_not_in_database(self):
        self.assertIs(get_simp('𠂉'), None)


class Traditional(Base):
    def test_traditional(self):
        self.assertEqual(get_trad('简体字'), '簡體字')

    def test_traditional_not_in_database(self):
        self.assertIs(get_trad('𠂉'), None)


class SplitHanzi(Base):
    def test_grouped_input_spaced_punc(self):
        self.assertEqual(
            split_hanzi('没有 ，是 我 第一次 来 上海 旅游 。'),
            ['没有', '，', '是', '我', '第一次', '来', '上海', '旅游', '。'],
        )

    def test_grouped_input_unspaced_punc(self):
        self.assertEqual(
            split_hanzi('没有，是 我 第一次 来 上海 旅游。'),
            ['没有', '，', '是', '我', '第一次', '来', '上海', '旅游', '。'],
        )

    def test_grouped_input_ungrouped_output(self):
        self.assertEqual(
            split_hanzi('没有，是 我 第一次 来 上海 旅游。', grouped=False),
            [
                '没',
                '有',
                '，',
                '是',
                '我',
                '第',
                '一',
                '次',
                '来',
                '上',
                '海',
                '旅',
                '游',
                '。',
            ],
        )

    def test_mixed_english_chinese(self):
        self.assertEqual(split_hanzi('Brian的'), ['Brian', '的'])
