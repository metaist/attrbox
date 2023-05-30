"""Pythonic command-line interface parser that will make you smile.

 * http://docopt.org
 * Repository and issue-tracker: https://github.com/docopt/docopt
 * Licensed under terms of MIT license (see LICENSE-MIT)
 * Copyright (c) 2013 Vladimir Keleshev, vladimir@keleshev.com

"""

# native
from __future__ import annotations
from typing import Dict
from typing import List
from typing import Optional
from typing import Sequence
from typing import Tuple
from typing import Union
from typing import Type
import re
import sys


__all__ = ["docopt"]
__version__ = "0.6.2"


class DocoptLanguageError(Exception):

    """Error in construction of usage-message by developer."""


class DocoptExit(SystemExit):

    """Exit in case user invoked program with incorrect arguments."""

    usage: str = ""

    def __init__(self, message: str = ""):
        SystemExit.__init__(self, (message + "\n" + self.usage).strip())


class Pattern(object):
    def __eq__(self, other: Pattern):
        return repr(self) == repr(other)

    def __hash__(self):
        return hash(repr(self))

    def fix(self):
        self.fix_identities()
        self.fix_repeating_arguments()
        return self

    def fix_identities(self, uniq=None):
        """Make pattern-tree tips point to same object if they are equal."""
        if not hasattr(self, "children"):
            return self

        uniq = list(set(self.flat())) if uniq is None else uniq
        for i, child in enumerate(self.children):
            if not hasattr(child, "children"):
                assert child in uniq
                self.children[i] = uniq[uniq.index(child)]
            else:
                child.fix_identities(uniq)

    def fix_repeating_arguments(self):
        """Fix elements that should accumulate/increment values."""
        either = [list(child.children) for child in transform(self).children]
        for case in either:
            for e in [child for child in case if case.count(child) > 1]:
                if type(e) is Argument or type(e) is Option and e.argcount:
                    if e.value is None:
                        e.value = []
                    elif type(e.value) is not list:
                        e.value = e.value.split()
                if type(e) is Command or type(e) is Option and e.argcount == 0:
                    e.value = 0
        return self


def transform(pattern):
    """Expand pattern into an (almost) equivalent one, but with single Either.

    Example: ((-a | -b) (-c | -d)) => (-a -c | -a -d | -b -c | -b -d)
    Quirks: [-a] => (-a), (-a...) => (-a -a)

    """
    result = []
    groups = [[pattern]]
    while groups:
        children = groups.pop(0)
        parents = [Required, Elective, OptionsShortcut, Either, OneOrMore]
        if any(t in map(type, children) for t in parents):
            child = [c for c in children if type(c) in parents][0]
            children.remove(child)
            if type(child) is Either:
                for c in child.children:
                    groups.append([c] + children)
            elif type(child) is OneOrMore:
                groups.append(child.children * 2 + children)
            else:
                groups.append(child.children + children)
        else:
            result.append(children)
    return Either(*[Required(*e) for e in result])


class LeafPattern(Pattern):

    """Leaf/terminal node of a pattern tree."""

    def __init__(self, name: Optional[str], value: Optional[str] = None):
        self.name, self.value = name, value

    def __repr__(self) -> str:
        return "%s(%r, %r)" % (self.__class__.__name__, self.name, self.value)

    def flat(self, *types: Type[Pattern]) -> Union[Sequence[LeafPattern], bool]:
        return [self] if not types or type(self) in types else []

    def match(self, left, collected=None):
        collected = [] if collected is None else collected
        pos, match = self.single_match(left)
        if match is None:
            return False, left, collected
        left_ = left[:pos] + left[pos + 1 :]
        same_name = [a for a in collected if a.name == self.name]
        if type(self.value) in (int, list):
            if type(self.value) is int:
                increment = 1
            else:
                increment = [match.value] if type(match.value) is str else match.value
            if not same_name:
                match.value = increment
                return True, left_, collected + [match]
            same_name[0].value += increment
            return True, left_, collected
        return True, left_, collected + [match]


