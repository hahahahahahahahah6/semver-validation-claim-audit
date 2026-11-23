# Documentation Claim Audit

This MIT-licensed offline tool compares documented claims about judging version strings with recognizable Python call sites. It uses static patterns, not execution or semantic reasoning. Install either distribution with pip, then run:

```sh
python3 -m pip install semver_validation_claim_audit-0.1.0-py3-none-any.whl
semver-validation-claim-audit audit .
python3 -m semver_validation_claim_audit audit . --json --fail-on medium
```

The optional repository defaults to the current directory. Use `--verbose` for details and repeat `--ignore PREFIX` to exclude path prefixes. The default failure threshold is `high`; `medium` includes test-only findings. Exit status is 0 for a pass, 2 for findings at the threshold, and 1 for usage or I/O errors. The tool reads root README and Markdown under docs, excluding fenced blocks. Inline code counts. Production source, test source, fixtures, examples, and symlinks are treated separately.

Finding identifiers:

```text
documented-semver-validation-claim-false
documented-no-semver-validation-claim-false
```

## Differentiation

This audit concerns well-formed version strings. Other families cover generic input checks; ISBN book-number and ISSN serial-number check digits; IBAN bank-account check digits; UUID identifiers; card payments; extracting card details; one-time codes and confirmation links for account authentication; password verification, hashing, generation, and strength; PDF encryption; sending email and SMS; document extraction; barcode decoding and generation; email address, phone number, JSON Schema, calendar date, card number, domain, URL, IP address, and hardware address checks. A possible BIC family concerns business identifiers.

Other operations include JSON decoding, regex matching, splitting or fetching a web address, DNS resolution, reading an account number from a document, version formatting or conversion, bumping or minting a version, comparing versions, matching a constraint, judging a constraint expression, reading a version component, and fetching registry data. Those are distinct from judging an input string.

Other claim-audit families cover spreadsheet and word-document reading and generation, presentation reading and generation, PDF extraction, generation, merging, splitting, rotation, form-filling, watermarking, redaction, compression and annotation, table extraction, OCR, document extraction, e-signature, screen recording, video generation, QR and barcode generation, barcode scanning, audio mixing, generation and editing, source separation, speech recognition, text-to-speech, noise suppression, music generation and transcription. Their claims are outside this tool's phrase lists.

## Limitations

Matching is exact, so paraphrases are missed and unrelated uses can be flagged. The following individual phrases can have other meanings:

```text
validate semver
```

A database or registry lookup may be intended. This can produce a false positive.

```text
check semver
```

A manual runbook step may be intended. This can produce a false positive.

```text
semver validation
```

A roadmap feature may be intended. This can produce a false positive.

```text
semver validator
```

A hosted web page may be intended. This can produce a false positive.

```text
valid semver
```

Advice to a reader may be intended. This can produce a false positive.

```text
semver is valid
```

A successful lookup may be intended. This can produce a false positive.

```text
semver string validation
```

A specification section may be intended. This can produce a false positive.

```text
validate semver string
```

An allow-list check may be intended. This can produce a false positive.

```text
verify semver
```

A registry existence lookup may be intended. This can produce a false positive.

```text
detect invalid semver
```

A length-only check may be intended. This can produce a false positive.

```text
semver well formed
```

A theoretical discussion may be intended. This can produce a false positive.

```text
is valid semver
```

A generated value rather than input may be intended. This can produce a false positive.

```text
semver format validation
```

A spacing-only check may be intended. This can produce a false positive.

```text
validate semver version
```

A metadata label check may be intended. This can produce a false positive.

```text
semver check
```

A manual runbook step may be intended. This can produce a false positive.

```text
semver string check
```

A specification section may be intended. This can produce a false positive.

```text
validate semantic version
```

A database lookup may be intended. This can produce a false positive.

Constructing a version from integer components is not evidence.
Reading a version component is not evidence.
Comparing versions is not evidence.
Bumping a version is not evidence.
Selecting a maximum or minimum version is not evidence.
Matching a version to a constraint is not evidence.
Constructing a constraint specifier is not evidence.
Comparing already-built version objects is not evidence.
Matching a version-shaped regular expression is not evidence.
Variable chains that cannot be traced are missed.
A bare library import is not evidence.
Roadmaps, changelogs and TODOs in scanned prose still count as claims.
Denials outside the listed phrases may be missed.
Claims outside the root README and docs directory are missed.
Evidence split across modules does not combine.
Locally defined route names shadow imports and generic methods.
Dead code counts as evidence.
Calling an external command through a subprocess is not evidence.
A generic input check alone is not evidence.
An email address check alone is not evidence.
A phone number check alone is not evidence.
A URL check alone is not evidence.
An IP address check alone is not evidence.
A domain check alone is not evidence.
An ISBN check alone is not evidence.
An ISSN check alone is not evidence.
An IBAN check alone is not evidence.
A UUID check alone is not evidence.
Extraction alone is not evidence.
A locally defined generic route name is shadowed.
Untraceable alias chains are missed.
Only Python source is inspected; other languages are invisible.
Dynamic imports and runtime plugins are invisible.
The tool never executes inspected code or accesses the network.
