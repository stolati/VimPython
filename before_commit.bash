#!/usr/bin/env bash
set -eux -o pipefail

autopep8 --recursive --in-place --verbose --aggressive .


