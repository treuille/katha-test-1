# Katha Multi-Book Project

## Project Overview

A modular storybook system for creating interconnected children's stories across multiple characters. Each character has their own storybook, and characters can share scenes at the same page numbers, creating an interlocking narrative web.

## Architecture

```
world.yaml (master document)
    ↓ links to
characters/cc-name.yaml (character attributes + page list)
    ↓ references
pages/cc-pp.yaml (individual story pages)
```

### Core Concept

- **World Document** (`world.yaml`): Master YAML file defining world lore, settings, challenges, and character interactions
- **Character Files** (`characters/`): Each character is their own storybook with attributes and an ordered page list
- **Page Files** (`pages/`): Individual scenes that can belong to one or multiple characters
- **Shared Pages**: When characters interact, they share a page at the same page number in both books

### File Naming

All filenames use lowercase with dashes:

- **World**: `world.yaml`
- **Characters**: `characters/cc-name.yaml` (e.g., `ma-maya.yaml`, `le-leo.yaml`, `cu-cullan.yaml`)
  - `cc` = two-letter character code (unique identifier)
  - `name` = character name in lowercase
- **Pages**: `pages/cc-pp.yaml` (e.g., `ma-01.yaml`, `le-05.yaml`, `cu-01.yaml`)
  - `cc` = two-letter character code
  - `pp` = two-digit page number
- **Shared Pages**: `pages/cc-cc-pp.yaml` (e.g., `cu-ma-07.yaml`, `le-ma-07.yaml`)
  - Character codes in alphabetical order
  - Same page number across all involved characters

## How It Works

### world.yaml - The Master Document

`world.yaml` is the central hub:
- Defines world lore, settings, rules, themes
- Links to all character files
- Maps character interactions (who appears together, at which page numbers)
- Does NOT contain detailed character attributes (those live in character files)

### Character Files - The Storybooks

Each character file in `characters/` is a complete storybook:
- Character attributes (name, age, appearance, personality, goals, etc.)
- Ordered list of pages for this character's narrative
- References to pages they appear in (both solo and shared)

Example: `characters/ma-maya.yaml` contains:
- Maya's profile
- Her page sequence: `ma-01`, `ma-02`, ..., `le-ma-07` (shared with Leo), `ma-08`, ...

### Page Files - The Scenes

Each page in `pages/` contains:
- Story content (markdown)
- Metadata (characters, setting, mood, plot points)
- Image prompt for illustrations
- Can be referenced by one or multiple character files

### The Shared Page Constraint

**Critical Rule**: When characters share a scene, they must be at the SAME page number.

Example:
- Maya's book page 7 → `le-ma-07.yaml`
- Leo's book page 7 → `le-ma-07.yaml` (same file!)

Both `characters/ma-maya.yaml` and `characters/le-leo.yaml` list this page at position 7.

## Workflow

### 1. Create Your World
Copy `templates/world-example.yaml` to `world.yaml` at the project root:
- Fill in your world name
- Add settings and locations as needed
- Define world rules and challenges
- Set themes and tone

### 2. Create Characters
Use `/new-character` or manually create character files:
- Add to `characters/` directory
- Define attributes and relationships
- Start with empty or placeholder page list
- Update character index in `world.yaml`

### 3. Map Character Interactions
In `world.yaml`, plan which characters meet:
- Identify shared scenes
- Assign page numbers for interactions
- Note what happens in each shared scene

### 4. Generate All Pages
Use `/create-all-pages`:
- Reads character interaction map from `world.yaml`
- Follows the story structure defined in `templates/story-template.yaml`
- Creates all page files based on the 12-spread arc (beats, hooks, and payoffs)
- Generates both single-character and multi-character pages
- Includes story content, metadata, and image prompts matching the template structure

### 5. Update Character Page Lists
After pages are created, update each character file's `pages` array with the correct sequence.

### 6. Iterate
- Edit individual pages to refine content
- Adjust character attributes
- Update interaction mapping
- Regenerate or manually edit pages as needed

## File Structure