class BranchPattern(Pattern):

    """Branch/inner node of a pattern tree."""

    def __init__(self, *children: Pattern):
        self.children = list(children)

    def __repr__(self) -> str:
        return "%s(%s)" % (
            self.__class__.__name__,
            ", ".join(repr(a) for a in self.children),
        )

    def flat(self, *types: Type[Pattern]) -> Sequence[Pattern]:
        if type(self) in types:
            return [self]
        return sum([child.flat(*types) for child in self.children], [])


class Argument(LeafPattern):
    def single_match(
        self, left: Sequence[Pattern]
    ) -> Tuple[Optional[int], Optional[Argument]]:
        for n, pattern in enumerate(left):
            if type(pattern) is Argument:
                return n, Argument(self.name, pattern.value)
        return None, None

    @classmethod
    def parse(cls, source: str) -> Argument:
        name = re.findall("(<\S*?>)", source)[0]
        value = re.findall("\[default: (.*)\]", source, flags=re.I)
        return cls(name, value[0] if value else None)


class Command(Argument):
    def __init__(self, name: Optional[str], value: bool = False):
        self.name, self.value = name, value

    def single_match(self, left) -> Tuple[Optional[int], Optional[Pattern]]:
        for n, pattern in enumerate(left):
            if type(pattern) is Argument:
                if pattern.value == self.name:
                    return n, Command(self.name, True)
                else:
                    break
        return None, None


class Option(LeafPattern):
    def __init__(self, short=None, long=None, argcount=0, value=False):
        assert argcount in (0, 1)
        self.short, self.long, self.argcount = short, long, argcount
        self.value = None if value is False and argcount else value

    @classmethod
    def parse(cls, option_description: str) -> Option:
        short, long, argcount, value = None, None, 0, False
        options, _, description = option_description.strip().partition("  ")
        options = options.replace(",", " ").replace("=", " ")
        for s in options.split():
            if s.startswith("--"):
                long = s
            elif s.startswith("-"):
                short = s
            else:
                argcount = 1
        if argcount:
            matched = re.findall("\[default: (.*)\]", description, flags=re.I)
            value = matched[0] if matched else None
        return cls(short, long, argcount, value)

    def single_match(self, left: Sequence[Pattern]) -> Tuple[None, None]:
        for n, pattern in enumerate(left):
            if self.name == pattern.name:
                return n, pattern
        return None, None

    @property
    def name(self):
        return self.long or self.short

    def __repr__(self):
        return "Option(%r, %r, %r, %r)" % (
            self.short,
            self.long,
            self.argcount,
            self.value,
        )


class Required(BranchPattern):
    def match(self, left, collected=None):
        collected = [] if collected is None else collected
        left_ = left
        collected_ = collected
        for pattern in self.children:
            matched, left_, collected_ = pattern.match(left_, collected_)
            if not matched:
                return False, left, collected
        return True, left_, collected_


class Elective(BranchPattern):
    def match(self, left, collected=None):
        collected = [] if collected is None else collected
        for pattern in self.children:
            m, left, collected = pattern.match(left, collected)
        return True, left, collected


class OptionsShortcut(Elective):

    """Marker/placeholder for [options] shortcut."""


class OneOrMore(BranchPattern):
    def match(self, left, collected=None):
        assert len(self.children) == 1
        collected = [] if collected is None else collected
        left_ = left
        c = collected
        l_ = None
        matched = True
        times = 0
        while matched:
            # could it be that something didn't match but changed l or c?
            matched, left_, c = self.children[0].match(left_, c)
            times += 1 if matched else 0
            if l_ == left_:
                break
            l_ = left_
        if times >= 1:
            return True, left_, c
        return False, left, collected


