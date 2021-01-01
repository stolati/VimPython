import json
import subprocess
import tempfile
from pathlib import Path

# TODO : replace with resource loading
SAVE_STATE_PATH = Path(__file__).parent / 'save_state.vim'

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
      json_res = json.loads(output_content)
      return json_res