```
katha-base/
├── world.yaml                 # Your world (copy from templates/world-example.yaml)
├── characters/
│   ├── ma-maya.yaml           # Maya's storybook
│   ├── le-leo.yaml            # Leo's storybook
│   ├── sa-sara.yaml           # Sara's storybook
│   └── cu-cullan.yaml         # Cullan's storybook
├── pages/
│   ├── ma-01.yaml             # Maya solo page 1
│   ├── le-01.yaml             # Leo solo page 1
│   ├── cu-01.yaml             # Cullan solo page 1
│   ├── le-ma-07.yaml          # Shared page (both at page 7)
│   └── ...
├── templates/
│   ├── world-example.yaml
│   ├── character-template.yaml
│   └── page-template.yaml
└── .claude/
    ├── claude.md              # This file
    └── commands/
        ├── new-character.md
        ├── new-page.md
        └── create-all-pages.md
```

## Working with the Graph Structure

### How Claude Reads the Structure

When Claude needs to understand the narrative:

1. **Start at world.yaml**: See the big picture, character index, and interaction map
2. **Load character files**: Understand each character's arc and page sequence
3. **Read pages in order**: Follow the narrative by reading pages in sequence for each character
4. **Understand relationships**: See how shared pages connect different character narratives

### Example: Reading Maya's Story

```
1. Read world.yaml → see Maya's file is ma-maya.yaml, code "ma"
2. Read characters/ma-maya.yaml → get her attributes and page list
3. Read pages in order:
   - pages/ma-01.yaml (page 1, solo)
   - pages/ma-02.yaml (page 2, solo)
   - pages/le-ma-07.yaml (page 7, shared with Leo)
   - pages/ma-08.yaml (page 8, solo)
   - etc.
```

### Cross-Referencing

- Pages know which characters appear via `character_codes` field
- Character files list their full page sequence
- world.yaml maps all interactions
- No circular dependencies: world → characters → pages (one direction)

## Key Features

- **Modular and Reusable**: Same page can appear in multiple character books
- **Synchronized Interactions**: Characters share scenes at same page numbers
- **Character-Driven**: Each character is their own storybook
- **Graph Structure**: World links to characters, characters link to pages
- **Easy to Navigate**: Claude can traverse the graph to understand relationships
- **Flexible Narrative**: Mix solo and shared scenes for each character

## Templates

Templates serve as both examples and schemas, showing the structure with real example data:

- **World Template**: `templates/world-example.yaml` - Copy to `world.yaml` to create your world
- **Character Template**: `templates/character-example.yaml` - Complete example showing all fields with Cullan's data
- **Story Arc Template**: `templates/story-template.yaml` - **SOURCE OF TRUTH** for story structure: 12 spreads with beats, hooks, and payoffs
- **Page Template**: `templates/page-template.yaml` - Template for creating individual story pages
- Copy and fill in to create new content

### Story Structure

All stories follow the structure defined in `templates/story-template.yaml`:
- 12 spreads (24 pages) covering the complete story arc
- Each spread has: story beat, description, hook (anticipation), and payoff (next spread)
- Pages should match the beats, hooks, and payoffs described in the template
- This ensures consistent story structure across all character books

## Commands

- `/new-character` - Create a new character file
- `/new-page` - Create a single page (for manual additions)
- `/create-all-pages` - Generate all pages from character interaction map

## Usage in Claude Code Web

This structure works identically in both local CLI and Claude Code web:
- All context is in committed files
- Slash commands work the same way
- No environment-specific setup required
- Claude can traverse the graph structure to understand narratives

## Quick Reference

- **Master document**: `world.yaml` (at root level, copy from `templates/world-example.yaml`)
- **Story structure**: `templates/story-template.yaml` (SOURCE OF TRUTH - 12 spreads with beats, hooks, payoffs)
- **Character files**: `characters/cc-name.yaml` (see `templates/character-example.yaml` for structure)
- **Page files**: `pages/cc-pp.yaml` or `pages/cc-cc-pp.yaml` (see `templates/page-template.yaml` for structure)
- **Templates**: `templates/*.yaml` (example files that also serve as schemas)
- **Commands**: `.claude/commands/*.md` (framework files)