class Either(BranchPattern):
    def match(self, left, collected=None):
        collected = [] if collected is None else collected
        outcomes = []
        for pattern in self.children:
            matched, _, _ = outcome = pattern.match(left, collected)
            if matched:
                outcomes.append(outcome)
        if outcomes:
            return min(outcomes, key=lambda outcome: len(outcome[1]))
        return False, left, collected


class Tokens(list):
    def __init__(self, source: Union[str, Sequence[str]], error=DocoptExit):
        self += source.split() if hasattr(source, "split") else source
        self.error = error

    @staticmethod
    def from_pattern(source: str):
        source = re.sub(r"([\[\]\(\)\|]|\.\.\.)", r" \1 ", source)
        source = [s for s in re.split("\s+|(\S*<.*?>)", source) if s]
        return Tokens(source, error=DocoptLanguageError)

    def move(self) -> Optional[str]:
        return self.pop(0) if len(self) else None

    def current(self) -> Optional[str]:
        return self[0] if len(self) else None


def parse_long(tokens: Tokens, options: Sequence[Option]) -> Sequence[Option]:
    """long ::= '--' chars [ ( ' ' | '=' ) chars ] ;"""
    long, eq, value = tokens.move().partition("=")
    assert long.startswith("--")
    value = None if eq == value == "" else value
    similar = [o for o in options if o.long == long]
    if tokens.error is DocoptExit and similar == []:  # if no exact match
        similar = [o for o in options if o.long and o.long.startswith(long)]
    if len(similar) > 1:  # might be simply specified ambiguously 2+ times?
        raise tokens.error(
            "%s is not a unique prefix: %s?"
            % (long, ", ".join(o.long for o in similar))
        )
    elif len(similar) < 1:
        argcount = 1 if eq == "=" else 0
        o = Option(None, long, argcount)
        options.append(o)
        if tokens.error is DocoptExit:
            o = Option(None, long, argcount, value if argcount else True)
    else:
        o = Option(
            similar[0].short, similar[0].long, similar[0].argcount, similar[0].value
        )
        if o.argcount == 0:
            if value is not None:
                raise tokens.error("%s must not have an argument" % o.long)
        else:
            if value is None:
                if tokens.current() in [None, "--"]:
                    raise tokens.error("%s requires argument" % o.long)
                value = tokens.move()
        if tokens.error is DocoptExit:
            o.value = value if value is not None else True
    return [o]


def parse_shorts(tokens: Tokens, options: Sequence[Option]) -> Sequence[Option]:
    """shorts ::= '-' ( chars )* [ [ ' ' ] chars ] ;"""
    token = tokens.move()
    assert token.startswith("-") and not token.startswith("--")
    left = token.lstrip("-")
    parsed = []
    while left != "":
        short, left = "-" + left[0], left[1:]
        similar = [o for o in options if o.short == short]
        if len(similar) > 1:
            raise tokens.error(
                "%s is specified ambiguously %d times" % (short, len(similar))
            )
        elif len(similar) < 1:
            o = Option(short, None, 0)
            options.append(o)
            if tokens.error is DocoptExit:
                o = Option(short, None, 0, True)
        else:  # why copying is necessary here?
            o = Option(short, similar[0].long, similar[0].argcount, similar[0].value)
            value = None
            if o.argcount != 0:
                if left == "":
                    if tokens.current() in [None, "--"]:
                        raise tokens.error("%s requires argument" % short)
                    value = tokens.move()
                else:
                    value = left
                    left = ""
            if tokens.error is DocoptExit:
                o.value = value if value is not None else True
        parsed.append(o)
    return parsed


def parse_pattern(source: str, options: Sequence[Option]):
    tokens = Tokens.from_pattern(source)
    result = parse_expr(tokens, options)
    if tokens.current() is not None:
        raise tokens.error("unexpected ending: %r" % " ".join(tokens))
    return Required(*result)


