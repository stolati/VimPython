
# Launch the vim in terminal mode, like the vim
# So we can test if it's the correct usage.
from curses import wrapper
import textwrap

from vim_python import vim

class VimTerminal:

  def __init__(self, vim_instance):
    self._vim = vim_instance
  
  def _refresh_state(self, stdscr, status=None):
    stdscr.clear()

    buffer = self._vim.get_buffer()
    pos_x, pos_y = self._vim.get_cursor_pos()

    stdscr.addstr(0, 0, buffer)

    if status:
      screen_rows, screen_cols = stdscr.getmaxyx()
      status = status.ljust(screen_cols-1, ' ')
      stdscr.addstr(screen_rows-2, 1, status)

    stdscr.refresh()

    stdscr.move(pos_y, pos_x)

  def start(self, stdscr):
    stdscr.clear()
    k = ''

    while True:
      self._refresh_state(stdscr, k)

      k = stdscr.getkey()
      if k in 'Zz':
        break
      if k in 'hjkl$0':
        self._vim.key_stroke(k)


def main():
  text = textwrap.dedent("""
    Lorem ipsum dolor sit amet
    Curabitur sapien neque

    id nisl. Fusce id diam id
    -
    vitae mi non orci ultricies
  """)
  text = '\n'.join(text.split('\n')[1:-1])
  vim_instance = vim.VimPython(text)

  t = VimTerminal(vim_instance)
  wrapper(t.start)

if __name__ == '__main__':
  main()


