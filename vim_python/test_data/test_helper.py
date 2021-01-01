from vim_exe import vim_exe
import vim
import unittest
from pathlib import Path
import json
import deepdiff

LORUM = (
  'Lorem ipsum dolor sit amet\n'
  'Curabitur sapien neque\n'
  'id nisl. Fusce id diam id\n'
  'vitae mi non orci ultricies' # TODO add newline there
)

class VimTester(unittest.TestCase):

  @classmethod
  def _get_test_path(cls):
    name = cls.__name__
    return Path(__file__).parent / f'test_data_{name}.json'
  
  @classmethod
  def _read_saved_data(cls):
    test_path = cls._get_test_path()
    if not test_path.exists():
      return {}
    return json.loads(test_path.read_text())

  def _write_saved_data(cls, command, expected):
    saved_data = cls._read_saved_data()
    saved_data[command] = expected
    cls._get_test_path().write_text(
      json.dumps(saved_data, sort_keys=True, indent=4))

  def assert_correct(self, command, auto_save=True):
    print('testing correctness')
    actual = vim.VimPython.act(LORUM, command)
    expected = self._read_saved_data().get(command)

    if not expected:
      expected = vim_exe.VimExe.act(LORUM, command)
      if auto_save:
        self._write_saved_data(command, expected)
    
    self.assertEqual(expected, actual, deepdiff.DeepDiff(expected, actual))
  
  def assert_random(allowed_commands, number_loop=1000, size_commands=10):
    pass