def parse_expr(tokens: Tokens, options: Sequence[Option]):
    """expr ::= seq ( '|' seq )* ;"""
    seq = parse_seq(tokens, options)
    if tokens.current() != "|":
        return seq
    result = [Required(*seq)] if len(seq) > 1 else seq
    while tokens.current() == "|":
        tokens.move()
        seq = parse_seq(tokens, options)
        result += [Required(*seq)] if len(seq) > 1 else seq
    return [Either(*result)] if len(result) > 1 else result


def parse_seq(tokens: Tokens, options: Sequence[Option]):
    """seq ::= ( atom [ '...' ] )* ;"""
    result = []
    while tokens.current() not in [None, "]", ")", "|"]:
        atom = parse_atom(tokens, options)
        if tokens.current() == "...":
            atom = [OneOrMore(*atom)]
            tokens.move()
        result += atom
    return result


def parse_atom(tokens: Tokens, options: Sequence[Option]) -> Sequence[Pattern]:
    """atom ::= '(' expr ')' | '[' expr ']' | 'options'
    | long | shorts | argument | command ;
    """
    token = tokens.current()
    result = []
    if token is None:
        return result

    if token in "([":
        tokens.move()
        matching, pattern = {"(": [")", Required], "[": ["]", Elective]}[token]
        result: Union[Required, Elective] = pattern(*parse_expr(tokens, options))
        if tokens.move() != matching:
            raise tokens.error("unmatched '%s'" % token)
        return [result]
    elif token == "options":
        tokens.move()
        return [OptionsShortcut()]
    elif token.startswith("--") and token != "--":
        return parse_long(tokens, options)
    elif token.startswith("-") and token not in ("-", "--"):
        return parse_shorts(tokens, options)
    elif token.startswith("<") and token.endswith(">") or token.isupper():
        return [Argument(tokens.move())]
    else:
        return [Command(tokens.move())]


def parse_argv(
    tokens: Tokens, options: List[Option], options_first: bool = False
) -> Sequence[LeafPattern]:
    """Parse command-line argument vector.

    If options_first:
        argv ::= [ long | shorts ]* [ argument ]* [ '--' [ argument ]* ] ;
    else:
        argv ::= [ long | shorts | argument ]* [ '--' [ argument ]* ] ;

    """
    parsed: List[LeafPattern] = []
    current = tokens.current()
    while current is not None:
        if current == "--":
            return parsed + [Argument(None, v) for v in tokens]
        elif current.startswith("--"):
            parsed += parse_long(tokens, options)
        elif current.startswith("-") and current != "-":
            parsed += parse_shorts(tokens, options)
        elif options_first:
            return parsed + [Argument(None, v) for v in tokens]
        else:
            parsed.append(Argument(None, tokens.move()))
        current = tokens.current()
    return parsed


def parse_defaults(doc: str) -> Sequence[Option]:
    defaults = []
    for s in parse_section("options:", doc):
        # FIXME corner case "bla: options: --foo"
        _, _, s = s.partition(":")  # get rid of "options:"
        split = re.split("\n[ \t]*(-\S+?)", "\n" + s)[1:]
        split = [s1 + s2 for s1, s2 in zip(split[::2], split[1::2])]
        options = [Option.parse(s) for s in split if s.startswith("-")]
        defaults += options
    return defaults


def parse_section(name: str, source: str) -> Sequence[str]:
    pattern = re.compile(
        "^([^\n]*" + name + "[^\n]*\n?(?:[ \t].*?(?:\n|$))*)",
        re.IGNORECASE | re.MULTILINE,
    )
    return [s.strip() for s in pattern.findall(source)]


def formal_usage(section: str) -> str:
    _, _, section = section.partition(":")  # drop "usage:"
    pu = section.split()
    return "( " + " ".join(") | (" if s == pu[0] else s for s in pu[1:]) + " )"


