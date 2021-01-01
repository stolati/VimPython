
import pprint
import keystrokes

class VimPython:

  @classmethod
  def act(cls, buffer, actions):
    vb = cls(buffer)
    vb.key_strokes(actions)
    return vb.to_dict()

  def __init__(self, buffer = ''):
    self._mode = 'NORMAL'
    self._buffer_lines = [list(l) for l in buffer.split('\n')]
    # Cursor info
    self._col = 1
    self._lnum = 1
    self._cursor_want = 1

    self._buffer_paste = ''
    self._executed_commands = []

  def to_dict(self):
    return {
      'output' : [''.join(l) for l in self._buffer_lines],
      'paste' : self._buffer_paste,
      'command' : ''.join(self._executed_commands),
      'cursor' : {
        'bufnum': 0, # buffers not handled yet
        'col': self._col,
        'lnum': self._lnum,
        'curswant': self._cursor_want,
        'off': 0, # I don't understand what it's for
      },
      'search': '',
    }
  
  def get_buffer(self):
    return '\n'.join([''.join(l) for l in self._buffer_lines])

  def get_cursor_pos(self):
    return (self._col -1 , self._lnum-1)
  
  def show_state(self):
    pprint.pprint(self.to_dict())

  def key_strokes(self, keys):
    # TODO : have a more complicated split system
    for key in keys:
      self.key_stroke(key)

  def key_stroke(self, key):
    self._executed_commands.append(key)
    command = keystrokes.KEYSTROKE_REVERSE[key]
    
    if command == 'LEFT_1':
      self._move_left()
    elif command == 'DOWN_1':
      self._move_down()
    elif command == 'UP_1':
      self._move_up()
    elif command == 'RIGHT_1':
      self._move_right()
    elif command == 'DELETE_CHAR_AT_POS':
      self._delete_char_at_pos()
    elif command == 'END_OF_LINE':
      self._end_of_line()
    elif command == 'BEGINNING_OF_LINE':
      self._beginning_of_line()
    else:
      raise NotImplementedError(f'{key} => {command}')
  
  @property
  def _cur_line_len(self):
    return len(self._buffer_lines[self._lnum-1])
  
  def _move_down(self):
    # Going over the number of lines
    if self._lnum >=len(self._buffer_lines):
      return
    self._lnum += 1

    self._col = min(self._cursor_want, self._cur_line_len)
 
  def _move_up(self):
    if self._lnum == 1:
      return
    self._lnum -= 1

    self._col = min(self._cursor_want, self._cur_line_len)
  
  def _move_right(self):
    if self._col >= self._cur_line_len:
      return
    self._col += 1 
    self._cursor_want = self._col

  def _move_left(self):
    if self._col == 1:
      return
    self._col -= 1 
    self._cursor_want = self._col
  
  def _delete_char_at_pos():
    pass

  def _end_of_line(self):
    self._col = self._cur_line_len
    self._cursor_want = 2147483647 # Extracted from vim

  def _beginning_of_line(self):
    self._col = 1
    self._cursor_want = 1