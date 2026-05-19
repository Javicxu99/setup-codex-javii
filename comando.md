# Commands

Short command reference for this repo.

## Main Command

```bash
iniciar-setup
```

Run the default Codex bootstrap and offer optional CodeGraph setup.

From PowerShell inside this repo, use:

```powershell
.\iniciar-setup.cmd
```

From another project, run the launcher by absolute path:

```powershell
C:\path\to\setup-codex-javii\iniciar-setup.cmd
```

```powershell
.\iniciar-setup.ps1 -NoCodeGraph
```

Run only the Codex bootstrap and skip CodeGraph prompts.

## Bootstrap

```bash
python .codex/skills/setup-codex-javii/scripts/setup_codex_javii.py --profile default
```

Initialize the current target project with the default Codex setup.

```bash
python .codex/skills/setup-codex-javii/scripts/setup_codex_javii.py --help
```

Show bootstrap script options.

## CodeGraph

```bash
npx @colbymchenry/codegraph
```

Run the official interactive CodeGraph installer.

```bash
codegraph init -i
```

Initialize CodeGraph in the current project and create local `.codegraph/` state.

```bash
codegraph install --print-config codex
```

Print the Codex MCP config snippet without writing files.

## Validation

```bash
python -m py_compile .codex/skills/setup-codex-javii/scripts/setup_codex_javii.py
```

Check that the bootstrap script compiles.

```bash
git diff --check
```

Check for whitespace problems before commit.

```bash
rg -n "vehicle-3d|ONNX|TensorRT|Jetson|LiDAR|camera-only" --hidden -g "!tmp/**" -g "!.git/**"
```

Check that old domain-specific references did not return.

## Git

```bash
git status --short --branch
```

Show branch and changed files.

```bash
git add .
```

Stage all current changes.

```bash
git commit -m "1.0.3 Add optional CodeGraph support"
```

Create the v1.0.3 release commit.

```bash
git tag -a v1.0.3 -m "v1.0.3"
```

Create the annotated release tag.

```bash
git push
git push origin v1.0.3
```

Push the branch and release tag.

## Cleanup

```bash
Remove-Item -Recurse -Force tmp
```

Remove temporary validation folders in PowerShell.
