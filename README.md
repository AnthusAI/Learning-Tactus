# Learning Tactus

A book introducing Tactus: durable orchestration for tool-using AI agents.
Tactus builds on DSPy for LLM programming primitives (signatures, modules, optimizers) and adds a higher-level DSL with durability, sandboxing, and human-in-the-loop.

**Read online:** https://anthusai.github.io/Learning-Tactus/

## Building the Book

This book is built with [Quarto](https://quarto.org/). To build:

### HTML Version
```bash
quarto render --to html
```

The HTML output will be in `_output/index.html` with clean, simple web styling.
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

- **Part I: Foundations** — What Tactus is, plus transparent durability and everything-as-code.
- **Part II: Build a Useful Agent** — A single running example, iteratively extended until it’s useful (including HITL).
- **Part III: Reliability and Correctness at Scale** — State/idempotency, specs, and evaluations.
- **Part IV: Secure Execution at Scale** — Sandboxing, isolation boundaries, and secretless runtimes.
- **Part V: Putting It Together** — Complete examples you can adapt.

## Code Examples

All code examples are in the `code/` directory, organized by chapter. Each example:
- Is a runnable `.tac` file
- Includes embedded BDD specifications for testing
- Can be tested with `tactus test code/**/*.tac`

To keep examples correct and CI-backed, `code/` is copied directly from the main Tactus repo’s `examples/` directory (`../Tactus/examples`). Prefer updating the upstream example in the Tactus repo, then re-copying it into this book.

## Testing

The GitHub Actions workflow automatically validates and tests all examples:

```bash
# Validate syntax
tactus validate code/**/*.tac

# Run BDD tests
tactus test code/**/*.tac
```

## Design Notes

- **PDF**: Custom styling with magenta title blocks and LaTeX cover
- **HTML**: Clean, simple styling for web readability
- **Target Audience**: AI/ML practitioners frustrated with fragile agent scripts
- **Hook**: Transparent durability - write normal code, get resilience for free

## Author

Ryan Porter

## Publisher

Anthus AI Solutions
