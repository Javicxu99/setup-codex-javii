# setup-codex-javii

Bootstrap personal para preparar proyectos con una configuracion estandar de Codex.

Este repositorio contiene una skill reutilizable llamada `setup-codex-javii`. Su objetivo es inicializar en cualquier repo destino una estructura minima, clara y repetible para trabajar con Codex: instrucciones de agente, configuracion, prompts, documentacion de contexto y skills locales.

## Que genera

Al ejecutar el script en un proyecto destino se crean:

- `AGENTS.md`
- `.codex/config.toml`
- `.codex/prompts/`
- `.codex/skills/`
- `docs/project-context.md`
- `docs/architecture.md`
- `docs/task-log.md`
- `docs/README.codex.md`

El perfil `vehicle-3d` anade documentacion especifica para deteccion 3D de vehiculos camera-only: datos, entrenamiento, evaluacion, exportacion ONNX, TensorRT y despliegue en Jetson.

## Uso

Puedes traer este repo desde GitHub y usarlo como base personal:

```bash
git clone https://github.com/Javicxu99/setup-codex-javii.git
```

Desde la raiz de un proyecto destino:

```bash
python path/to/setup-codex-javii/setup-codex-javii/scripts/setup_codex_javii.py --profile default
```

Para proyectos camera-only de deteccion 3D de vehiculos:

```bash
python path/to/setup-codex-javii/setup-codex-javii/scripts/setup_codex_javii.py --profile vehicle-3d
```

El script detecta la raiz del proyecto buscando `.git`, `pyproject.toml`, `package.json`, `Cargo.toml` o `go.mod`.

Si un archivo ya existe, no lo pisa en silencio: primero crea un backup `.bak`, `.bak.1`, `.bak.2`, etc.

## Configuracion generada

La configuracion base de Codex usa:

```toml
model = "gpt-5.5"
model_provider = "openai"
model_reasoning_effort = "high"
plan_mode_reasoning_effort = "high"
model_reasoning_summary = "auto"
model_verbosity = "medium"
approval_policy = "on-request"
sandbox_mode = "workspace-write"
```

No incluye MCP ni configuracion avanzada por defecto.

## Skills locales incluidas

- `project-orientation`: orientacion previa antes de una tarea importante, sin modificar codigo.
- `update-project-context`: actualizacion de contexto y log despues de cambios relevantes.
- `karpathy-guidelines`: adaptacion breve de principios de trabajo inspirados por `forrestchang/andrej-karpathy-skills`.

Este repo tambien incluye `karpathy-guidelines` en `.codex/skills/karpathy-guidelines/` para poder seleccionarla directamente desde Codex mientras trabajas en este proyecto.

## Instalar karpathy-guidelines globalmente

Para usar la skill en todos tus chats/proyectos de Codex, copia la skill al directorio global de Codex.

PowerShell:

```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.codex\skills\karpathy-guidelines"
Copy-Item -Force ".codex\skills\karpathy-guidelines\SKILL.md" "$env:USERPROFILE\.codex\skills\karpathy-guidelines\SKILL.md"
```

Bash:

```bash
mkdir -p ~/.codex/skills/karpathy-guidelines
cp .codex/skills/karpathy-guidelines/SKILL.md ~/.codex/skills/karpathy-guidelines/SKILL.md
```

## Uso con Codex en VS Code

1. Copia o referencia esta skill desde tu entorno de Codex.
2. Abre el proyecto destino en VS Code.
3. Ejecuta el script con el perfil adecuado.
4. Pide a Codex que lea `AGENTS.md` y `docs/project-context.md` antes de tareas relevantes.
5. Usa las skills locales cuando necesites orientacion, actualizacion de contexto o disciplina de implementacion.

## Validacion local

Desde la raiz de este repo:

```bash
mkdir tmp/sample-default
cd tmp/sample-default
git init
python ../../setup-codex-javii/scripts/setup_codex_javii.py --profile default
python ../../setup-codex-javii/scripts/setup_codex_javii.py --profile default
```

Comprueba que se crean backups en la segunda ejecucion.

Para el perfil `vehicle-3d`:

```bash
mkdir tmp/sample-vehicle-3d
cd tmp/sample-vehicle-3d
git init
python ../../setup-codex-javii/scripts/setup_codex_javii.py --profile vehicle-3d
```

## Primer commit

Revisa los archivos generados antes de commitear.

```bash
git status
git add .
git commit -m "Initial Codex bootstrap skill"
git push -u origin main
```
