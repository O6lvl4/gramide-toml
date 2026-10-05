"""Focused TOML syntax-shape evidence; not semantic validator conformance."""
from pathlib import Path
import subprocess
import sys
import tempfile
import tomllib

BIN = str(Path(sys.argv[1]).resolve())
GOOD = ['x=1','x=-1','x=0xF','x=0o755','x=0b1010','x=1_000','x=1.2e-3','x=+inf','x=-nan','x=12:30:00','x=1979-05-27 07:32:00Z','x="""\nhello\\\n world"""','""=true','[a.b]\nx=1','[[a]]\nx=1\n[[a]]\nx=2','123abc=1']
GOOD += ['1."a b" = 2', "1.'a b' = 2", '[1."a b"]\nx=2', "[1.'a b']\nx=2"]
BAD = ['x=01','x=1_','x=1__2','x=1e','x=.2','x=2.','x=+0x1','x=0x','x=0b2','x=1abc','x=[1 2]','x={a=1,}','x=true false','x=1[2]']
BAD += ['x="\x7f"', "x='\x7f'", 'x="""\x7f"""', "x='''\x7f'''", 'x=1\ry=2', '1\x01b=2', '1\x0cb=2', '1\x7fb=2', 'x=1979-05-27 07:32:00\x01Z']
with tempfile.TemporaryDirectory() as tmp:
    path = Path(tmp) / 'oracle.toml'
    for expected, samples in ((True, GOOD), (False, BAD)):
        for text in samples:
            try: tomllib.loads(text); accepted=True
            except tomllib.TOMLDecodeError: accepted=False
            assert accepted == expected, text
            path.write_text(text)
            result = subprocess.run([BIN, 'symbols', str(path)], capture_output=True, text=True, timeout=30)
            assert (result.returncode == 0) == expected, (text, result.stdout, result.stderr)
            if not expected: assert not result.stdout
print(f'TOML oracle passed: {len(GOOD)} valid and {len(BAD)} malformed syntax shapes')
