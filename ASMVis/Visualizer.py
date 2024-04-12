import Grammar as grm

"""
Author: Efren Haskell
Last Update: 4/8/2024
Visualizer class handles tokenization and high-level parsing
"""

spec_tokens = {"[", "]", "=", "$", "@", ",", " ", "\t", "\n"}
ignore = {" ", "\t", "\n"} # skip whitespace
file_nm = "" # global variable for file name


def start(emul) -> tuple[str, list[list[str]]]:
    """Main entry point for Visualizer
    returns tuple[str, list[list[str]]]

        - Handles high-level parsing, tokenization and lexical analysis of file contents
        - Files should be UTF-8 encoded
        - Errors handled and returned as strings
            - Second return value defaults to empty list when an error occurs
    """
    grm.labels = set()
    line_index: int = 1
    lines: list[str] = []
    with open(file_nm, 'r') as file:
        line: str = file.readline()
        while line != '':
            tokens: list[str] = tokenize(line+" ")
            if len(tokens) > 0:
                t_types: list[str] = []
                try:
                    t_types = parse(tokens, line_index)
                except Exception as e:
                    grm.labels = set()
                    return e, []
                temp = None
                emul.encode_skel(tokens, t_types, line_index)
                line_index += 1
                lines.append(tokens)
            line = file.readline()
        if t_types[-1] != "halt":
            return f"Error: line {line_index} -> All programs must end with a halt instruction", []
    return "Looks good! No syntax errors found!", lines


def tokenize(line: str) -> list[str]:
    """Tokenization method for token sets
    returns list[str]
        - Breaks tokens on spec_tokens
        - Non-ignore spec_tokens are added individually
    """
    tokens: list[str] = []
    long_token: str = ""
    for char in line:
        if char in spec_tokens:
            if long_token != "":
                tokens.append(long_token)
                long_token = ""
            if char in ignore:
                continue
            tokens.append(char)
        else:
            long_token += char
    return tokens


def parse(tokens: list[str], line_index: int) -> list[str]:
    """Parse method for running low-level grammar parse methods"""
    grm.line_tokens = tokens
    return grm.hash_parse(line_index, 0)
