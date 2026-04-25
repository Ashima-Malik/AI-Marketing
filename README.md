# AI for Personal Brand Marketing or Business

# AI Content Creation Pipeline for Personal Brand Marketing or Business

A Claude-powered content production system that transforms a single topic into a complete,
publish-ready content package across six platforms — in one session, with one prompt.

Given a topic and keyword, the pipeline produces: a full SEO/AEO-optimized newsletter article,
a LinkedIn post, a Twitter/X thread, a Reddit post, an Instagram carousel (HTML + exportable
PNGs), and two AI-generated visual assets — all saved to a structured output folder.

---

## Table of Contents

- [How It Works](#how-it-works)
- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [Configuration](#configuration)
- [Running the Pipeline](#running-the-pipeline)
- [Running Individual Skills](#running-individual-skills)
- [Generating Images Standalone](#generating-images-standalone)
- [Output Structure](#output-structure)
- [Skills Reference](#skills-reference)
- [Customizing for Your Brand](#customizing-for-your-brand)

---

## How It Works

The system is built around **Claude Code** (Anthropic's CLI) and a set of structured Markdown
skill files. Skills are instruction sets that Claude reads and executes — they encode platform
rules, brand voice, formatting constraints, and output specs so you never have to re-explain
them.

```
Topic + Keyword
      │
      ▼
┌─────────────────────────────────────────────────────────┐
│              content-pipeline-skill.md                  │
│                                                         │
│  Phase 1 ── SEO/AEO Article       → article.md          │
│  Phase 2 ── LinkedIn Post         → linkedin.md         │
│  Phase 3 ── Twitter/X Thread      → twitter.md          │
│  Phase 4 ── Reddit Post           → reddit.md           │
│  Phase 5 ── Instagram Brief       → instagram-brief.md  │
│  Phase 6 ── Instagram HTML        → instagram-carousel  │
│  Phase 7 ── AI Images (auto-run)  → .png + .json        │
└─────────────────────────────────────────────────────────┘
      │
      ▼
output/pipeline/YYYY-MM-DD_[topic-slug]/
```

The image step (Phase 7) uses the OpenAI API: GPT-4o reads the article and writes
image generation prompts, which are then sent to `gpt-image-2`. Both images are upscaled
2× after generation for print and zoom quality.

---

## Prerequisites

| Requirement | Version |
|---|---|
| Python | 3.9 or higher |
| Claude Code CLI | Latest (`npm install -g @anthropic/claude-code`) |
| Anthropic API key | Required for Claude Code |
| OpenAI API key | Required for Phase 7 image generation only |

---

## Setup

**1. Clone the repository**

```bash
git clone <repository-url>
cd "ai marketing"
```

**2. Create and activate the virtual environment**

```bash
python3 -m venv venv
source venv/bin/activate      # macOS / Linux
venv\Scripts\activate         # Windows
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Configure environment variables**

Copy the example below and save it as `.env` in the project root:

```env
# OpenAI — required for Phase 7 image generation
OPENAI_API_KEY=sk-...

# Brand credit on generated images (bottom-right watermark)
# Set this directly, or derive from BRAND_DOMAIN + BRAND_AUTHOR_NAME below
BRAND_CREDIT=habitcoach.com · Ashima Malik

# Optional: used as fallback if BRAND_CREDIT is not set
BRAND_DOMAIN=https://habitcoach.com
BRAND_AUTHOR_NAME=Ashima Malik
```

> `.env` is listed in `.gitignore` and will never be committed.

---

## Configuration

Brand identity is controlled inside `skills/content-pipeline-skill.md` under the
**Brand Configuration** block at the top of the file. Update these values before your
first run — they propagate to every platform output automatically.

```
BRAND_AUTHOR_NAME:       Ashima Malik
BRAND_AUTHOR_TITLE:      Habit Coach
BRAND_NEWSLETTER_NAME:   The Habit Lab
BRAND_DOMAIN:            https://habitcoach.com/
BRAND_AUDIENCE:          busy professionals and general audience
BRAND_NICHE:             habit formation
BRAND_HANDLE:            @habitcoach
BRAND_LINKEDIN_URL:      https://www.linkedin.com/in/ashima-malik-ph-d-10740711a/
BRAND_SUBSCRIBER_COUNT:  12K
BRAND_COLOR_PRIMARY:     "#FF1F6B"
BRAND_COLOR_ACCENT:      "#FFD700"
BRAND_COLOR_ACCENT2:     "#00D4FF"
```

The color variables control the Instagram carousel color scheme. `BRAND_COLOR_PRIMARY` sets
the dominant slide background; `BRAND_COLOR_ACCENT` controls badge pills and highlights;
`BRAND_COLOR_ACCENT2` is used for secondary accents and contrast slides.

---

## Running the Pipeline

Open Claude Code in the project directory and invoke the pipeline skill with your topic:

```
claude
```

Then paste the following prompt (replace the bracketed values):

```
@skills/content-pipeline-skill.md

TOPIC: [Your article topic or headline angle]
PRIMARY KEYWORD: [The exact keyword phrase to optimize for]
AUDIENCE ANGLE: [Who specifically this is for]
```

**Example:**

```
@skills/content-pipeline-skill.md

TOPIC: Why your willpower is failing and how to design the friction out of your life
PRIMARY KEYWORD: friction-free habit design
AUDIENCE ANGLE: busy professionals who keep falling off their routines
```

Claude will run all 7 phases sequentially and save every output file automatically. Phase 7
(image generation) runs via the Bash tool without requiring any additional input from you.

### Regenerate social posts only

If you already have an article and only need fresh social content:

```
@skills/content-pipeline-skill.md

MODE: regenerate-social
ARTICLE_FILE: output/pipeline/2026-04-24_friction-free-habit-design/article.md
```

This skips Phase 1 and regenerates Phases 2–6 from the existing article, overwriting
the previous platform files.

---

## Running Individual Skills

Each platform skill can also be invoked independently with any article or topic as input.

```
@skills/linkedin-skill.md
@skills/twitter-skill.md
@skills/reddit-skill.md
@skills/instagram-carousel-skill.md
@skills/seo-aeo-skill.md
```

Individual skill outputs are saved to their respective folders:

```
output/linkedin/YYYY-MM-DD_[topic-slug].md
output/twitter/YYYY-MM-DD_[topic-slug].md
output/reddit/YYYY-MM-DD_[topic-slug].md
output/instagram/YYYY-MM-DD_[topic-slug].html
output/articles/YYYY-MM-DD_[topic-slug].md
```

---

## Generating Images Standalone

To regenerate or replace images for an existing pipeline folder:

```bash
# From the project root
venv/bin/python generate_images.py output/pipeline/2026-04-24_friction-free-habit-design/

# Or point directly to an article file
venv/bin/python generate_images.py output/pipeline/2026-04-24_friction-free-habit-design/article.md
```

The script runs three steps:

1. **GPT-4o reads the article** and writes both image generation prompts, choosing the best
   visual layout for the content (circular loop, icon grid, mind map, funnel, etc.)
2. **`gpt-image-2` generates both images** at their target resolutions
3. **Both images are upscaled 2× via LANCZOS + UnsharpMask** for crisp output at any size

`image-prompts.json` is saved alongside the images. If you want a different layout or style,
edit the prompts in that file and re-run `generate_images.py` — the script will use the
article file as input and overwrite the existing images.

### Generated image specs

| File | Resolution | Use case |
|---|---|---|
| `visual-infographic.png` | 2048×2048 (or 3072×2048) | Instagram carousel cover, LinkedIn image post, Twitter header |
| `concept-explainer.png` | 3072×2048 | Newsletter hero image, LinkedIn document post, article featured image |

---

## Output Structure

Every full pipeline run produces a self-contained folder:

```
output/pipeline/YYYY-MM-DD_[topic-slug]/
  ├── article.md                ← Phase 1: full article, meta block, AEO schema
  ├── linkedin.md               ← Phase 2: LinkedIn post with engagement analysis
  ├── twitter.md                ← Phase 3: Twitter/X thread with character counts
  ├── reddit.md                 ← Phase 4: Reddit post with subreddit recommendation
  ├── instagram-brief.md        ← Phase 5: slide plan, Instagram caption, hashtags
  ├── instagram-carousel.html   ← Phase 6: self-contained carousel viewer + PNG exporter
  ├── _all.md                   ← Combined: all phases in one file for review
  ├── visual-infographic.png    ← Phase 7: shareable social visual (upscaled 2×)
  ├── concept-explainer.png     ← Phase 7: landscape academic poster (upscaled 2×)
  └── image-prompts.json        ← Phase 7: GPT-4o prompts (edit + re-run to adjust style)
```

### Using the Instagram carousel

1. Open `instagram-carousel.html` in Chrome or Safari
2. Review slides using arrow keys or the navigation buttons
3. Click **Export All Slides** — PNGs are downloaded to your Downloads folder at 1200×1200px
4. Upload the PNGs directly to Instagram as a carousel post

---

## Skills Reference

| File | Purpose |
|---|---|
| `skills/content-pipeline-skill.md` | Master orchestrator — runs all 7 phases end-to-end |
| `skills/seo-aeo-skill.md` | Standalone article writer with SEO and AEO optimization |
| `skills/linkedin-skill.md` | LinkedIn post generator (4 post types) |
| `skills/twitter-skill.md` | Twitter/X thread and standalone tweet generator |
| `skills/reddit-skill.md` | Reddit post generator with subreddit selection guide |
| `skills/instagram-carousel-skill.md` | Instagram carousel HTML generator with export |

All skills use `[BRAND_*]` placeholders and work for any niche — habit formation, personal
finance, AI/tech, marketing, career, health, and others. The subreddit guide, hashtag banks,
and hook formulas inside each skill cover all major professional content niches.

---

## Customizing for Your Brand

To adapt this pipeline for a different brand or niche:

1. **Update brand values** in `skills/content-pipeline-skill.md` — the Brand Configuration
   block at the top of the file
2. **Update the image watermark** — set `BRAND_CREDIT` in `.env`
3. **Update carousel colors** — change `BRAND_COLOR_PRIMARY`, `BRAND_COLOR_ACCENT`, and
   `BRAND_COLOR_ACCENT2` in the Brand Configuration block
4. **Update individual skills** — each skill has its own Brand Configuration block at the
   top for standalone use; update these to match

The pipeline is niche-agnostic. The only hardcoded assumption is the Claude Code CLI as the
execution environment.

---

## Project Structure

```
.
├── README.md
├── generate_images.py          ← Phase 7 image generation script
├── requirements.txt
├── .env                        ← API keys and brand credit (not committed)
├── .gitignore
├── skills/
│   ├── content-pipeline-skill.md
│   ├── seo-aeo-skill.md
│   ├── linkedin-skill.md
│   ├── twitter-skill.md
│   ├── reddit-skill.md
│   └── instagram-carousel-skill.md
└── output/
    ├── pipeline/               ← Full pipeline runs (one folder per topic)
    ├── articles/               ← Standalone article outputs
    ├── linkedin/               ← Standalone LinkedIn outputs
    ├── twitter/                ← Standalone Twitter outputs
    ├── reddit/                 ← Standalone Reddit outputs
    └── instagram/              ← Standalone carousel outputs
```

---

## License

See [LICENSE](LICENSE).
