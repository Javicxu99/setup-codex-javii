# Design Notes

## Intent

`setup-codex-javii` debe ser un bootstrapper personal, facil de copiar entre proyectos y suficientemente simple para mantenerlo sin deuda.

## Decisions

- Python estandar para evitar dependencias.
- Plantillas en `assets/` para que la skill pueda copiar recursos sin cargar todo en contexto.
- `AGENTS.md` corto y contexto largo en `docs/`.
- Backups `.bak` antes de sobrescribir archivos existentes.
- Perfil `vehicle-3d` separado para no contaminar proyectos generales.

## Non-Goals

- No gestionar MCP.
- No instalar herramientas.
- No crear un framework de plugins.
- No asumir una arquitectura unica para todos los proyectos.

