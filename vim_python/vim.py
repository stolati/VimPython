import pprint
from collections import namedtuple

from vim_python import keystrokes

class CursorData(namedtuple('CursorData', ['col', 'lnum', 'want'])):

  END_OF_LINE_MAX = 2147483647

  @classmethod
  def default(cls):
    return cls(1, 1, 1)

  def to_json(self):
    return {
      'bufnum': 0, # buffers not handled yet
      'col': self.col,
      'lnum': self.lnum,
      'curswant': self.want,
      'off': 0, # I don't understand what it's for
    }
  
  def get_cursor_pos(self):
    # TODO : change to avoid -1 here, the terminal should do it
    return (self.col -1 , self.lnum-1)
  
  def to_new(self, col=None, lnum=None, want=None):
    col = self.col if col is None else col
    lnum = self.lnum if lnum is None else lnum
    want = self.want if want is None else want
    return CursorData(col, lnum, want)


class VimPython:

  @classmethod
  def act(cls, buffer, actions):
    vb = cls(buffer)
    vb.key_strokes(actions)
    return vb.to_dict()

  def __init__(self, buffer = ''):
    self._mode = 'NORMAL'
    self._buffer_lines = [list(l) for l in buffer.split('\n')]

    self._cursor = CursorData.default()

    self._buffer_paste = ''
    self._executed_commands = []

    self._current_command = []

  def to_dict(self):
    return {
      'output' : [''.join(l) for l in self._buffer_lines],
      'paste' : self._buffer_paste,
      'command' : ''.join(self._executed_commands),
      'cursor' : self._cursor.to_json(),
      'search': '',
    }
  
  def get_buffer(self):
    return '\n'.join([''.join(l) for l in self._buffer_lines])

  def get_cursor_pos(self):
    return self._cursor.get_cursor_pos()
  
  def show_state(self):
    pprint.pprint(self.to_dict())

  def key_strokes(self, keys):
    # TODO : have a more complicated split system
    for key in keys:
      self.key_stroke(key)

  def key_stroke(self, key):
    self._executed_commands.append(key)
    command = keystrokes.KEYSTROKE_REVERSE[key]
    method = getattr(self, f'_command_{command.lower()}')
    method()
  
  def _get_line_len(self, lnum=None, min_1=True):
    lnum = self._cursor.lnum if lnum is None else lnum
    line_len = len(self._buffer_lines[lnum-1])
    if min_1:
      line_len = max(line_len, 1)
    return line_len
  
  def _command_move_down_1(self): # j
    new_lnum = self._cursor.lnum + 1
    # Going over the number of lines
    if new_lnum > len(self._buffer_lines):
      return
    self._cursor = self._cursor.to_new(
      lnum = new_lnum,
      col = min(self._cursor.want, self._get_line_len(new_lnum)),
    )
 
  def _command_move_up_1(self): # k
    new_lnum = self._cursor.lnum - 1
    if new_lnum == 0:
      return
    self._cursor = self._cursor.to_new(
      lnum = new_lnum,
      col = min(self._cursor.want, self._get_line_len(new_lnum)),
    )
  
  def _command_move_right_1(self): # l
    new_col = self._cursor.col + 1
    if new_col > self._get_line_len():
      return
    self._cursor = self._cursor.to_new(
      col= new_col,
      want = new_col,
    )

  def _command_move_left_1(self): # h
    new_col = self._cursor.col - 1
    if new_col == 0:
      return
    self._cursor = self._cursor.to_new(
      col= new_col,
      want = new_col,
    )

  def _command_move_end_of_line(self): # $
    self._cursor = self._cursor.to_new(
      col=self._get_line_len(),
      want=CursorData.END_OF_LINE_MAX,
    )

  def _command_move_beginning_of_line(self):
    self._cursor = self._cursor.to_new(col=1, want=1)

  def _command_delete_char_at_pos(self):
    line = self._buffer_lines[self._cursor.lnum-1]
    line_len = len(line)
    if line_len == 0:
      self._cursor = self._cursor.to_new(want=1)    
      return
    self._buffer_paste = line.pop(self._cursor.col-1)
    new_col = min(self._cursor.want, self._get_line_len())
    self._cursor = self._cursor.to_new(
      col = new_col,
      want = new_col,
    )    



    