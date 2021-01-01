from enum import Enum, unique

@unique
class KeyStroke(Enum):
  LEFT_1 = 'h'
  DOWN_1 = 'j'
  UP_1 = 'k'
  RIGHT_1 = 'l'
  DELETE_CHAR_AT_POS = 'x'

  ENTER = '\<CR>'
  ESCAPE = '\<ESC>'

KEYSTROKE_REVERSE = {
  e.value : e.name
  for e in KeyStroke
}

def get_next_command(s):
  findings = []
  for e in KeyStroke:
    if s.startswith(e.value):
      findings.append(e)
  if not findings:
    raise ValueError(f'Next command not found for : [{s}]')
  
  if len(findings) == 1:
    return findings[0], s[len(findings[0].value):]
  raise ValueError(f'Multiples values found for [{s}] : {findings}')


# \<C-w> => Ctrl w
#<BS>           Backspace
#<Tab>          Tab
#<CR>           Enter
#<Enter>        Enter
#<Return>       Enter
#<Esc>          Escape
#<Space>        Space
#<Up>           Up arrow
#<Down>         Down arrow
#<Left>         Left arrow
#<Right>        Right arrow
#<F1> - <F12>   Function keys 1 to 12
##1, #2..#9,#0  Function keys F1 to F9, F10
#<Insert>       Insert
#<Del>          Delete
#<Home>         Home
#<End>          End
#<PageUp>       Page-Up
#<PageDown>     Page-Down
#<bar>          the '|' character, which otherwise needs to be escaped '\|'