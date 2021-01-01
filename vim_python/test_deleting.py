
import unittest

from vim_python.test_data import test_helper

class TestDeleting(test_helper.VimTester):

    def test_x(self):
      self.assert_correct('x')
      self.assert_correct('$x')
      self.assert_correct('$xx')
      self.assert_correct('jx$x')

      self.assert_correct('x' * 20)
      self.assert_correct('x' * 40)

      self.assert_correct('$jjx')

      self.assert_correct('xjjx')

    @test_helper.skip_random
    def test_random(self):
      self.assert_random('hjkl$0x')

  # TODO test line with no characters
  # TODO test with last line ending in 0 or 1

if __name__ == '__main__':
    unittest.main()
