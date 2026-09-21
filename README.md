<!-- version: 1.1.0 | build: 2026-09-20 | update: 2026-09-20 -->
# msr-cli

The reference command-line tool for [MSR JSON](https://github.com/msrjson/specification),
providing the `msr` command.

> **Status: implementation in progress.** Nothing is published on PyPI yet.

## Role in the MSR JSON project

```
msrjson/specification        source of truth: schemas, examples, RFCs
        ▲
        │  bundles the schema of a pinned release tag
msrjson/msr-validator        the validation library
        ▲
        │  depends on
msrjson/msr-cli              this repository: the `msr` command
```

Dependencies point one way only. Validation logic lives in `msr-validator`; this
tool calls it and never reimplements it, so the command line and every registry
that imports the library always agree on what is valid.

## Planned commands

The command surface is specified at <https://msrjson.org/cli/>:

| Command | Purpose |
| --- | --- |
| `msr validate` | Validate a manifest — delegates to `msr-validator` |
| `msr generate` | Draft a manifest from a project's own metadata |
| `msr lint` | Style and completeness checks beyond schema validity |
| `msr convert` | Migrate legacy formats such as PAD XML |
| `msr sign` | Detached signatures over a manifest |

The initial release implements only `msr validate`; the remaining commands are
not advertised as available until their behavior and tests exist.

```bash
msr validate .well-known/msr.json
```

`sign` is the reason this is a separate package: it needs cryptographic
dependencies, and a registry importing only the validator should not inherit
them.

## Rules this implementation follows

- **Never publish a digest, a package or an install command before the artifact
  exists.** Release checksums are computed from the real published files.
- **Python**, published on PyPI as `msr-cli`. (The PyPI name `msr` belongs to an
  unrelated project; the installed command is still `msr`.)

## Author

MSR JSON was created by Antonio Santos. See the
[specification's AUTHORS](https://github.com/msrjson/specification/blob/main/AUTHORS).

## License

[MIT](LICENSE).

## Experimental MSR JSON 2.1 validation

Until 2.1 is ratified and pinned, pass the local draft schema explicitly.
The default remains the bundled MSR JSON 2.0 schema.

```bash
msr validate .well-known/msr.json --schema path/to/msr-2.1-draft.json
```
