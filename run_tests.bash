#!/usr/bin/env bash
set -eu -o pipefail

if [[ "${1:-}" == '--with-random' ]] ; then
  export WITH_RANDOM=true
  python -m unittest discover --failfast .
else
  python -m unittest discover .
fi


