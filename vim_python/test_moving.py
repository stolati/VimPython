import unittest
from test_data import test_helper

class TestMoving(test_helper.VimTester):

    def test_jklh(self):
      self.assert_correct('j')
      self.assert_correct('k')
      self.assert_correct('l')
      self.assert_correct('h')

if __name__ == '__main__':
    unittest.main()
