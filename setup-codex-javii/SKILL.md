---
name: setup-codex-javii
description: Inicializa un repositorio destino con el setup personal de Codex de Javii. Usar cuando el usuario quiera preparar un proyecto con AGENTS.md, .codex/config.toml, prompts, docs de contexto, perfiles default o vehicle-3d, y skills locales reutilizables.
---

# setup-codex-javii

Usar esta skill para inicializar un repo con una estructura Codex limpia, corta y mantenible.

## Procedimiento

1. Detectar la raiz del repo destino buscando `.git`, `pyproject.toml`, `package.json`, `Cargo.toml` o `go.mod`.
2. Elegir perfil:
   - `default` para proyectos generales.
   - `vehicle-3d` para deteccion 3D camera-only de vehiculos.
3. Ejecutar el script desde la raiz del proyecto destino:

```bash
python path/to/setup-codex-javii/setup-codex-javii/scripts/setup_codex_javii.py --profile default
```

o:

```bash
python path/to/setup-codex-javii/setup-codex-javii/scripts/setup_codex_javii.py --profile vehicle-3d
```

4. Crear o actualizar:
   - `AGENTS.md`
   - `.codex/config.toml`
   - `.codex/prompts/`
   - `.codex/skills/`
   - `docs/`
5. Copiar las skills locales:
   - `project-orientation`
   - `update-project-context`
   - `karpathy-guidelines`
6. Crear backups `.bak` antes de sobrescribir cualquier archivo existente.
7. Revisar el reporte final de archivos creados, archivos actualizados con backup, backups y proximos pasos.

## Reglas

- No instalar dependencias.
- No hacer commit salvo orden explicita.
- Mantener `AGENTS.md` breve; el contexto largo va en `docs/`.
- Priorizar una configuracion facil de revisar y transportar entre proyectos.

