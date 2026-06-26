#!/usr/bin/env python3
"""Behavioral oracle (known-answer test) for ttp (Template Text Parser).

Exercises the SAME parsing pipeline the fuzzer drives — ttp(data, template).parse() ->
.result() — and ASSERTS the specific structured values ttp extracts from a known network-config
sample (mayhem/testsuite/seed.data parsed with mayhem/testsuite/seed.template). A no-op / neutered
program (which prints nothing) FAILS test.sh, because the SELFTEST_PASS marker and its asserted
values are only printed when every assertion holds.
"""
import pathlib

from ttp import ttp

# Resolve the seed corpus relative to this file: oracle.py lives at <repo>/mayhem/oracle.py, so the
# seeds are at <repo>/mayhem/testsuite/* (the whole repo is COPYed to /mayhem in the commit image).
HERE = pathlib.Path(__file__).resolve().parent
TEMPLATE = (HERE / "testsuite" / "seed.template").read_text()
DATA = (HERE / "testsuite" / "seed.data").read_text()


def parse(data, template):
    p = ttp(data=data, template=template)
    p.parse()
    # ttp nests results as [per-data-input][per-template-group][...]; the seed has one input + one
    # template, so the records live at result()[0][0].
    return p.result()[0][0]


# 1) The seed config parses to exactly two interface records with known field values.
records = parse(DATA, TEMPLATE)
assert isinstance(records, list), records
assert len(records) == 2, records
byname = {r["interface"]: r for r in records}

lo = byname["Loopback0"]
assert lo["ip"] == "192.168.0.113", lo
assert lo["mask"] == "24", lo
assert lo["description"] == "Router-id-loopback", lo

vlan = byname["Vlan778"]
assert vlan["ip"] == "2002::fd37", vlan
assert vlan["mask"] == "124", vlan
assert vlan["vrf"] == "CPE1", vlan

# 2) Non-matching data must yield NO fabricated records (the parser must not invent matches).
garbage = parse("this is definitely not interface config\n", TEMPLATE)
assert not garbage, garbage

print(
    "SELFTEST_PASS loopback_ip=%r vlan_vrf=%r records=%d"
    % (lo["ip"], vlan["vrf"], len(records))
)
