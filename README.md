# CYK Parser

This is my implementation of a Cocke–Younger–Kasami (CYK) parser for a Natural Language Processing course. The program takes in a
Chomsky Normal Form grammar (see [sampleGrammar.cnf](./sampleGrammar.cnf)) and will prompt the user for sentences to parse. It will then output
all valid parses or say "NO VALID PARSES" if there are no valid parses. It can additionally display parse trees for improved readability.

## Usage

`
python3 cky_parser.py [Path to CNF grammar file]
`