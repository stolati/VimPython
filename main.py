import json
import pprint
import subprocess
import tempfile
from pathlib import Path

KEY_COMMAND = {
  'h' : 'LEFT_1',
  'j': 'DOWN_1',
  'k': 'UP_1',
  'l': 'RIGHT_1',
  'x': 'DELETE_CHAR_AT_POS',
}

SAVE_STATE_PATH = Path('./save_state.vim')

class VimExe:

  @staticmethod
  def act(buffer, actions):
    with tempfile.TemporaryDirectory() as tmp_path_str:
      tmp_path = Path(tmp_path_str)
      
      input_path = tmp_path / 'input.txt'
      command_path = tmp_path / 'commands.str'
      output_path = tmp_path / 'output.json'
      vim_code_path = tmp_path / 'save_state.vim'

      input_path.write_text(buffer)
      command_path.write_text(actions)
      vim_code_path.write_text(SAVE_STATE_PATH.read_text())

      cmd = [
        'vim',
        '+:source save_state.vim',
        f'+call ExecuteAndSave("input.txt", "commands.str")',
        '--not-a-term',
        '--noplugin'
      ]

      _ = subprocess.check_output(cmd, cwd = tmp_path_str)

      output_content = output_path.read_text()
      return json.loads(output_content)


class VimPython:

  @classmethod
  def act(cls, buffer, actions):
    vb = cls(buffer)
    vb.key_strokes(actions)
    return vb.show_state()

  def __init__(self, buffer):
    self._mode = 'NORMAL'
    self._buffer_lines = [list(l) for l in buffer.split('\n')]
    self._pos_x = 0
    self._pos_y = 0
    self._buffer_paste = ''
    self._executed_commands = []

  def to_dict(self):
    return {
      'buffer' : '\n'.join(''.join(l) for l in self._buffer_lines),
      'pos' : [self._pos_x, self._pos_y],
      'paste' : self._buffer_paste,
      'command' : ''.join(self._executed_commands)
    }
  
  def show_state(self):
    pprint.pprint(self.to_dict())

  def key_strokes(self, keys):
    # TODO : have a more complicated split system
    for key in keys:
      self.key_stroke(key)

  def key_stroke(self, key):
    command = KEY_COMMAND[key]
    if command == 'LEFT_1':
      self._pos_x -= 1 
    elif command == 'DOWN_1':
      self._pos_y += 1 
    elif command == 'UP_1':
      self._pos_y -= 1 
    elif command == 'RIGHT_1':
      self._pos_x += 1 
    elif command == 'DELETE_CHAR_AT_POS':
      self._buffer_paste = self._buffer_lines[self._pos_y].pop(self._pos_x)
    else:
      raise NotImplementedError(f'{key} => {command}')

if __name__ == '__main__':
  print('hello world')

  text = open('short_lorum.txt').read()
  actions = 'jlx'

  pd = VimPython.act(text, actions)
  pprint.pprint(pd)

  ed = VimExe.act(text, actions)
  pprint.pprint(ed)

