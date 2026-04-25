#!/usr/bin/env python3
"""
Generate two visual assets from a pipeline article using gpt-image-2.

GPT-4o reads the article and writes the image generation prompts itself.

  1. visual-infographic.png   — visually rich, minimal-text concept infographic
                                (circular loop, mind map, icon grid, spoke diagram, etc.)
  2. concept-explainer.png    — landscape academic paper poster (multi-section, data-rich)

Both saved into the pipeline folder alongside all other outputs.

Usage:
  python generate_images.py output/pipeline/2026-04-23_habit-stacking-guide/
  python generate_images.py output/articles/2026-04-23_habit-stacking-guide.md

Brand credit is read from .env:
  BRAND_CREDIT=habitcoach.com · Ashima Malik
If not set, falls back to BRAND_DOMAIN + BRAND_AUTHOR_NAME from .env.
"""

import io
import os
import sys
import json
import base64
from pathlib import Path
from dotenv import load_dotenv
import openai
from PIL import Image, ImageFilter

# ── Config ────────────────────────────────────────────────────────────────────
load_dotenv()

MODEL_TEXT  = "gpt-4o"
MODEL_IMAGE = "gpt-image-2"

# Brand credit — set BRAND_CREDIT in .env, or derive from BRAND_DOMAIN + BRAND_AUTHOR_NAME
BRAND = (
    os.environ.get("BRAND_CREDIT")
    or f"{os.environ.get('BRAND_DOMAIN', 'your-domain.com')} · {os.environ.get('BRAND_AUTHOR_NAME', 'Your Name')}"
)


# ── Path resolution ───────────────────────────────────────────────────────────

def resolve_paths(arg: str) -> tuple:
    """
    Return (article_path: Path, output_dir: Path).
    - Directory  → article = dir/article.md, output = dir
    - .md in output/pipeline/*/ → output = parent dir
    - .md anywhere else → output = output/pipeline/<stem>/
    """
    p = Path(arg)

    if p.is_dir():
        article = p / "article.md"
        output  = p
    elif p.suffix == ".md" and p.exists():
        article = p
        output  = p.parent if "pipeline" in p.parts else Path("output/pipeline") / p.stem
    else:
        print("Usage:")
        print("  python generate_images.py <pipeline-folder>")
        print("  python generate_images.py <article.md>")
        sys.exit(1)

    if not article.exists():
        print(f"Error: article not found at {article}")
        sys.exit(1)

    output.mkdir(parents=True, exist_ok=True)
    return article, output


# ── Prompt generation ─────────────────────────────────────────────────────────

def generate_prompts(article_text: str, client: openai.OpenAI) -> dict:
    """
    Ask GPT-4o to read the article and write both image generation prompts.
    GPT-4o decides the layout, structure, content, and best image size.
    """
    resp = client.chat.completions.create(
        model=MODEL_TEXT,
        messages=[{
            "role": "user",
            "content": f"""
You are a professional visual designer creating two images for a content article.
Read the article carefully, then write two detailed prompts for gpt-image-2.

Return ONLY valid JSON, no markdown fences:
{{
  "infographic": {{
    "prompt": "...",
    "size": "1536x1024 or 1024x1536 or 1024x1024"
  }},
  "explainer": {{
    "prompt": "...",
    "size": "1536x1024"
  }}
}}

──────────────────────────────────────────
IMAGE 1 — Visual Concept Infographic
──────────────────────────────────────────
Write a prompt for a visually rich, minimal-text concept infographic.
The image should communicate the article's core idea at a glance — like a social media
infographic or educational poster. Think: bold colors, strong illustrations, very few words.

Pick the layout that best fits the article's main concept:
- CIRCULAR LOOP: concepts arranged in a clockwise cycle with arrows between them
  (great for: habits, feedback loops, cycles, processes that repeat)
- MIND MAP / SPOKE: central icon in the middle, 5–8 concept branches radiating outward,
  each with a small icon and a 1–3 word label
  (great for: multi-faceted topics, "what influences X", frameworks with sub-topics)
- ICON GRID: 4, 6, or 9 panels arranged in a grid — each panel has a bold icon/illustration
  and a 1–3 word title on a solid colored background
  (great for: lists of principles, steps, or building blocks)
- VISUAL FUNNEL or PYRAMID: layered levels showing stages, progression, or hierarchy
  (great for: mastery paths, priority frameworks, tiered models)
- SPOKE / WHEEL: central circle surrounded by smaller concept circles connected by lines,
  each with an illustration inside
  (great for: "pillars of X", "components of Y", systems with equal-weight parts)

Rules:
- MINIMAL TEXT: only short labels (1–4 words per element) — no sentences, no paragraphs
- VIBRANT, SATURATED COLORS: each concept gets its own distinct bold color
  (greens, reds, yellows, blues — high contrast, never muted or pastel)
- Bold flat-style illustrations or icons for each concept — not just abstract shapes
- White or very light background so the colors pop
- Clear visual hierarchy: one dominant central concept, supporting elements around it
- Each element feels complete and labeled — no mystery about what it represents
- No title or heading anywhere on the image
- Brand: very small gray text bottom-right: "{BRAND}"
- Choose size: 1024x1024 for circular/grid layouts, 1536x1024 for wide spoke/funnel layouts

──────────────────────────────────────────
IMAGE 2 — Landscape Academic Paper Poster
──────────────────────────────────────────
Write a prompt for a LANDSCAPE academic paper poster (always 1536x1024).
Model it exactly after a research paper one-pager / cheat sheet.

The prompt MUST instruct the image model to:
- Create a multi-section landscape poster with colored section headers and icons
- Include every important chart, diagram, flow, or plot described in the article
  (if the article doesn't provide one explicitly, design an appropriate one based on content)
- Cover every key concept thoroughly — motivation, method, structure, results, analysis, takeaways
- Use tables, graphs, flow diagrams, and comparison charts — not just bullet points
- Add a full-width TAKEAWAYS bar at the bottom with 3–4 key insights
- TYPOGRAPHY: section headers at 16pt+, body text at 12pt+ minimum — nothing smaller
- HIGH CONTRAST: pure black or very dark text on white/light backgrounds; white on dark headers
- Limit text density — prefer fewer, larger, well-spaced labels over many tiny ones
- No title or heading anywhere on the image
- Brand: very small gray text bottom-right: "{BRAND}"
- Size must always be: 1536x1024

──────────────────────────────────────────
Article:
{article_text[:9000]}
""",
        }],
        response_format={"type": "json_object"},
    )
    return json.loads(resp.choices[0].message.content)


