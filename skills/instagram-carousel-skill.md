# SKILL: Instagram Carousel Generator — Universal Brand

## Brand Configuration (Fill This In Before Running)

```
BRAND_AUTHOR_NAME:      e.g. "Ashima Malik" / "Jordan Lee" / "Dr. Sarah Chen"
BRAND_HANDLE:           e.g. "@aipminsider" / "@moneywithjordan" / "@habitlab"
BRAND_NEWSLETTER_NAME:  e.g. "AI PM Insider" / "Money Clarity Weekly" / "The Habit Lab"
BRAND_DOMAIN:           e.g. "aiskillshub.io" / "moneyclarity.com" / "habitlab.co"
BRAND_NICHE_TAG:        e.g. "AI PRODUCT" / "PERSONAL FINANCE" / "HABIT SCIENCE"
BRAND_COLOR_PRIMARY:    e.g. "#FF1F6B" (hot pink default) — the dominant slide background
BRAND_COLOR_ACCENT:     e.g. "#FFD700" (yellow default) — badge + highlight color
BRAND_COLOR_ACCENT2:    e.g. "#00D4FF" (cyan default) — secondary accent / comparison B
```

---

## What This Skill Produces

A single self-contained HTML file that dynamically generates slides based on article content.
Each slide is a **400×400px** div styled to brand spec. The skill analyzes article structure,
extracts key concepts, frameworks, and diagrams, then creates slides that match the actual
content rather than using fixed templates.

A JavaScript export function uses html2canvas to render each slide as a PNG for Instagram.
No Canva. No external tools. One file → open in browser → export → post.

---

## Brand Design System

### Colors (Vibrant — Based on Reference Palette)

```
--bg:           [BRAND_COLOR_PRIMARY]  default #FF1F6B  ← hot pink slide background
--bg-dark:      #1A1A2E               ← deep navy for stat + CTA slides
--bg-alt:       #2D1B69               ← deep purple for diagram slides
--text-primary: #FFFFFF               ← white — all main text
--text-secondary: rgba(255,255,255,0.80) ← slightly muted white
--text-muted:   rgba(255,255,255,0.55) ← labels, captions
--accent:       [BRAND_COLOR_ACCENT]  default #FFD700  ← yellow badges, highlights
--accent2:      [BRAND_COLOR_ACCENT2] default #00D4FF  ← cyan secondary accent
--accent3:      #FF6B35               ← orange for tertiary callouts
--badge-bg:     [BRAND_COLOR_ACCENT]  default #FFD700  ← label/tag pill background
--badge-text:   #1A1A1A               ← dark text on yellow badge
--card-bg:      rgba(255,255,255,0.12) ← frosted card surfaces on colored bg
--card-border:  rgba(255,255,255,0.20) ← card borders
```

**Why vibrant?** Carousels compete for attention in a fast-scroll feed.
High-contrast, saturated colors stop the scroll. Pink + yellow + white = instant standout.

### Typography (Heavy Sans-Serif — Visible at Phone Scale)

```
Headings:     'Arial Black', 'Helvetica Neue Black', Impact, sans-serif
              Sizes: 36px (cover title), 22px (section titles), 16px (slide titles)
              Weight: 900 / black — never below 700 on colored backgrounds
Body/Labels:  system-ui, -apple-system, sans-serif
              Sizes: 11px (body bullets), 12px (card titles), 9–10px (labels/captions)
Badge/Tag:    system-ui, 600 weight, 9px, letter-spacing 0.14em, ALL CAPS
Brand credit: system-ui, 500 weight, 9px, letter-spacing 0.10em
```

**No serif fonts** — Georgia and similar fonts lose legibility on phone screens at slide scale.

### Slide Dimensions

```
Width:  400px
Height: 400px
Overflow: hidden — NOTHING exits the slide boundary
Border-radius: 8px (slides), 10–12px (internal cards)
Export scale: 3× (outputs at 1200×1200px — Instagram optimal)
```

### Visual Identity Elements

