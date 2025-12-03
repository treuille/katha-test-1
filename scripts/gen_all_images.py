#!/usr/bin/env python3
"""
Generate images for a character's story pages in parallel, then create a PDF.

Usage:
    uv run scripts/gen_all_images.py <character-code> [--workers N]

Arguments:
    character-code  Two-letter character code (e.g., cu, em, ha)

Options:
    --workers N     Number of concurrent image generations (default: 5)

Examples:
    uv run scripts/gen_all_images.py cu
    uv run scripts/gen_all_images.py em --workers 10
    uv run scripts/gen_all_images.py ha --workers 3
"""

import subprocess
import sys
import yaml
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Tuple
import argparse


def load_character_story(char_code: str) -> List[str]:
    """Load a character's story pages from their YAML file."""
    # Find character file
    char_files = list(Path("characters").glob(f"{char_code}-*.yaml"))

    if not char_files:
        print(f"Error: No character file found for code '{char_code}'")
        print(f"Expected: characters/{char_code}-*.yaml")
        sys.exit(1)

    if len(char_files) > 1:
        print(f"Error: Multiple character files found for code '{char_code}':")
        for f in char_files:
            print(f"  - {f}")
        sys.exit(1)

    char_file = char_files[0]

    # Load character data
    try:
        with open(char_file, 'r') as f:
            char_data = yaml.safe_load(f)
    except Exception as e:
        print(f"Error loading character file {char_file}: {e}")
        sys.exit(1)

    # Get story array
    story = char_data.get('story', [])
    if not story:
        print(f"Error: No 'story' array found in {char_file}")
        sys.exit(1)

    print(f"Loaded {len(story)} pages from {char_file.name}")
    return story


def generate_image(page_path: Path) -> Tuple[Path, bool, str]:
    """
    Generate image for a single page.
    Returns (page_path, success, message).
    """
    page_id = page_path.stem

    try:
        # Print header for this worker
        print(f"\n{'='*80}")
        print(f"[{page_id}] Starting generation...")
        print(f"{'='*80}\n")

        # Call gen_image.py as subprocess, letting output flow through
        # Always use openai backend, no guide lines
        result = subprocess.run(
            ["uv", "run", "scripts/gen_image.py", "openai", str(page_path)],
            timeout=180,  # 3 minute timeout per image
        )

        # Print footer for this worker
        print(f"\n{'='*80}")
        print(f"[{page_id}] Finished (exit code: {result.returncode})")
        print(f"{'='*80}\n")

        if result.returncode == 0:
            return (page_path, True, f"✓ {page_id}")
        else:
            return (page_path, False, f"✗ {page_id}: Exit code {result.returncode}")

    except subprocess.TimeoutExpired:
        print(f"\n{'='*80}")
        print(f"[{page_id}] TIMEOUT after 3 minutes")
        print(f"{'='*80}\n")
        return (page_path, False, f"✗ {page_id}: Timeout (>3min)")
    except Exception as e:
        print(f"\n{'='*80}")
        print(f"[{page_id}] ERROR: {str(e)}")
        print(f"{'='*80}\n")
        return (page_path, False, f"✗ {page_id}: {str(e)[:100]}")


def create_pdf(char_code: str, page_filenames: List[str]) -> None:
    """Create a PDF from generated images in story order."""
    try:
        from PIL import Image
    except ImportError:
        print("Error: PIL/Pillow not installed. Run: uv pip install pillow")
        sys.exit(1)

    print("\n" + "=" * 80)
    print("Creating PDF...")
    print("=" * 80)

    # Collect images in order
    images = []
    out_images_dir = Path("out-images")

    for page_filename in page_filenames:
        page_id = Path(page_filename).stem
        image_path = out_images_dir / f"{page_id}-openai.jpg"

        if not image_path.exists():
            print(f"Error: Missing image file: {image_path}")
            sys.exit(1)

        print(f"Adding page: {page_id}")
        img = Image.open(image_path)
        images.append(img)

    # Save as PDF
    pdf_path = out_images_dir / f"{char_code}.pdf"
    print(f"\nSaving PDF to: {pdf_path}")

    if len(images) == 1:
        images[0].save(pdf_path, "PDF", resolution=100.0)
    else:
        images[0].save(
            pdf_path,
            "PDF",
            resolution=100.0,
            save_all=True,
            append_images=images[1:]
        )

    print(f"✓ PDF created successfully: {pdf_path}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Generate images for a character's story pages, then create PDF",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    uv run scripts/gen_all_images.py cu
    uv run scripts/gen_all_images.py em --workers 10
        """
    )
    parser.add_argument(
        "char_code",
        type=str,
        help="Two-letter character code (e.g., cu, em, ha)"
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=5,
        help="Number of concurrent image generations (default: 5)",
    )

    args = parser.parse_args()

    # Load character's story
    page_filenames = load_character_story(args.char_code)
    total = len(page_filenames)

    print(f"Found {total} pages for character '{args.char_code}'")
    print(f"Using {args.workers} concurrent workers")
    print(f"Backend: openai (always)")
    print("=" * 80)

    # Convert filenames to paths
    pages_dir = Path("pages")
    page_paths = []
    for page_filename in page_filenames:
        page_path = pages_dir / page_filename
        if not page_path.exists():
            print(f"Error: Page file not found: {page_path}")
            sys.exit(1)
        page_paths.append(page_path)

    # Process pages in parallel
    successes = []
    failures = []

    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        # Submit all tasks
        future_to_page = {
            executor.submit(generate_image, page): page
            for page in page_paths
        }

        # Process results as they complete
        completed = 0
        for future in as_completed(future_to_page):
            page_path, success, message = future.result()
            completed += 1

            print(f"[{completed}/{total}] {message}")

            if success:
                successes.append(page_path)
            else:
                failures.append((page_path, message))

    # Print summary
    print("=" * 80)
    print(f"\nImage Generation Summary:")
    print(f"  Total pages:    {total}")
    print(f"  Successful:     {len(successes)}")
    print(f"  Failed:         {len(failures)}")

    if failures:
        print(f"\nFailed pages:")
        for page_path, message in failures:
            print(f"  - {page_path.name}: {message}")
        sys.exit(1)
    else:
        print(f"\n✓ All images generated successfully!")

        # Create PDF
        create_pdf(args.char_code, page_filenames)
        sys.exit(0)


if __name__ == "__main__":
    main()
