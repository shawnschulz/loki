#!/bin/bash
#
touch command_names.txt

echo $(compgen -c) >> command_names.txt
