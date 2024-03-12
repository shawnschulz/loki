#!/usr/bin/env

touch raw_man_pages.txt
touch raw_help_text.txt

cli_tools=$(compgen -c)

for cmd in ${cli_tools}; do
    $($cmd -h) >> raw_help_text.txt
    man "$cmd" >> raw_man_pages.txt
done

