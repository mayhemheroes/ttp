#!/usr/bin/env python3

import atheris
import sys
import fuzz_helpers

with atheris.instrument_imports(include=['ttp']):
    import ttp

# Exceptions
from xml.etree.ElementTree import ParseError
import re

def TestOneInput(data):
    fdp = fuzz_helpers.EnhancedFuzzedDataProvider(data)
    try:
        parser = ttp.ttp(fdp.ConsumeRandomString(), fdp.ConsumeRandomString())
        parser.parse()
    except (ParseError, PermissionError, UnicodeDecodeError, SystemExit, re.error):
        return -1

def main():
    atheris.Setup(sys.argv, TestOneInput)
    atheris.Fuzz()


if __name__ == "__main__":
    main()
