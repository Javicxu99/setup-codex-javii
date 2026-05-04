# setup-codex-javii

Este repo es una skill bootstrapper para inicializar proyectos con mi setup personal de Codex.

## Reglas de trabajo

- Mantener cambios pequenos, claros y revisables.
- No anadir dependencias externas.
- No sobreingenierizar scripts, plantillas ni workflows.
- No romper compatibilidad de la CLI sin documentarlo.
- Validar `setup-codex-javii/scripts/setup_codex_javii.py` antes de cerrar cambios.
- Mantener `AGENTS.md` y plantillas cortos, operativos y faciles de adaptar.
- Respetar siempre backups `.bak` al escribir en proyectos destino.
- Aplicar `.codex/skills/karpathy-guidelines` por defecto en tareas de codigo no triviales.
- No hacer commit sin orden explicita.

## Done

- La estructura esperada existe.
- El script funciona con `--profile default` y `--profile vehicle-3d`.
- Una segunda ejecucion crea backups antes de sobrescribir.
- El README contiene comandos reproducibles.
