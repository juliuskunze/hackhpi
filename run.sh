#!/usr/bin/env bash
alias python=/home/julius/.local/bin/python
export PATH=/home/julius/.local/bin:$PATH
cd /home/julius/prj/tensorflow-models/syntaxnet/
syntaxnet/demo.sh < /home/julius/prj/hackhpi/data/input.txt