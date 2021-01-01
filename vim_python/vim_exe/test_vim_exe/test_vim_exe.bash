#!/usr/bin/env bash
set -eu -o pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Test the vim command inside a bash command
command="${1:-jdd}"

tmp_dir="$(mktemp -d)"

cp "$DIR"/lorum.txt "$tmp_dir"/input.txt
cp "$DIR"/../save_state.vim "$tmp_dir"/save_state.vim
echo "$command" > "$tmp_dir"/commands.str

pushd "$tmp_dir"
vim \
  +':source save_state.vim' \
  +'call ExecuteAndSave("input.txt", "commands.str")' \
  --not-a-term \
  --noplugin | cat `#To force non-terminal`
popd

clear
jq . "$tmp_dir"/output.json

rm -rf "$tmp_dir"

# Should return something like : 
#{
#  "output": [
#    "Lorem ipsum dolor sit amet",
#    "id nisl. Fusce id diam id",
#    "vitae mi non orci ultricies"
#  ],
#  "cursor": {
#    "lnum": 2,
#    "bufnum": 0,
#    "col": 1,
#    "off": 0,
#    "curswant": 1
#  },
#  "paste": "Curabitur sapien neque\n",
#  "search": "",
#  "command": "jdd"
#}

