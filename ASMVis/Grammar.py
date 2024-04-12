import re

"""
Author: Efren Haskell
Last Update: 4/8/2024
Grammar class handles low-level token parsing and error-handling
Defines the syntactic structure of MiniASM and token productions
"""


instructions: set[str] = {"load", "store", "read", "write"} 
arithmetic: dict[str,str] = {"add":"+", "sub":"-", "div":"/", "mul":"*"} 
increment: str = "inc"
branch: str = "br"
address_modes: dict[str,str] = {"$":"relative", "@":"indirect", "[":"index", "=":"immediate", "]":"index", ",":""}
branches: dict[str,str] = {"blt":"<", "bgt":">", "bleq":"<=", "bgeq":">=", "beq":"==", "bneq":"!="}
labels: set[str] = set()

productions: dict[str,list[str]] = {
    "label": ["production"],
    "load": ["reg", ",", "address"],
    "store": ["reg", ",", "address1"],
    "read": ["reg", ",", "address2"],
    "write": ["reg", ",", "address2"],
    "arithmetic": ["reg", ",", "reg"],
    "inc": ["reg"],
    "br": ["id"],
    "branch": ["reg", ",", "reg", ",", "id"],
    "$": ["var"],
    "@": ["var"],
    "=": ["num"],
    "[": ["var", ",", "reg", "]"],
    "skip":[],
    "halt":[],
    "num": [],
    "reg": []
}

transitions: dict[str, set[str]] = {
    "production": {"skip", "load", "read", "write", "store", "arithmetic", "halt", "branch", "inc", "br"},
    "reg": {},
    "address": {"num", "reg", "$", "@", "[", "="},
    "address1": {"reg", "$", "["},
    "address2": {"num", "reg","["},
    ",": {},
    "]": {},
    "skip": {},
    "halt": {},
    "var": {"num", "reg"},
    "id": {},
    "num": {}
}


def follow_transition(non_terminal: str, token_index: int, line_index: int, t_types: list[str]):
    """The follow_transition method determines any possible transitions from a type determination
    """
    if token_index >= len(line_tokens):
        # Check that the number of tokens left in production does not exceed the length of user input
        raise Exception(f"Error:\nLine {line_index} -> Reached end of token sequence\nExpected \"{non_terminal}\"")
    token: str = line_tokens[token_index].lower()
    t_type: str = get_type(token)
    t_types.append(t_type)
    transition: set[str] = transitions[non_terminal]
    if len(transition) > 0:
        if t_type not in transition:
            raise Exception(f"Error\nLine {line_index} -> Got token: \"{token}\" of type: \"{t_type}\"\nExpected one of {transition}")
        next_t: str = t_type
        follow(next_t, line_index, token_index+1, t_types)
    else:
        if non_terminal != t_type:
            raise Exception(f"Error:\nLine {line_index} -> Got token: \"{token}\" of type: \"{t_type}\"\nExpected \"{non_terminal}\"")


def follow(non_term: str, line_index: int, token_index: int, t_types: list[str]):
    """The follow method follows a specific production, returning any possible transition tokens
    Production is determined as a dictionary value
    Calls follow_transition method which will determine the transitions possible from a production token
    """
    production: list[str] = productions[non_term]
    for non_terminal in production:
        follow_transition(non_terminal, token_index, line_index, t_types)
        token_index += 1


def hash_parse(line_index: int, token_index: int):
    """The hash_parse method acts as entry point for MiniASM parser
    Takes an int param line_index which is used for more descriptive exceptions and an int param
    token_index to keep track of the token being parsed
    raise Exception when a token should not begin a production
    """
    token: str = line_tokens[token_index].lower()
    t_types: list[str] = []
    t_type: str = get_type(token)
    t_types.append(t_type)
    if t_type != "label" and t_type not in transitions["production"]:
        raise Exception(f"Error:\nLine {line_index} -> Got token: \"{token}\"\nNot a valid start to a production")
    follow(t_type, line_index, token_index+1, t_types)
    return t_types


def get_type(token: str) -> str:
    """The get_type method determines the type of a specific token through regex matches and hash look-ups
    Takes a String param token and returns token type
    raises Exception when two different labels share the same name
    """
    if re.match(".+:$", token):
        if token in labels:
            raise Exception(f"Error:\nThe label \"{token}\" has already been defined elsewhere\nno two labels can have the same name")
        labels.add(token)
        return "label"
    elif re.match("^r[0-9]$|^r1[0-6]$", token):
        return "reg"
    elif re.match("^[0-9]+$", token):
        return "num"
    elif token in instructions:
        return token
    elif token in arithmetic:
        return "arithmetic"
    elif token in branches:
        return "branch"
    elif token in address_modes:
        return token
    elif token + ":" in labels:
        return "id"
    elif token == "br":
        return "br"
    elif token == "skip":
        return "skip"
    elif token == "halt":
        return "halt"
    elif token == "inc":
        return "inc"
    else:
        return "id"
