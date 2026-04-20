# Week 3 Assignment

Write your solution in any language you like (Python, TypeScript, Go, Rust, etc.). Commit it to this repo and push.

## Requirements

Two automated checks run on every push. Both must pass (green check on your commit) for the assignment to count.

### 1. Your code must compile

- **Python** — no syntax errors (`python -m compileall` must succeed on every `.py`).
- **TypeScript** — `tsc --noEmit` must pass. Include a `tsconfig.json`.
- **JavaScript** — every `.js` file must parse (`node --check`).
- **Go** — `go build ./...` must succeed.
- **Rust** — `cargo check` must succeed.

If you use dependencies, include the manifest (`package.json`, `requirements.txt`, `go.mod`, `Cargo.toml`) so CI can install them.

### 2. Do not hardcode secrets or env vars

API keys, tokens, passwords, and similar secrets must **not** be written as string literals in your code. Read them from environment variables instead.

Bad:

```python
API_KEY = "sk-abc123realkey..."
```

Good:

```python
import os
API_KEY = os.environ["API_KEY"]
```

Same idea in TS/JS: use `process.env.API_KEY`, not a literal.


## How to check locally

- Python: `python -m compileall -q .`
- TS: `npx tsc --noEmit`
- Node: `node --check yourfile.js`
- Go: `go build ./...`
- Rust: `cargo check`
- Secrets: `gitleaks detect --source .`
