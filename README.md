# Learning Tactus

A book introducing Tactus: durable orchestration for tool-using AI agents.
Tactus builds on DSPy for LLM programming primitives (signatures, modules, optimizers) and adds a higher-level DSL with durability, sandboxing, and human-in-the-loop.

**Read online:** https://anthusai.github.io/Learning-Tactus/

## Building the Book

This book is built with [Quarto](https://quarto.org/). To build:

### Preview (stable port)

```bash
./scripts/preview-book.sh
```

Then open `http://127.0.0.1:4444` (the port stays fixed unless something else is using it).

### HTML Version
```bash
quarto render --to html
```

The HTML output will be in `_output/index.html` (book cover) and `_output/chapters/*.html` (chapters).

If you want HTML and PDF outputs to stop deleting each other during single-format renders, use:

```bash
./scripts/render-html.sh
./scripts/render-pdf.sh
```

That produces stable outputs at:
- `_output/html/index.html`
- `_output/pdf/Learning-Tactus.pdf`

Note: `_output/index.html` is overwritten post-render with `cover.html` (see `_quarto.yml` `project.post-render`), and the book’s preface now lives in `chapters/00-preface.qmd`. The cover expects a square animal image at `images/cover-animal.png` (or `cover-animal.png`).

### PDF Version
```bash
quarto render --to pdf
```

The PDF output will be in `_output/Learning-Tactus.pdf` with custom formatting and cover.

### Both Formats
```bash
quarto render
```

## Book Structure

- **Part I: Foundations** — What Tactus is, plus transparent durability, everything-as-code, and a quick install to run the examples.
- **Part II: Build a Useful Agent** — A single running example, iteratively extended until it’s useful (including HITL).
- **Part III: Guardrails (Safety + InfoSec)** — Capability control, sandboxing, isolation boundaries, and secretless execution.
- **Part IV: Reliability and Correctness at Scale** — Behavior specs and evaluations.
- **Part V: Putting It Together** — Complete examples you can adapt.

## Code Examples

All code examples are in the `code/` directory, organized by chapter. Each example:
- Is a runnable `.tac` file
- Includes embedded BDD specifications for testing
- Can be tested with `tactus test code/**/*.tac`

To keep examples correct and CI-backed, `code/` is copied directly from the main Tactus repo’s `examples/` directory (`../Tactus/examples`). Prefer updating the upstream example in the Tactus repo, then re-copying it into this book.

## Including Example Code in the Book

Chapters can include code directly from files under `code/` at render-time (so the book can’t drift from runnable examples).

Use a fenced code block with a `file="..."` attribute (optionally `snippet="..."` and `show-path="true"`):

````markdown
```lua {file="code/chapter-02/10-feature-state.tac" snippet="durable-loop" show-path="true"}
```
````

`show-path="true"` renders a small filename label above the code block in HTML output. For PDF output, it renders a `Source: ...` line above the block.

If you use `snippet="..."`, the included file must contain matching markers:

```lua
-- snippet:start durable-loop
-- ...
-- snippet:end durable-loop
```

If you prefer line-based slicing instead of snippet markers, use `lines="..."` (1-based, inclusive):

````markdown
```lua {file="code/chapter-02/10-feature-state.tac" lines="15-35"}
```
````

You can also use open-ended ranges:

- `lines="15-"` (from line 15 to end)
- `lines="-35"` (from start through line 35)
- `lines="15"` (just line 15)

To verify includes are valid:

```bash
python scripts/check-snippet-includes.py
```

## Testing

The GitHub Actions workflow automatically validates and tests all examples:

```bash
# Validate syntax
tactus validate code/**/*.tac

# Run BDD tests
tactus test code/**/*.tac
```

## Spec Sync Demo

This repo includes a runnable demo procedure that compares each `chapters/*.qmd` file against the Tactus specification:

```bash
tactus run sync-book-with-spec.tac --param max_chapters=3
```

It expects the Tactus repo to exist at `../Tactus` and uses sandbox volume mounts configured in `sync-book-with-spec.tac.yml`.

Outputs:
- `_output/spec-sync/spec-summary.txt`
- `_output/spec-sync/report.txt`

## Design Notes

- **PDF**: Custom styling with magenta title blocks and LaTeX cover
- **HTML**: Clean, simple styling for web readability
- **Target Audience**: AI/ML practitioners frustrated with fragile agent scripts
- **Hook**: Transparent durability - write normal code, get resilience for free

## Author

Ryan Porter

## Publisher

Anthus AI Solutions
