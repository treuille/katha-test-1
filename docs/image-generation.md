# Image Generation

Generate AI illustrations for storybook pages using the `gen_image.py` script.

## Usage

```bash
uv run scripts/gen_image.py <model-backend> <page-path>
```

## Naming Convention

Generated images follow the format: `{page-id}-{backend}.jpg`

Examples:
- `cu-01-openai.jpg` - Cullan's first page generated with OpenAI DALL-E 3
- `em-05-replicate.jpg` - Emer's fifth page generated with Replicate SDXL
- `ha-12-ideogram.jpg` - Hansel's twelfth page generated with Ideogram v3

## Image Specifications

- **Aspect Ratio**: Wide format (2:1 or 3:1 depending on backend)
- **Format**: JPEG (.jpg)
- **Resolution**: Varies by backend
  - OpenAI: 1792x1024 (2:1 ratio)
  - Replicate: 1536x768 (2:1 ratio)
  - Ideogram: 3:1 ratio (backend-dependent resolution)

## Available Backends

- **openai** - OpenAI DALL-E 3
- **replicate** - Replicate IPAdapter Style SDXL
  - **Requires** `out-images/cu-01-openai.jpg` as a style reference
  - Applies the visual style from that reference image to all generations
  - Generate the reference image with OpenAI first before using Replicate
- **ideogram** - Ideogram v3
- **prompt** - Test mode (displays prompt without generating)

## What Gets Generated

Each image includes:
1. **World Visual Style** - Consistent aesthetic from `world.yaml`
2. **Scene Illustration** - Visual description from the page YAML file

**Important**: Each generated image should be a single frame showing one moment in time. The visual descriptions should NOT include panels, subframes, or multiple scenes. Create one cohesive illustration per page.

## Setup

1. Copy `.env.example` to `.env`
2. Add your API keys:
   - `OPENAI_API_KEY` - For OpenAI backend
   - `REPLICATE_API_TOKEN` - For Replicate backend
   - `IDEOGRAM_API_KEY` and `IDEOGRAM_API_URL` - For Ideogram backend

## Examples

```bash
# Generate with OpenAI DALL-E 3
uv run scripts/gen_image.py openai pages/cu-01.yaml

# Generate with Replicate (requires reference image)
uv run scripts/gen_image.py replicate pages/em-05.yaml

# Generate with Ideogram
uv run scripts/gen_image.py ideogram pages/ha-12.yaml

# Test mode - show prompt without generating
uv run scripts/gen_image.py prompt pages/cu-ha-02.yaml
```

## Output Location

All generated images are saved to the `out-images/` directory and are git-ignored (not committed to the repository). Each user generates their own images using their API keys.