def extras(
    help: bool, version: Optional[str], options: Sequence[LeafPattern], doc: str
) -> None:
    if help and any((o.name in ("-h", "--help")) and o.value for o in options):
        print(doc.strip("\n"))
        sys.exit()
    if version and any(o.name == "--version" and o.value for o in options):
        print(version)
        sys.exit()


class DocoptDict(Dict[str, Union[bool, str]]):
    def __repr__(self) -> str:
        return "{%s}" % ",\n ".join("%r: %r" % i for i in sorted(self.items()))


def docopt(
    doc: str,
    argv: Optional[Sequence[str]] = None,
    help: bool = True,
    version: Optional[str] = None,
    options_first: bool = False,
) -> DocoptDict:
    """Parse `argv` based on command-line interface described in `doc`.

    `docopt` creates your command-line interface based on its
    description that you pass as `doc`. Such description can contain
    --options, <positional-argument>, commands, which could be
    [optional], (required), (mutually | exclusive) or repeated...

    Parameters
    ----------
    doc : str
        Description of your command-line interface.
    argv : list of str, optional
        Argument vector to be parsed. sys.argv[1:] is used if not
        provided.
    help : bool (default: True)
        Set to False to disable automatic help on -h or --help
        options.
    version : any object
        If passed, the object will be printed if --version is in
        `argv`.
    options_first : bool (default: False)
        Set to True to require options precede positional arguments,
        i.e. to forbid options and positional arguments intermix.

    Returns
    -------
    args : dict
        A dictionary, where keys are names of command-line elements
        such as e.g. "--verbose" and "<path>", and values are the
        parsed values of those elements.

    Example
    -------
    >>> from docopt import docopt
    >>> doc = '''
    ... Usage:
    ...     my_program tcp <host> <port> [--timeout=<seconds>]
    ...     my_program serial <port> [--baud=<n>] [--timeout=<seconds>]
    ...     my_program (-h | --help | --version)
    ...
    ... Options:
    ...     -h, --help  Show this screen and exit.
    ...     --baud=<n>  Baudrate [default: 9600]
    ... '''
    >>> argv = ['tcp', '127.0.0.1', '80', '--timeout', '30']
    >>> docopt(doc, argv)
    {'--baud': '9600',
     '--help': False,
     '--timeout': '30',
     '--version': False,
     '<host>': '127.0.0.1',
     '<port>': '80',
     'serial': False,
     'tcp': True}

    See also
    --------
    * For video introduction see http://docopt.org
    * Full documentation is available in README.rst as well as online
      at https://github.com/docopt/docopt#readme

    """
    argv_: Sequence[str] = sys.argv[1:] if argv is None else argv

    usage_sections = parse_section("usage:", doc)
    if len(usage_sections) == 0:
        raise DocoptLanguageError('"usage:" (case-insensitive) not found.')
    if len(usage_sections) > 1:
        raise DocoptLanguageError('More than one "usage:" (case-insensitive).')
    DocoptExit.usage = usage_sections[0]

    options = parse_defaults(doc)
    pattern = parse_pattern(formal_usage(DocoptExit.usage), options)
    # [default] syntax for argument is disabled
    # for a in pattern.flat(Argument):
    #    same_name = [d for d in arguments if d.name == a.name]
    #    if same_name:
    #        a.value = same_name[0].value
    args = parse_argv(Tokens(argv_), list(options), options_first)
    pattern_options = set(pattern.flat(Option))
    for options_shortcut in pattern.flat(OptionsShortcut):
        doc_options = parse_defaults(doc)
        options_shortcut.children = list(set(doc_options) - pattern_options)
        # if any_options:
        #    options_shortcut.children += [Option(o.short, o.long, o.argcount)
        #                    for o in argv if type(o) is Option]
    extras(help, version, args, doc)
    matched, left, collected = pattern.fix().match(argv_)
    if matched and left == []:  # better error message if left?
        return DocoptDict((a.name, a.value) for a in (pattern.flat() + collected))
    raise DocoptExit()
