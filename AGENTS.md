# Learning Tactus (Agent Runbook)

## Workflow Rule (Always)

Apply requested changes in two passes:

1. **Local pass**: change the specific chapter/code mentioned.
2. **Holistic pass**: ensure coherence across `_quarto.yml` (TOC/parts), chapter transitions, cross-references, and code examples/tests.

## Quick Commands

From repo root:

```bash
# Live preview (stable URL)
./scripts/preview-book.sh
# http://127.0.0.1:4444

# Build outputs (stable locations)
./scripts/render-html.sh        # -> _output/html/index.html
./scripts/render-pdf.sh         # -> _output/pdf/Learning-Tactus.pdf (requires LaTeX)
```

Notes:
- `_quarto.yml` runs `scripts/post-render.sh` automatically after render to keep the cover/index consistent.

## Validate/Test `.tac` Examples

Examples live in `code/chapter-*/`. CI validates/tests these (see `.github/workflows/test-examples.yml`); locally:

```bash
# Validate all examples
find code -type f -name '*.tac' -print0 | xargs -0 -n1 tactus validate

# Run BDD specs (use --mock when you don’t want network/API calls)
find code -type f -name '*.tac' -print0 | xargs -0 -I{} sh -c 'tactus test "$1" --mock || true' _ {}
```

## Canonical Tactus References (Sibling Repo)

When writing/adjusting DSL details, prefer checking these first:
- `../Tactus/README.md`
- `../Tactus/SPECIFICATION.md`
- `../Tactus/docs/TOOLS.md`
- `../Tactus/examples/`

## Keeping Book Examples In Sync

- Prefer updating the upstream example in `../Tactus/examples/` first, then copying it into `code/chapter-*/` (keep filenames stable if chapters reference them).
- To find where an example is referenced in prose: `rg -n "code/chapter-" chapters`.

## Where Things Live

- Book structure/TOC: `_quarto.yml`
- Chapter content: `chapters/*.qmd`
- Code examples referenced by chapters: `code/chapter-*/**/*.tac`
