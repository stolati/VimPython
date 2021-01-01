import unittest
import os

from vim_python.test_data import test_helper

class TestMoving(test_helper.VimTester):

    def test_jklh(self):
      self.assert_correct('j')
      self.assert_correct('k')
      self.assert_correct('l')
      self.assert_correct('h')
      self.assert_correct('$')
      self.assert_correct('0')
      self.assert_correct('$j')
      self.assert_correct('$hjj')
      self.assert_correct('$hl0hj00jh')
      self.assert_correct('$lll')

    @test_helper.skip_random
    def test_random(self):
      self.assert_random('hjkl$0')

  # TODO test line with no characters
  # TODO test with last line ending in 0 or 1

if __name__ == '__main__':
    unittest.main()
