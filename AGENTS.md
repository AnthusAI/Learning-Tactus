# AI Agent Setup Documentation

This document describes how the Learning Tactus book was created using AI agents.

## Tactus Reference Documentation

When working on this book, consult these authoritative sources in the Tactus project:

- **../Tactus/README.md** - Overview of Tactus: the problem it solves, key features, comparisons to other frameworks, and quick start guide
- **../Tactus/SPECIFICATION.md** - Complete DSL reference including all primitives, syntax, HITL patterns, and advanced features
- **../Tactus/docs/TOOLS.md** - Tools and MCP integration guide
- **../Tactus/examples/** - Working example procedures demonstrating various patterns

Tactus is a programming language for AI agents with durable execution built in. It uses a Lua-based DSL where workflows are defined as `.tac` files. Key concepts include:

- **Transparent checkpointing** - Every agent turn, tool call, and human interaction is automatically persisted
- **Human-in-the-loop** - First-class primitives for approval, input, review, and notification
- **Safe embedding** - Lua VM sandboxing for multi-tenant platforms
- **Everything as code** - Complete agent definitions in a single readable file

## Overview

The three Tactus documentation books (Learning Tactus, Programming Tactus, Tactus in a Nutshell) were created as separate Git repositories using Claude to:

1. Design the book structure and content outlines
2. Set up Quarto for professional book generation
3. Write the initial "hook" chapters for Learning Tactus
4. Create placeholder chapters for all remaining content

## Repository Structure

Three separate repositories were created as siblings to the main Tactus project:

```
/Users/ryan.porter/Projects/
├── Tactus/                    # Main Tactus repo
├── Learning-Tactus/           # Introductory book
├── Programming-Tactus/        # Comprehensive reference
└── Tactus-in-a-Nutshell/      # Quick reference
```

## Setup Process

### 1. Repository Creation

```bash
# Create directories
mkdir -p /Users/ryan.porter/Projects/{Learning-Tactus,Programming-Tactus,Tactus-in-a-Nutshell}

# Initialize git repos
cd /Users/ryan.porter/Projects/Learning-Tactus && git init
cd /Users/ryan.porter/Projects/Programming-Tactus && git init
cd /Users/ryan.porter/Projects/Tactus-in-a-Nutshell && git init
```

### 2. Quarto Configuration

Each book uses Quarto for professional typesetting. The `_quarto.yml` files configure:

- Book metadata (title, author, chapters)
- Output formats (HTML and PDF)
- Code highlighting for Lua/Tactus syntax
- LaTeX settings for PDF generation

### 3. Content Creation

#### Learning Tactus

Part I (Chapters 1-3) was fully written to establish the "hook":

1. **The Problem with Agent Scripts** - Why traditional approaches fail
2. **Transparent Durability** - How Tactus solves the durability problem
3. **Everything as Code** - The power of single-file agent definitions

These chapters include ~28KB of compelling prose designed to sell the language to AI/ML practitioners.

Parts II-V have placeholder chapters outlining the content to be written.

#### Programming Tactus

25 placeholder chapters across 8 parts provide a comprehensive reference structure.

#### Tactus in a Nutshell

10 reference chapters with more detailed placeholders including actual syntax examples and common patterns.

### 4. Code Examples

Runnable `.tac` files with embedded BDD specifications.

These are copied directly from the main Tactus repo’s `examples/` directory (`../Tactus/examples`) so they stay CI-backed and correct. Prefer updating the upstream example first, then re-copying it into this book.

```
code/
├── chapter-01/
│   └── 04-basics-simple-agent.tac
├── chapter-02/
│   └── 10-feature-state.tac
├── chapter-03/
│   └── 18-feature-lua-tools-individual.tac
└── chapter-05/
    ├── 02-basics-simple-logic.tac
    └── 70-mocking-static.tac
```

### 5. CI/CD Setup

Each repository includes `.github/workflows/test-examples.yml` to:

1. Validate all `.tac` files for syntax correctness
2. Run BDD specifications to ensure examples work
3. Optionally test consistency across multiple runs

## Building the Books

### Prerequisites

Install Quarto for book generation:

```bash
# macOS
brew install --cask quarto

# Other platforms
# Download from https://quarto.org/docs/get-started/
```

Note: The Homebrew installation on macOS requires sudo permissions.

### Generate Output

```bash
cd /Users/ryan.porter/Projects/Learning-Tactus

# Build HTML and PDF
quarto render

# Live preview during writing
quarto preview
```

Output appears in `_output/`:
- `Learning-Tactus.html` - Web version
- `Learning-Tactus.pdf` - PDF version (requires LaTeX)

## Design Decisions

### Why Separate Repositories?

- Each book can be versioned independently
- Cleaner separation of concerns
- Easier to manage permissions if books have different contributors
- Can be moved to separate GitHub repos later

### Why Quarto?

- Markdown-based (no LaTeX complexity)
- Professional PDF output
- HTML output for web reading
- Code syntax highlighting
- Cross-references and indexing
- Used by many technical books and documentation

### Content Strategy

- **Learning Tactus**: Progressive tutorial starting with "why"
- **Programming Tactus**: Comprehensive reference for all features
- **Tactus in a Nutshell**: Quick lookup for experienced users

### Testing Strategy

All code examples include BDD specifications so they can be tested automatically as Tactus evolves, ensuring the documentation stays accurate.

## Future Work

- Complete remaining chapters of Learning Tactus (Parts II-V)
- Write full content for Programming Tactus
- Write full content for Tactus in a Nutshell
- Set up GitHub repositories for collaboration
- Configure automated PDF generation in CI
- Add search functionality to HTML output

## Notes

This documentation was created during an AI-assisted session where:

1. The user requested books for Tactus
2. Claude explored the Tactus codebase to understand its positioning
3. Detailed outlines were created for all three books
4. The initial "hook" content was written for Learning Tactus
5. Full repository structures were set up with Quarto configuration

The entire process demonstrates using AI agents for documentation creation at scale.