# ── Image generation ──────────────────────────────────────────────────────────

def generate_image(prompt: str, client: openai.OpenAI, size: str) -> bytes:
    resp = client.images.generate(
        model=MODEL_IMAGE,
        prompt=prompt,
        size=size,
        quality="high",
        n=1,
    )
    return base64.b64decode(resp.data[0].b64_json)


def upscale_image(image_bytes: bytes, scale: int = 2) -> bytes:
    """
    2× LANCZOS upscale + UnsharpMask sharpening.
    Turns 1536×1024 → 3072×2048 so zooming in stays crisp.
    """
    img = Image.open(io.BytesIO(image_bytes))
    new_size = (img.width * scale, img.height * scale)
    img = img.resize(new_size, Image.LANCZOS)
    img = img.filter(ImageFilter.UnsharpMask(radius=1.5, percent=120, threshold=3))
    buf = io.BytesIO()
    img.save(buf, format="PNG", optimize=True)
    return buf.getvalue()


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python generate_images.py <pipeline-folder>")
        print("  python generate_images.py <article.md>")
        sys.exit(1)

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY not found in .env")
        sys.exit(1)

    client = openai.OpenAI(api_key=api_key)

    article_path, output_dir = resolve_paths(sys.argv[1])

    print(f"Article : {article_path}")
    print(f"Output  : {output_dir}/")
    print(f"Brand   : {BRAND}\n")

    article_text = article_path.read_text()

    # Step 1: GPT-4o generates both image prompts from the article
    print("Step 1/3 — GPT-4o writing image prompts from article...")
    data = generate_prompts(article_text, client)

    inf_prompt = data["infographic"]["prompt"]
    inf_size   = data["infographic"]["size"]
    exp_prompt = data["explainer"]["prompt"]
    exp_size   = "1536x1024"   # always landscape for academic paper poster

    # Save prompts for inspection / tweaking
    prompts_file = output_dir / "image-prompts.json"
    prompts_file.write_text(json.dumps(data, indent=2))
    print(f"  Prompts saved → {prompts_file}")
    print(f"  Infographic size : {inf_size}")
    print(f"  Explainer size   : {exp_size}\n")

    # Step 2: Visual infographic
    print("Step 2/3 — Generating visual-infographic.png...")
    inf_bytes = upscale_image(generate_image(inf_prompt, client, inf_size))
    inf_file  = output_dir / "visual-infographic.png"
    inf_file.write_bytes(inf_bytes)
    print(f"  → {inf_file}\n")

    # Step 3: Concept explainer (landscape academic poster)
    print("Step 3/3 — Generating concept-explainer.png...")
    exp_bytes = upscale_image(generate_image(exp_prompt, client, exp_size))
    exp_file  = output_dir / "concept-explainer.png"
    exp_file.write_bytes(exp_bytes)
    print(f"  → {exp_file}\n")

    # Compute actual output sizes for display
    inf_out_size = "×".join(str(int(d) * 2) for d in inf_size.split("x"))
    exp_out_size = "3072×2048"

    print("Done!")
    print(f"  ├── visual-infographic.png  ({inf_size} → {inf_out_size} after upscale)")
    print(f"  ├── concept-explainer.png   ({exp_size} → {exp_out_size} after upscale)")
    print(f"  └── image-prompts.json      (edit prompts here and re-run if needed)")
    print()
    print("Usage tips:")
    print("  visual-infographic.png → Instagram carousel cover, LinkedIn image post, Twitter header")
    print("  concept-explainer.png  → Newsletter header, LinkedIn document post, article hero image")


if __name__ == "__main__":
    main()
