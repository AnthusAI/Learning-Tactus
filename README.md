# Learning Tactus

A book introducing the Tactus programming language for AI agents that never lose their place.

**Read online:** https://anthusai.github.io/Learning-Tactus/

## Building the Book

This book is built with [Quarto](https://quarto.org/). To build:

### HTML Version
```bash
quarto render --to html
```

The HTML output will be in `_output/index.html` with clean, simple web styling.

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

- **Part I: Why Tactus?** - The compelling case for a new language
  - Chapter 1: The Problem with Agent Scripts
  - Chapter 2: Transparent Durability
  - Chapter 3: Everything as Code

- **Part II: Getting Started** - Installation and basics
- **Part III: Core Concepts** - Tools, state, agent loops, HITL
- **Part IV: Testing Your Agents** - BDD specifications and evaluations
- **Part V: Putting It Together** - Complete examples

## Code Examples

All code examples are in the `code/` directory, organized by chapter. Each example:
- Is a runnable `.tac` file
- Includes embedded BDD specifications for testing
- Can be tested with `tactus test code/**/*.tac`

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