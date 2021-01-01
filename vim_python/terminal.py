
# Launch the vim in terminal mode, like the vim
# So we can test if it's the correct usage.
from curses import wrapper
import vim
import textwrap

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

    stdscr.leaveok(False)
    stdscr.refresh()

    stdscr.move(pos_y, pos_x)

  def start(self, stdscr):
    stdscr.clear()
    k = ''

    while True:
      self._refresh_state(stdscr, k)

      k = stdscr.getkey()
      if k == 'e':
        break
      if k in 'hjkl$0':
        self._vim.key_stroke(k)



#  while True:
#
#    cur_state_str = str(state) + '\n' + f'({cur_pos_x}, {cur_pos_y})   '
#    stdscr.leaveok(False)
#  
#    stdscr.addstr(0, 0, cur_state_str) 
#    stdscr.refresh()
#
#    cur_pos_y = cur_pos_y % h
#    cur_pos_x = cur_pos_x % w
#    sol_pos = board.SolPos(sol_x=cur_pos_x, sol_y=cur_pos_y)
#
#    win_pos_y = cur_pos_y * 2 + 1
#    win_pos_x = cur_pos_x * 2 + 1
#  
#    stdscr.move(win_pos_y, win_pos_x)
#
#    c = stdscr.getch()
#    if c == ord('e'):
#        break
#    if c == ord('j') or c == curses.KEY_DOWN: # down
#      cur_pos_y += 1
#    if c == ord('k') or c == curses.KEY_UP: # up
#      cur_pos_y -= 1
#    if c == ord('h') or c == curses.KEY_LEFT: # left
#      cur_pos_x -= 1
#    if c == ord('l') or c == curses.KEY_RIGHT: # right
#      cur_pos_x += 1
#    if c == ord('s'):
#      solvers.all_solvers(state)
#    if c == ord(' '):
#      existing_val = state.get_sol(sol_pos)
#      new_val = existing_val.loop_forward()
#      state.set_sol(sol_pos, new_val)
#      if state.is_solved():
#        break
#    if c == curses.KEY_ENTER:
#      existing_val = state.get_sol(sol_pos)
#      new_val = existing_val.loop_backward()
#      state.set_sol(sol_pos, new_val)
#      if state.is_solved():
#        break
#
#



def main():
  text = textwrap.dedent("""
    Lorem ipsum dolor sit amet
    Curabitur sapien neque
    id nisl. Fusce id diam id
    vitae mi non orci ultricies
  """)
  text = '\n'.join(text.split('\n')[1:-1])
  vim_instance = vim.VimPython(text)

  t = VimTerminal(vim_instance)
  wrapper(t.start)

if __name__ == '__main__':
  main()


