# Full local verification on Windows

Use 64-bit PowerShell, Git for Windows (including Git Bash), Python 3.10 or
newer, and Windows' `tar.exe`. This setup does not install system-wide tools or
change the user's persistent PATH or Git configuration.

First run, from the checkout:

```powershell
./scripts/verify.ps1 -Bootstrap
```

If needed, select the actual interpreter instead of a Windows Store alias:

```powershell
./scripts/verify.ps1 -Bootstrap -Python 'C:/Python312/python.exe'
```

Subsequent runs need only `./scripts/verify.ps1` (with the same `-Python`
argument if required). Use `-Bash` for a Git Bash installation outside the
default Program Files location.

The bootstrap downloads official portable RubyInstaller 3.4.12-1, jq 1.8.2 and
Vale 3.17.1, verifies their SHA-256 digests against
`tools/windows-toolchain.json`, and extracts them under ignored
`build/toolchain/windows-x64/`. Vale matches the CI pin. Archive downloads
remain local, including their licenses. The manifest records official release
URLs and the GitHub release-asset digests checked Nov. 12, 2026; never replace
a digest just to make an unexpected download pass.

The runner scopes the tools to its own process, routes Bash's `python3` to the
selected real interpreter, and supplies a per-command Git ownership exception
for this checkout. Existing environment values are restored even on failure.
It executes the ordinary `scripts/verify.sh`, including Python regressions,
syntax, jq JSON validation, Ruby coverage validation, whitespace and the pinned
Vale fixtures. Missing prerequisites and command failures stop the run.

Validation on Nov. 12, 2026: bootstrap and cached-tool runs both passed with
Python 3.12, Ruby 3.4.12, jq 1.8.2 and Vale 3.17.1: 238 Python tests, five Vale
fixture sets and four coverage manifests (84 rule records). This does not
substitute for release CI's Linux and minimum-supported Python checks, or for
the separate tag workflow required after an authorized release.
