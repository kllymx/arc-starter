# Windows Setup

arc-starter runs on Windows, but the path has a couple of gotchas that
don't exist on macOS or Linux. Read this once and you won't hit them.

## The short version

1. Install **Git for Windows** (which includes Git Bash). Required.
2. Install your agent harness (Claude Code or Codex CLI) using the
   native Windows installer. Both now support Windows directly.
3. Clone arc-starter.
4. Run `.\setup.ps1` in PowerShell.
5. Open your harness and start working.

That's it. The hooks and skills then work the same as on any other OS.

---

## Why Git Bash?

arc-starter uses shell hooks (`.sh` files in `hooks/`) for session
lifecycle events. These fire when your agent starts a session, ends one,
or compacts memory. They run through `bash`, which on Windows means
Git Bash.

- **Claude Code on Windows requires Git Bash anyway.** Its installer
  prompts you to install Git for Windows if you don't have it. Our hooks
  just work on top of that.
- **Codex CLI on Windows** can run natively in PowerShell *without*
  Git Bash, but our hooks need it. Install Git for Windows and you're set.
  If you prefer WSL2, that works too — Codex's WSL2 path is more mature
  and OpenAI recommends it for heavy use.

Install Git for Windows via winget or the installer:

```powershell
winget install Git.Git
```

Verify:

```powershell
bash --version
```

Should print `GNU bash, version ...`.

---

## Install your agent harness

### Claude Code (Anthropic's recommended path)

Open PowerShell and run:

```powershell
irm https://claude.ai/install.ps1 | iex
```

Restart your terminal after install. Verify:

```powershell
claude --version
```

### Codex CLI (OpenAI)

Option A, native (simpler):

```powershell
winget install OpenJS.NodeJS.LTS
npm install -g @openai/codex
codex --version
```

Option B, WSL2 (recommended by OpenAI for production use):

```powershell
wsl --install
```

Then inside Ubuntu:

```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
nvm install 22
npm i -g @openai/codex
codex --version
```

---

## Run arc-starter setup

From the arc-starter project root:

```powershell
powershell -ExecutionPolicy Bypass -File .\setup.ps1
```

The `-ExecutionPolicy Bypass` is a one-time override for this run only
and doesn't change your system policy. The script installs `uv` (the
Python package manager we use) and the project dependencies.

Open your harness inside the arc-starter folder. The session-start hook
should fire automatically, loading your context layer into the agent.

---

## If hooks don't fire

### Symptom: `bash: /bin/bash^M: bad interpreter`

Your shell scripts got CRLF line endings on clone. Fix:

```powershell
git rm --cached -r .
git reset --hard
```

The repo ships a `.gitattributes` that forces LF on `.sh` files, so a
fresh clone on any machine is already correct. This symptom is only for
clones that predate that fix.

### Symptom: `bash: command not found`

Git Bash isn't on your PATH. Reinstall Git for Windows and make sure
"Git Bash" is selected during install, then restart PowerShell.

### Symptom: `uv: command not found`

`uv` isn't on your PATH. Open a new PowerShell window (the install
added it to your profile but the current window doesn't know yet).

---

## What still requires Unix tools

Nothing that runs in a normal session. Everything day-to-day — skills,
commands, hooks, session capture — works on Windows with Git Bash.

The only place you'd want WSL2 is if you want the Codex sandbox to use
the more mature Linux Landlock/seccomp isolation instead of the
experimental AppContainer on native Windows. For workshop and ARC use
that's not required.
