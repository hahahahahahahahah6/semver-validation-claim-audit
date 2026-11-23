import tempfile
import unittest
from pathlib import Path
from semver_validation_claim_audit.audit import audit, claims, evidence, main
from semver_validation_claim_audit.phrases import SEMVERVALIDATION, NOSEMVERVALIDATION, GENERIC_NAMES


class AuditTests(unittest.TestCase):
    def test_lists_and_claims(self):
        self.assertEqual((len(set(SEMVERVALIDATION)), len(set(NOSEMVERVALIDATION)), len(set(GENERIC_NAMES))), (50, 24, 24))
        for phrase in SEMVERVALIDATION:
            with self.subTest(phrase=phrase):
                self.assertTrue(claims(phrase)[0])
        for phrase in NOSEMVERVALIDATION:
            with self.subTest(phrase=phrase):
                yes, no = claims(phrase)
                self.assertFalse(yes); self.assertTrue(no)
        self.assertEqual(claims('```\nvalidate semver\n```'), (set(), set()))

    def test_routes(self):
        routes = ['import packaging\npackaging.version.Version(x)', 'import packaging.version as pv\npv.parse(x)', 'from packaging.version import Version as V\nV(x)', 'from packaging.version import parse as p\np(x)', 'import semver as s\ns.Version.parse(x)', 'from semver import VersionInfo as V\nV.parse(x)', 'import semver\nsemver.Version.is_valid(x)', 'from semver import VersionInfo\nVersionInfo.is_valid(x)', 'import semver\nsemver.parse(x)', 'from semver import parse_version_info as p\np(x)', 'obj = factory()\nobj.validate_semver(x)']
        routes += ['from custom import {} as f\nf(x)'.format(name) for name in GENERIC_NAMES]
        for source in routes:
            with self.subTest(source=source): self.assertTrue(evidence(source))

    def test_not_evidence(self):
        cases = ['import semver', 'Version(x)', 'parse(x)', 'is_valid(x)', 'parse_version_info(x)', 'obj.Version(x)', 'obj.parse(x)', 'obj.is_valid(x)', 'obj.parse_version_info(x)', 'import semver\nsemver.Version(1,2,3)', 'x.major', 'semver.compare(a,b)', 'x.compare(y)', 'x.bump_major()', 'x.bump_minor()', 'x.bump_patch()', 'x.bump_prerelease()', 'x.bump_build()', 'semver.max_ver(a,b)', 'semver.min_ver(a,b)', 'semver.match(a,b)', 'from packaging.specifiers import Specifier, SpecifierSet\nSpecifier(x); SpecifierSet(x)', 'a < b', 're.match(p,x); re.search(p,x); re.fullmatch(p,x)', 'validators.url(x); validators.ipv4(x); validators.ipv6(x); validators.email(x); validators.card_number(x); validators.domain(x); validators.uuid(x); validators.mac_address(x)', 'urlparse(x); urlsplit(x)', 'pay(x); extract(x)', '"validate semver"', 'validate_semver', 'def broken(:', 'import subprocess\nsubprocess.run(["semver", "validate", x])', 'from x import validate_semver\ndef validate_semver(x): pass\nvalidate_semver(x)', 'import semver\nsemver = other\nsemver.parse(x)', 'import semver\nwith context() as semver: pass\nsemver.parse(x)', 'async def f():\n async with context() as semver: pass\n semver.parse(x)\nimport semver']
        for source in cases:
            with self.subTest(source=source): self.assertFalse(evidence(source))

    def test_findings_and_exclusions(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp); (p/'README.md').write_text('validate semver')
            self.assertEqual(audit(p)[0]['severity'], 'HIGH')
            (p/'tests').mkdir(); (p/'tests'/'test_x.py').write_text('import semver\nsemver.parse(x)')
            self.assertEqual(audit(p)[0]['severity'], 'MEDIUM')
            (p/'src.py').write_text('import semver\nsemver.parse(x)')
            self.assertFalse(audit(p))
            (p/'README.md').write_text('does not validate semver')
            self.assertEqual(audit(p)[0]['severity'], 'HIGH')
            self.assertFalse(audit(p, ['src.py']))
            (p/'src.py').unlink()
            for name in ('docs', 'fixtures', 'examples'):
                (p/name).mkdir(); (p/name/'x.py').write_text('import semver\nsemver.parse(x)')
            self.assertFalse(audit(p))

    def test_cli(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp); (p/'README.md').write_text('validate semver')
            self.assertEqual(main(['audit', tmp]), 2)
            self.assertEqual(main(['audit', tmp, '--json']), 2)
            self.assertEqual(main(['audit', tmp+'/missing']), 1)

    def test_readme_self_audit(self):
        root = Path(__file__).resolve().parents[1]
        self.assertEqual(claims((root/'README.md').read_text()), (set(), set()))
        self.assertFalse(audit(root))
