from . import ChineseTests


# consumers: colorize
class RubyTests(ChineseTests):
    def test_ruby(self):
        from chinese.edit_functions import ruby
        self.assertEqual(ruby('你', 'Pinyin'), ['你[nǐ]'])
        self.assertEqual(
            ruby('图书馆', 'Pinyin'),
            ['图[tú]', '书[shū]', '馆[guǎn]']
        )

    def test_ruby_top(self):
        from chinese.ruby import ruby_top
        self.assertEqual(ruby_top('汉[hàn]字[zì]'), 'hàn zì ')

    def test_ruby_bottom(self):
        from chinese.ruby import ruby_bottom
        self.assertEqual(ruby_bottom('汉[hàn]字[zì]'), '汉 字 ')
