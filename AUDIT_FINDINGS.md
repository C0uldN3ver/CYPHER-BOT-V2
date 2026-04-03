# CYPHER-BOT-V2 — Complete Audit Findings & Fix Plan

## Critical Issues Found (Will Crash the Bot)

| # | File | Issue | Fix |
|---|------|-------|-----|
| 1 | `nixpacks.toml` | Uses Nix package names (`libffi`, `opus`) but Railway Nixpacks expects `aptPackages` for Ubuntu-based builders. The `packages` key is for Nix packages, but Railway may use apt. Need to verify and use correct format. | Use `[phases.setup]` with `nixPkgs` for Nix packages OR `aptPkgs` for apt packages. |
| 2 | `Procfile` | Says `worker: python main.py` but `nixpacks.toml` says `python3.11 main.py`. Conflict. Railway uses `nixpacks.toml` `[start]` over `Procfile` when both exist. But `python3.11` may not be the correct binary name. | Align both files. Use `python main.py` in nixpacks.toml since runtime.txt controls the version. |
| 3 | `requirements.txt` | Missing `aiohttp` (needed by discord.py internally), missing `python-dotenv`. Only 3 packages listed. | Add `aiohttp>=3.9.0` to be safe. discord.py pulls it as dependency but explicit is better. |
| 4 | `inactivity.py` | The `@tasks.loop` is defined but **never started**. The loop `check_inactivity` is never called with `.start()` in `__init__`. This is not a crash but dead code. | Start the loop in `__init__` or remove it. |
| 5 | `verification.py` line 14 | `GUILD_ID = int(os.getenv("GUILD_ID"))` — raw `int()` at module level. If GUILD_ID is somehow not set, this crashes. Other cogs use `discord.Object(id=int(os.getenv("GUILD_ID")))` which has the same risk but is consistent. | All module-level env var access is protected by main.py's validation that runs first. This is safe but fragile. |
| 6 | `__pycache__` dirs | `__pycache__` directories are in the repo. These should be in `.gitignore` and removed from tracking. | Remove from git tracking. |

## Non-Critical Issues (Won't Crash But Should Be Fixed)

| # | File | Issue | Fix |
|---|------|-------|-----|
| 1 | `moderation.py`, `tools.py`, `verification.py` | `is_owner_check()` bypasses security if `OWNER_ROLE_ID` not set. Operator precedence bug: `owner_role and owner_role in interaction.user.roles or interaction.user.id == interaction.guild.owner_id` — `and` binds tighter than `or`, so this evaluates as `(owner_role and owner_role in roles) or (user.id == owner_id)`. This is actually correct behavior but should use parentheses for clarity. | Add explicit parentheses. |
| 2 | `trading_terms.py` | References `data/trading_terms.json` with relative path. On Railway, CWD may differ. | Use `os.path.dirname(__file__)` to build absolute path. |
| 3 | Multiple cogs | All placeholder responses (stats, crypto_news, cypher_ai, etc.) — functional but not real features. | Not a deployment issue. Leave as-is for now. |

## Deployment Configuration Fix Plan

1. **`runtime.txt`**: Keep `python-3.11.9` — this is correct.
2. **`nixpacks.toml`**: Fix to use correct Railway Nixpacks format. Railway uses Nixpacks which builds with Nix. The correct key is `nixPkgs` for Nix packages.
3. **`Procfile`**: Change to `worker: python3 main.py` or align with nixpacks.toml.
4. **`requirements.txt`**: Add `aiohttp` explicitly. Keep minimal.
5. **`.gitignore`**: Already has `__pycache__/`. Remove tracked `__pycache__` from git.
