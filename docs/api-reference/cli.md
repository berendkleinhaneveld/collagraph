# CLI

> **TODO**: Document the Collagraph command-line interface.

## Usage

```bash
python -m collagraph [options] <file.cgx>
```

## Options

### `--help`
Show help message and exit.

### `--renderer <name>`
Specify which renderer to use (default: auto-detect).

Options:
- `pyside`
- `pygfx`
- `dict`

### `--hot-reload` (if supported)
Enable hot reloading for development.

## Examples

Run a component:
```bash
python -m collagraph app.cgx
```

Run with specific renderer:
```bash
python -m collagraph --renderer pyside my_app.cgx
```

## See Also

- [Quick Start](../getting-started/quick-start.md)
- [Hot Reloading](../guides/hot-reloading.md)
