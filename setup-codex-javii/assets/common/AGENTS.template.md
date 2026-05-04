# {{PROJECT_NAME}}

Proyecto inicializado con el perfil Codex `{{PROFILE}}`.

## Mision

Ayudar a implementar, validar y documentar cambios de forma clara, incremental y revisable.

## Estructura

- `.codex/config.toml`: configuracion local de Codex.
- `.codex/prompts/`: prompts reutilizables del proyecto.
- `.codex/skills/`: skills locales del proyecto.
- `docs/project-context.md`: contexto principal del proyecto.
- `docs/architecture.md`: estructura tecnica.
- `docs/task-log.md`: cambios, decisiones y validaciones.

## Reglas

- Leer `docs/project-context.md` antes de tareas importantes.
- Mantener cambios pequenos y directamente relacionados con la tarea.
- No introducir dependencias, servicios o abstracciones sin necesidad clara.
- No sobrescribir trabajo existente sin entenderlo.
- Registrar decisiones importantes en `docs/task-log.md`.

## Validacion

- Ejecutar las pruebas o checks disponibles.
- Si no hay validacion automatica, explicar que se reviso manualmente.
- No afirmar resultados no ejecutados.

## Done

- El cambio cumple el objetivo acordado.
- La validacion relevante esta ejecutada o justificada.
- La documentacion de contexto queda actualizada si cambio el objetivo, arquitectura o flujo de trabajo.

## Respuesta

Responder con resumen breve, archivos tocados, validacion y riesgos pendientes.

