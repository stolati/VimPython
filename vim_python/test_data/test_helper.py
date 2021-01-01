import unittest
from pathlib import Path
import json
import random

import deepdiff
from progress.bar import Bar

from vim_python import vim
from vim_python.vim_exe import vim_exe

LORUM = (
  'Lorem ipsum dolor sit amet\n'
  'Curabitur sapien neque\n'
  '\n'
  'id nisl. Fusce id diam id\n'
  ' \n'
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

  def assert_correct(self, command, auto_save=True, force_vim_exe=False):
    actual = vim.VimPython.act(LORUM, command)
    expected = None
    if not force_vim_exe:
      expected = self._read_saved_data().get(command)

    if not expected:
      expected = vim_exe.VimExe.act(LORUM, command)
      if auto_save:
        self._write_saved_data(command, expected)
    
    self.assertEqual(expected, actual, deepdiff.DeepDiff(expected, actual))
  
  def assert_random(self, allowed_commands, number_loop=1000, size_commands=10):
    random.seed()
    bar = Bar('Testing random sequences', max=number_loop)
    for _ in range(number_loop):
      command = random.choices(allowed_commands, k=size_commands)
      self.assert_correct(''.join(command), auto_save=False, force_vim_exe=True)
      bar.next()
    bar.finish()
