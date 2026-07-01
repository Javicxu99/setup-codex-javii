# grafo/

Directorio de almacenamiento local del knowledge graph generado por [codebase-memory-mcp](https://github.com/DeusData/codebase-memory-mcp).

## Qué contiene

El binario crea aquí un archivo SQLite por proyecto:

```
grafo/
└── C-Users-...-setup-codex-javii.db   ← grafo del proyecto (gitignored)
```

El `.db` no se commitea — es estado local regenerable en segundos.

## Por qué aquí

Por defecto codebase-memory-mcp guarda los grafos en `~/.cache/codebase-memory-mcp/`.
Este proyecto redirige el cache a `grafo/` para tener todo el estado del proyecto co-localizado.
La ruta se configura en `.claude/settings.local.json` (gitignored, cada dev pone la suya):

```json
{
  "env": {
    "CBM_CACHE_DIR": "/ruta/absoluta/a/este/proyecto/grafo"
  }
}
```

## Cómo funciona

codebase-memory-mcp indexa el repositorio y construye un grafo de conocimiento:

- **Nodos**: funciones, clases, módulos, archivos, rutas HTTP, tests
- **Edges**: `CALLS`, `IMPORTS`, `DEFINES`, `IMPLEMENTS`, `INHERITS`, `SIMILAR_TO`...
- **Motor**: SQLite WAL + FTS5 para búsqueda full-text
- **Queries**: subconjunto read-only de Cypher (openCypher)
- **Velocidad**: indexación en ms, queries en <1ms

## Comandos útiles

```bash
# Indexar este proyecto (necesario tras clonar o cambiar CBM_CACHE_DIR)
codebase-memory-mcp cli index_repository '{"repo_path": "/ruta/absoluta/al/proyecto"}'

# Listar proyectos indexados
codebase-memory-mcp cli list_projects '{}'

# Buscar símbolo
codebase-memory-mcp cli search_graph '{"project": "...", "name_pattern": "mi_funcion"}'
```

## Instalación (una vez por máquina)

**macOS/Linux:**
```bash
curl -fsSL https://raw.githubusercontent.com/DeusData/codebase-memory-mcp/main/install.sh | bash
```

**Windows (PowerShell):**
```powershell
Invoke-WebRequest -Uri https://raw.githubusercontent.com/DeusData/codebase-memory-mcp/main/install.ps1 -OutFile install.ps1; .\install.ps1
```

El instalador configura Claude Code, Codex CLI, VS Code y otros agentes automáticamente.