- **Badge pill** (top area): `[BRAND_NICHE_TAG]` or topic tag — yellow bg (#FFD700), dark text, 9px, letter-spacing 0.14em, 4px border-radius, padding 3px 8px
- **Slide number badge** (top right): circular 28px, white border 1.5px, white number inside
- **Bottom brand strip**: `[BRAND_DOMAIN] · [BRAND_AUTHOR_NAME]` — 9px, white at 60% opacity
- **Accent bar**: 3px left edge in --accent on content slides; none on full-bleed stat/CTA slides

---

## Text Safety Rules (No Text Gets Cut — Ever)

These rules are non-negotiable. A slide that clips text is worse than a simpler slide.

### Font Size Limits by Content Volume
| Lines of text | Max font size | Max characters/line |
|---|---|---|
| 1 line (big stat / headline) | 48px | 18 chars |
| 2 lines (cover subtitle) | 28px | 22 chars |
| 3 lines (cover title) | 24px | 20 chars |
| 4–5 bullets | 11px | 28 chars |

### Overflow Prevention CSS (apply to every slide)
```css
.slide {
  overflow: hidden;
  box-sizing: border-box;
  padding: 20px 22px;          /* safe zone — never reduce below 16px */
  word-break: break-word;
  hyphens: auto;
}
.slide * {
  max-width: 100%;
  box-sizing: border-box;
}
.text-block {
  overflow: hidden;
  display: -webkit-box;
  -webkit-box-orient: vertical;
}
```

### Content Limits Per Slide
- Cover: max 6 words per line × 3 lines for title; max 12 words for subtitle
- Bullet slides: max 4 bullets × max 20 words each
- Step slides: max 4 steps × max 2 lines description each
- Comparison: max 4 bullets per column × max 15 words each
- Stat slides: number + 2-line label only — no additional text
- If content exceeds limits → **split into 2 slides**, never compress

### Auto-Truncation Rule
If generated content would overflow: truncate at the last full word that fits, add "…" only
on bullet points. Never truncate headlines — shorten them instead.

---

## Slide Types — Building Blocks

### TYPE A: Cover Slide
- Background: solid `--bg` ([BRAND_COLOR_PRIMARY])
- Top area: badge pill `[BRAND_NICHE_TAG]` + right-side slide number badge
- Title: 36px Arial Black, white, max 3 lines, ONE key phrase wrapped in `<span style="color:var(--accent)">`
- Subtitle: 14px system-ui, white at 80%, max 2 lines, max 12 words
- Bottom strip: `[BRAND_DOMAIN] · [BRAND_AUTHOR_NAME]` in white at 55%
- Grid overlay (optional): accent at 4% opacity, 28px grid — adds texture without noise

### TYPE B: Problem / Hook Slide
- Background: `--bg` (brand primary)
- Label badge: "THE PROBLEM" or "WHY THIS MATTERS" — yellow pill
- Each pain point: frosted card (`--card-bg`), left 3px border in `--accent`, bold white title 12px, desc 11px white 80%
- Max 3 pain points — if 4+, use 2 separate TYPE B slides

### TYPE C: Diagram Slide
- Background: `--bg-alt` (#2D1B69 deep purple) — contrast from main pink slides
- Label badge: "HOW IT WORKS" or descriptive topic — yellow pill
- Inline SVG viewBox="0 0 340 200"
- Node styles:
  - Input/User: white fill, `--accent` 1.5px stroke, dark text
  - Processing/Core: `rgba(255,255,255,0.15)` fill, white 1px stroke, white text
  - Output/Result: white fill, `--accent2` 1.5px stroke, `--accent2` text
  - Supporting: `rgba(255,255,255,0.08)` fill, white dashed 1px stroke, muted text
- Arrows: `--accent` (#FFD700) stroke, arrowhead marker
- Caption: 9px, white at 60%, centered below SVG, max 1 line
- Max 6–8 nodes, max 8 arrows, node labels max 12 characters

### TYPE D: Framework / Steps Slide
- Background: `--bg`
- Label badge: "FRAMEWORK" or "STEP [N] OF [N]" — yellow pill
- Title: 18px Arial Black, white, one phrase in `--accent`
- Steps: flex row — circular step number (26px, white border 1.5px, white text bold) + frosted card
  - Card: 12px bold white title, 10px white 75% desc, max 2 lines desc
  - Connector: 1px dashed white at 25% opacity
- Max 4 steps per slide — split if more

### TYPE E: Comparison Slide
- Background: `--bg`
- Label badge: "COMPARE" or "[A] vs [B]" — yellow pill
- Two columns with frosted card containers:
  - Left column: 2px solid `--accent` top border, title in `--accent`
  - Right column: 2px solid `--accent2` top border, title in `--accent2`
- Bullets: 5px dot matching column color + 10px white 80% text
- Verdict bar at bottom: white 15% bg, border-radius 6px, centered verdict in `--accent`
- Max 4 bullets per column

### TYPE F: Stat / Data Slide
- Background: `--bg-dark` (#1A1A2E) — dark navy for contrast and gravitas
- Large number: 64px Arial Black, `--accent` color, centered
- Horizontal rule: 50px wide, 2px, `--accent`, centered
- Stat label: 14px system-ui, white 80%, centered, max 2 lines, max 16 words
- Source: 9px uppercase, white at 45%, centered, max 1 line
- No other elements — keep it clean and punchy

### TYPE G: CTA Slide (Always Last)
- Background: `--bg-dark` (#1A1A2E)
- Grid overlay: white at 3% opacity, 28px grid
- Top: label badge "IF THIS HELPED" — yellow pill
- Main text: "Save this. Follow for more." — 28px Arial Black, white
- Sub-copy: 12px system-ui, white 70%, max 2 lines — newsletter value prop
- Two action buttons:
  - Primary: `--accent` bg, dark text 11px bold — "Save this post"
  - Secondary: transparent, 1.5px solid `--accent2`, `--accent2` text 11px — "Subscribe free → [BRAND_DOMAIN]"
- Brand handle: `[BRAND_HANDLE] · [BRAND_AUTHOR_NAME]` — 9px uppercase, white 50%

---

## Dynamic Slide Generation (Content-Driven)

### Input Analysis
The skill receives the full article content and:
1. Extracts key sections — problem statements, frameworks, comparisons, diagrams, stats
2. Identifies architecture flows — any workflow or process with → arrows
3. Maps content to slide types — based on complexity and visual needs
4. Generates slide count dynamically — 7–12 slides depending on article depth

### Content-to-Slide Mapping
| Article Content | Slide Type | When Used |
|---|---|---|
| Bold claim/hook | TYPE A (Cover) | Always first |
| Pain points / "Why this matters" | TYPE B (Problem) | When article has problem section |
| → arrow flows / system designs | TYPE C (Diagram) | Any workflow or architecture |
| Numbered frameworks / steps | TYPE D (Framework) | Step-by-step content |
| Comparison tables | TYPE E (Comparison) | When article compares options |
| Key statistics / data | TYPE F (Stat) | Specific numbers cited |
| Takeaways / summary | TYPE D (Framework) | Final insights |
| CTA / subscribe | TYPE G (CTA) | Always last |

### Slide Count Logic
- **Simple topic**: 7 slides (Cover + Problem + 1 Framework + 1 Comparison + 1 Stat + CTA)
- **Medium topic**: 9 slides (Cover + Problem + 2 Frameworks + 1 Comparison + 2 Diagrams + CTA)
- **Complex topic**: 12 slides (Cover + Problem + 3 Frameworks + 2 Comparisons + 3 Diagrams + 1 Stat + CTA)

---

## HTML Generation Spec

### Full CSS Variables Block
```css
:root {
  --bg:            [BRAND_COLOR_PRIMARY]; /* default: #FF1F6B */
  --bg-dark:       #1A1A2E;
  --bg-alt:        #2D1B69;
  --text-primary:  #FFFFFF;
  --text-secondary:rgba(255,255,255,0.80);
  --text-muted:    rgba(255,255,255,0.55);
  --accent:        [BRAND_COLOR_ACCENT];  /* default: #FFD700 */
  --accent2:       [BRAND_COLOR_ACCENT2]; /* default: #00D4FF */
  --accent3:       #FF6B35;
  --badge-bg:      [BRAND_COLOR_ACCENT];
  --badge-text:    #1A1A1A;
  --card-bg:       rgba(255,255,255,0.12);
  --card-border:   rgba(255,255,255,0.20);
}

/* BASE SLIDE */
.slide {
  width: 400px; height: 400px;
  overflow: hidden; box-sizing: border-box;
  border-radius: 8px; padding: 20px 22px;
  background: var(--bg);
  font-family: system-ui, -apple-system, sans-serif;
  display: none; flex-direction: column;
  position: relative;
  word-break: break-word; hyphens: auto;
}
.slide.active { display: flex; }
.slide * { box-sizing: border-box; max-width: 100%; }

/* BADGE PILL */
.badge {
  display: inline-flex; align-items: center;
  background: var(--badge-bg); color: var(--badge-text);
  font-size: 9px; font-weight: 700;
  letter-spacing: 0.14em; text-transform: uppercase;
  padding: 3px 9px; border-radius: 4px;
}

/* SLIDE NUMBER BADGE */
.slide-num {
  position: absolute; top: 18px; right: 18px;
  width: 26px; height: 26px; border-radius: 50%;
  border: 1.5px solid #FFFFFF;
  display: flex; align-items: center; justify-content: center;
  font-size: 10px; font-weight: 700; color: #FFFFFF;
}

/* BRAND STRIP */
.brand-strip {
  position: absolute; bottom: 14px; left: 22px; right: 22px;
  font-size: 9px; letter-spacing: 0.10em;
  color: rgba(255,255,255,0.55); text-transform: uppercase;
}

/* FROSTED CARD */
.card {
  background: var(--card-bg);
  border: 1px solid var(--card-border);
  border-radius: 10px; padding: 10px 12px;
  overflow: hidden;
}
```

### Dynamic HTML Template
```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>[BRAND_NEWSLETTER_NAME] — [Topic] Carousel</title>
<style>
  /* Full CSS block above */
  body { background: #0F0F0F; display:flex; flex-direction:column; align-items:center; padding:20px; font-family:system-ui; }
  .carousel-wrap { max-width:500px; width:100%; }
  .viewer { position:relative; width:400px; }
  .nav-dots { display:flex; gap:6px; justify-content:center; margin-top:12px; }
  .dot { width:8px;height:8px;border-radius:50%;background:rgba(255,255,255,0.3);cursor:pointer; }
  .dot.active { background:#FFD700; }
  .nav-arrows { display:flex; gap:10px; justify-content:center; margin-top:10px; }
  .nav-arrows button { background:rgba(255,255,255,0.1); color:#fff; border:1px solid rgba(255,255,255,0.2); border-radius:6px; padding:6px 16px; cursor:pointer; }
  .export-panel { background:#1A1A1A; border:1px solid #333; border-radius:8px; padding:16px; margin-top:16px; color:#fff; }
  .export-instructions { font-size:12px; color:#aaa; margin:0 0 12px; }
  .export-buttons { display:flex; gap:10px; }
  .export-buttons button { background:#FFD700; color:#111; border:none; border-radius:6px; padding:8px 16px; font-weight:700; font-size:12px; cursor:pointer; }
  .export-buttons button:last-child { background:transparent; color:#00D4FF; border:1px solid #00D4FF; }
</style>
</head>
<body>
<div class="carousel-wrap">
  <div class="viewer">
    <!-- Slides generated dynamically — see slide type specs above -->
    <div class="slide s-cover active" id="slide-1"><!-- TYPE A content --></div>
    <div class="slide s-problem" id="slide-2"><!-- TYPE B content --></div>
    <!-- ... more slides based on article content ... -->
    <div class="slide s-cta" id="slide-N"><!-- TYPE G content --></div>
  </div>
  <div class="nav-dots"><!-- dots auto-generated to match slide count --></div>
  <div class="nav-arrows">
    <button onclick="prevSlide()">← Prev</button>
    <button onclick="nextSlide()">Next →</button>
  </div>
  <div class="export-panel">
    <p class="export-instructions">
      Step 1: Click "Export All Slides" →
      Step 2: [N] PNGs download to Downloads folder →
      Step 3: Upload to Instagram as a carousel post
    </p>
    <div class="export-buttons">
      <button onclick="exportAll()" id="export-all-btn">Export All Slides (→ Instagram PNGs)</button>
      <button onclick="exportSlide(currentSlide)">Export Current Slide</button>
    </div>
  </div>
</div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
<script>
  const TOTAL_SLIDES = [DYNAMIC_COUNT]; // set from content analysis: 7–12
  let currentSlide = 0;

  function showSlide(idx) {
    document.querySelectorAll('.slide').forEach((s,i) => {
      s.style.display = i === idx ? 'flex' : 'none';
      s.classList.toggle('active', i === idx);
    });
    document.querySelectorAll('.dot').forEach((d,i) => d.classList.toggle('active', i === idx));
    currentSlide = idx;
  }
  function prevSlide() { showSlide(currentSlide > 0 ? currentSlide - 1 : TOTAL_SLIDES - 1); }
  function nextSlide() { showSlide(currentSlide < TOTAL_SLIDES - 1 ? currentSlide + 1 : 0); }

  async function exportSlide(idx) {
    const slide = document.getElementById('slide-' + (idx + 1));
    slide.style.display = 'flex';
    await new Promise(r => setTimeout(r, 80));
    const canvas = await html2canvas(slide, {
      width: 400, height: 400, scale: 3,
      backgroundColor: null, useCORS: true, logging: false
    });
    slide.style.display = idx === currentSlide ? 'flex' : 'none';
    const a = document.createElement('a');
    a.download = '[brand-slug]-slide-' + String(idx + 1).padStart(2, '0') + '.png';
    a.href = canvas.toDataURL('image/png');
    a.click();
  }

  async function exportAll() {
    const btn = document.getElementById('export-all-btn');
    btn.textContent = 'Exporting... (0/' + TOTAL_SLIDES + ')';
    btn.disabled = true;
    for (let i = 0; i < TOTAL_SLIDES; i++) {
      await exportSlide(i);
      btn.textContent = 'Exporting... (' + (i+1) + '/' + TOTAL_SLIDES + ')';
      await new Promise(r => setTimeout(r, 350));
    }
    btn.textContent = '✓ Done — check your Downloads folder';
    btn.disabled = false;
  }
</script>
</body>
</html>
```

---

## Cover Headline Formula (Niche-Adaptive)

Pick the pattern that fits the article:
- **Contrarian**: "Stop [doing wrong thing]" — works in any niche
- **Curiosity**: "Why [surprising claim about niche topic]"
- **Practical**: "The [N]-Step [Framework Name]"
- **Pain**: "Most [audience] [mistake]. Here's the fix."
- **Direct**: "[Outcome] in [timeframe/steps]"

Always: ONE key phrase in `--accent` color. Max 6 words per line. Max 3 lines.
Never start with a question — statements outperform questions on Instagram.

---

## Slide Content Rules (Voice on Instagram)

### Slide titles
- 18–22px Arial Black, white + one phrase in `--accent`
- Max 8 words total
- Never start with "How to" — too generic, doesn't stop scroll

### Body text
- Max 2 lines per content block
- Max 20 words per bullet
- Use fragments: "Eliminates retrieval latency" not "This approach eliminates retrieval latency"
- Every bullet must be independently readable — no "see slide 3"

### What NOT to put on slides
- No code blocks (too small, unreadable at phone scale)
- No tables (use TYPE E comparison slide instead)
- No more than 4 bullets per slide
- No URLs except on CTA slide
- No hashtags inside slides (put in caption, not slide)

---

## Instagram Caption (Generate Alongside Carousel)

```
--- INSTAGRAM CAPTION ---

[Hook — bold claim or restate cover headline as a question or statement]

Swipe to learn:
→ [what slide 2 covers]
→ [what content slides 3–N cover, summarized by theme]
→ The [framework/rule/insight] that changes how you think about [topic]

Save this for your next [relevant moment for your audience].

Follow [BRAND_HANDLE] for [brief value prop — e.g. "weekly frameworks on X topic"].

Full breakdown: [BRAND_DOMAIN]

---
HASHTAGS (paste as first comment, not in caption):
[5 niche hashtags] [2 topic-specific hashtags] [2 broad hashtags]
```

---

## Diagram Rules (Instagram-Scale SVG)

Instagram renders at 375px wide on most phones. Complex diagrams become unreadable.

### Max complexity
- Max 6–8 nodes per diagram
- Max 2 hierarchy levels
- Max 8 arrows total
- Node labels: max 12 characters — abbreviate if needed
- No arrow labels — use node subtitles instead

### Font sizes inside SVG
- Node title: 9px, font-weight 600, white
- Node subtitle: 8px, white at 70%
- Step label (e.g. "STEP 1"): 7px, letter-spacing 0.08em, white at 50%

### Conversion rules (article → SVG)
| Article element | Convert to |
|---|---|
| A → B → C (arrow flow) | Linear node chain |
| Nested list (2 levels) | Parent + child nodes |
| Comparison table | TYPE E slide (not diagram) |
| 5+ step process | Break into 2 TYPE C slides |

---

## Auto-Save

After generating, save two files:

**1. HTML carousel:**
```
output/instagram/YYYY-MM-DD_[topic-slug].html
```

**2. Caption:**
```
output/instagram/YYYY-MM-DD_[topic-slug]-caption.md
```

After saving, confirm with:
```
✓ Saved carousel to output/instagram/[filename].html
✓ Saved caption to output/instagram/[filename]-caption.md

Open the HTML file in Chrome or Safari → click "Export All Slides" → PNGs download → upload to Instagram.
```

---

## Quality Checklist

### Visual Design
- [ ] Background is vibrant [BRAND_COLOR_PRIMARY] (not dull or dark on main slides)
- [ ] Badge pills use [BRAND_COLOR_ACCENT] background with dark text
- [ ] All text is white or high-contrast on colored backgrounds
- [ ] Slide number badge visible top-right on all slides
- [ ] Brand strip at bottom of every slide

### Text Safety
- [ ] No text exits the 400×400px slide boundary
- [ ] All slides use box-sizing: border-box with 20px+ padding
- [ ] Cover title: max 3 lines, max 6 words per line
- [ ] Bullet slides: max 4 bullets, max 20 words each
- [ ] Font sizes follow the size-by-content-volume table
- [ ] No content compressed — extra content split into additional slides

### Content Coverage
- [ ] All article key concepts covered in slides
- [ ] Diagrams extracted from → arrow flows
- [ ] Frameworks converted to step-by-step TYPE D slides
- [ ] Comparison tables converted to TYPE E slides
- [ ] Key statistics get dedicated TYPE F slides

### Technical
- [ ] Slide count matches article complexity (7–12 slides)
- [ ] TYPE A cover is first slide, TYPE G CTA is last
- [ ] All slides exactly 400×400px, overflow: hidden
- [ ] TOTAL_SLIDES variable set correctly
- [ ] Navigation dots match actual slide count
- [ ] Export buttons present and wired to html2canvas
- [ ] html2canvas loaded from cdnjs.cloudflare.com
- [ ] Export scale: 3× (outputs 1200×1200px)
- [ ] Export progress counter shows (X/N) during batch export
- [ ] All [BRAND_*] placeholders replaced with real values

