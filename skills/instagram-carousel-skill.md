# SKILL: Instagram Carousel Generator — AI PM Insider

## What this skill produces
A single self-contained HTML file that dynamically generates slides based on article content. Each slide is a 400×400px div styled to brand spec. The skill analyzes the article structure, extracts key concepts, frameworks, and diagrams, then creates slides that match the actual content rather than using fixed templates.

A JavaScript export function uses html2canvas to render each slide as a PNG for Instagram.
No Canva. No external tools. One file → export → post.

---

## Brand Design System (hardcoded — never change these)

### Colors
```
--bg:        #20B2AA   (slide background, teal)
--card:      #F5F5F5   (elevated surfaces, light)
--border:    #E0E0E0   (subtle borders)
--cream:     #2C3E50   (primary text on light, dark blue-gray)
--taupe:     #7F8C8D   (secondary text, gray)
--accent:    #F2C12D   (yellow — primary accent color)
--accent2:   #FF69B4   (pink — secondary accent for comparisons, CTAs)
--muted:     #95A5A6   (tertiary text, labels)
--grid-bg:   accent at 4% opacity, 32px grid (cover + CTA slides only)
```

### Typography
```
Headings:     Georgia, serif — bold, 700 weight
              Sizes: 38px (cover), 22px (section titles), 16px (slide titles)
Labels/UI:    system-ui, sans-serif — clean, 500-600 weight
              Sizes: 9-10px (labels/tags), 12-13px (body), 11px (captions)
Letter-spacing: 0.12-0.16em on uppercase labels
Brand tag:    AI PM INSIDER — always uppercase, 10px, letter-spacing .14em
```

### Slide dimensions
```
Width:  400px
Height: 400px
Border-radius: 4px (slides), 6-8px (internal cards)
Export scale: 3× (outputs at 1200×1200px — Instagram optimal)
```

### Accent bar
Every slide gets a 4px left-edge accent bar in --accent color.
Cover and CTA slides get a subtle grid background (accent color at 4% opacity, 32px grid).

### Slide numbering
Cover slide shows a circular badge (top-right): border in --accent, slide number inside.

---

## Slide Types — Use These Building Blocks

### TYPE A: Cover slide
- Full dark background with grid overlay
- Accent bar (left edge)
- Slide number badge (top right, circular, accent border)
- Tag line: "AI PM INSIDER · [Topic Name]" — uppercase, 10px, --accent color
- Headline: 3 lines max, 38px serif, cream + ONE word/phrase in --accent
- Subheadline: 13px system-ui, --taupe, 2 lines max
- Brand credit: "aiskillshub.io · Ashima Malik" — 10px, muted

### TYPE B: Problem / Hook slide
- Numbered list of 2–3 pain points
- Each item: left border in --accent, number in --accent (18px bold), text in --taupe
- Strong in cream for the pain point title, body in taupe
- Slide label: "THE PROBLEM" — 9px uppercase, --accent

### TYPE C: Architecture / Diagram slide
- Inline SVG diagram drawn at viewBox 340×220
- Background of SVG elements: #1A1A1A boxes, #161616 for containers
- Use --accent (#00E5FF) for primary flow / key boxes
- Use --accent2 (#7B61FF) for secondary elements (LLM, output, destination)
- Use #333 + dashed stroke for supporting elements (knowledge base, cache)
- Arrow color: match the box they point to
- Text inside SVG: font-family system-ui, 7-9px, fill matches the element ramp
- Caption below SVG: 10px system-ui, #555, centered, 1 sentence max
- Keep diagrams to MAX 6–8 nodes — Instagram is read at 375px wide on a phone

### TYPE D: Framework / Steps slide
- 3–4 step rows
- Each row: circular step number (28px, accent border) + content card
- Content card: 12px bold title in cream, 10px desc in muted
- Thin connector line between steps (1px, --accent at 30% opacity)
- Slide label + title follow standard pattern

### TYPE E: Comparison slide
- 2-column grid
- Left column: --accent top border (RAG / Option A)
- Right column: --accent2 top border (Fine-tuning / Option B)
- Bullet items: 4px dot matching column color, 10px text in --taupe
- Verdict bar at bottom: #0F0F0F background, 1px border #222, --accent bold for key phrase

### TYPE F: Stat / Data slide
- Full dark background with grid overlay
- Large number: 80px, 700 weight, system-ui, --accent
- Stat label: 13px system-ui, --taupe, centered, max 2 lines
- Horizontal rule: 60px wide, 1px, --accent, centered
- Source credit: 9px uppercase, #444

### TYPE G: CTA slide (always last)
- Grid background + accent bar
- "IF THIS WAS USEFUL" — 11px uppercase, --accent
- "Save this. Follow for more." — 30px serif bold, cream
- Body: 12px, #555, 2 lines about newsletter value
- Two buttons (styled divs):
  - Primary: --accent background, black text, "Save this post"
  - Secondary: transparent, --accent2 border + text, "Subscribe free → aiskillshub.io"
- Handle: "@aipminsider · Ashima Malik" — 10px uppercase muted

---

## Dynamic Slide Generation (Content-Driven)

### Input Analysis
The skill receives the full article content and:
1. **Extracts key sections** - Problem statements, frameworks, comparisons, diagrams
2. **Identifies architecture flows** - Any workflow, system design, or process diagrams
3. **Maps content to slide types** - Based on complexity and visual needs
4. **Generates slide count dynamically** - 7-12 slides depending on article depth

### Content-to-Slide Mapping Rules
| Article Content | Slide Type | When Used |
|---|---|---|
| Bold claim/hook | TYPE A (Cover) | Always first slide |
| Pain points/"Why this matters" | TYPE B (Problem) | When article has problem section |
| Architecture diagrams (→ flows) | TYPE C (Diagram) | Any workflow or system design |
| Numbered frameworks/steps | TYPE D (Framework) | When article has step-by-step |
| Comparison tables | TYPE E (Comparison) | When article compares options |
| Key statistics/data | TYPE F (Stat) | When article cites specific numbers |
| Takeaways/summary | TYPE D (Framework) | For final insights |
| CTA/newsletter | TYPE G (CTA) | Always last slide |

### Dynamic Slide Count Logic
- **Simple topic**: 7 slides (Cover + Problem + 1 Framework + 1 Comparison + 1 Stat + CTA)
- **Medium topic**: 9 slides (Cover + Problem + 2 Frameworks + 1 Comparison + 2 Diagrams + CTA)
- **Complex topic**: 12 slides (Cover + Problem + 3 Frameworks + 2 Comparisons + 3 Diagrams + 1 Stat + CTA)

The skill analyzes article structure and chooses appropriate complexity.

---

### Enhanced Diagram Rules for Instagram

Instagram is read on a 375px-wide phone screen. Diagrams that work in a newsletter
article will NOT work at Instagram slide scale. Follow these rules every time:

### Architecture Diagram Extraction
The skill automatically identifies and converts:
- **Arrow flows (→)**: Convert to SVG node diagrams
- **Workflow blocks**: Convert to structured boxes with connections
- **System components**: Map to visual hierarchy (input → process → output)
- **Comparison tables**: Convert to visual comparison slides
- **Step-by-step frameworks**: Convert to numbered flow diagrams

### Dynamic Diagram Generation
Based on article content, the skill:
1. **Scans for → arrows** indicating workflows
2. **Extracts table structures** for comparisons
3. **Identifies numbered lists** as frameworks
4. **Creates SVG representations** optimized for mobile viewing
5. **Maintains brand colors** and visual hierarchy

### Max complexity (per diagram)
- Maximum 6–8 nodes per diagram
- Maximum 2 hierarchy levels
- No more than 8 arrows total
- No labels longer than 12 characters per node

### Font sizes inside SVG (for Instagram readability)
- Node titles: 9px, font-weight 600
- Node subtitles: 8px, color #555 or #C4B5A5
- Step labels (e.g. "STEP 1"): 7px, letter-spacing .08em, color #444
- Arrow labels: avoid entirely — use node subtitle instead

### What to diagram vs what to describe
| Topic from Article | Use diagram? | Type |
|---|---|---|
| RAG architecture (→ flow) | YES | Flow: Query → Retriever → LLM → Answer |
| Fine-tuning pipeline | YES | Flow: Data → Train → Eval → Deploy |
| System design (2-layer) | YES | Structural: 2 containers max |
| Multi-stage pipeline (5+ steps) | YES | Break into multiple diagrams |
| Comparison (RAG vs FT) | YES | Visual comparison slide |
| Abstract concept (attention) | YES | Simplified: 4–5 nodes only |
| Numbered framework | YES | Step-by-step visual flow |
| Table with data | YES | Convert to visual comparison |

### Color mapping for diagrams
```
User / Input:         #F5F5F5 box + #F2C12D (accent) border + accent text
Processing / Core:    #E8E8E8 box + #E0E0E0 border + #7F8C8D text
Output / Result:      #F5F5F5 box + #FF69B4 (accent2) border + accent2 text
Supporting / Cache:   #EEEEEE box + #E0E0E0 dashed border + #95A5A6 text
Arrows (primary flow): #F2C12D stroke
Arrows (secondary):    #95A5A6 stroke
```

---

## Content-Driven HTML Generation

### Input Processing
The skill receives article content as input and processes it through these stages:

1. **Content Analysis Engine**
   - Extracts title, subtitle, and key claims
   - Identifies problem statements and pain points
   - Scans for workflow arrows (→) and numbered frameworks
   - Detects comparison tables and statistical data
   - Maps FAQ content to potential additional slides

2. **Slide Planning Algorithm**
   ```javascript
   function planSlides(articleContent) {
     const slides = [];
     
     // Always include cover and CTA
     slides.push({type: 'cover', content: extractMainClaim(articleContent)});
     
     // Dynamic content slides based on article structure
     if (hasProblemSection(articleContent)) {
       slides.push({type: 'problem', content: extractPainPoints(articleContent)});
     }
     
     const workflows = extractWorkflows(articleContent);
     workflows.forEach(flow => {
       slides.push({type: 'diagram', content: convertToSVG(flow)});
     });
     
     const frameworks = extractFrameworks(articleContent);
     frameworks.forEach(framework => {
       slides.push({type: 'framework', content: framework});
     });
     
     if (hasComparisons(articleContent)) {
       slides.push({type: 'comparison', content: extractComparisons(articleContent)});
     }
     
     if (hasStatistics(articleContent)) {
       slides.push({type: 'stat', content: extractKeyStat(articleContent)});
     }
     
     slides.push({type: 'cta', content: 'standard'});
     
     return slides;
   }
   ```

3. **Dynamic HTML Structure**
   - Generates slide divs based on planned content
   - Each slide gets appropriate CSS class and content
   - Navigation dots and arrows adjust to slide count
   - Export function works with dynamic slide numbers

### Dynamic HTML Template
```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>AI PM Insider — [Dynamic Topic] Carousel</title>
<style>
  /* Full CSS — all variables, slide types, layout */
  :root {
    --bg: #20B2AA; --card: #F5F5F5; --border: #E0E0E0;
    --cream: #2C3E50; --taupe: #7F8C8D;
    --accent: #F2C12D; --accent2: #FF69B4; --muted: #95A5A6;
  }
  /* Import html2canvas from CDN */
</style>
</head>
<body>
<div class="carousel-wrap">

  <!-- DYNAMIC SLIDE VIEWER -->
  <div class="viewer">
    <!-- Slides generated dynamically based on article content -->
    <!-- Example structure (actual slides vary by content) -->
    <div class="slide s-cover active" id="slide-1">[Dynamic Cover Content]</div>
    <div class="slide s-problem" id="slide-2">[Extracted Problem Content]</div>
    <div class="slide s-diagram" id="slide-3">[SVG from Article Workflow]</div>
    <div class="slide s-framework" id="slide-4">[Article Framework Steps]</div>
    <!-- ... more slides based on content ... -->
    <div class="slide s-cta" id="slide-N">[Standard CTA]</div>
  </div>

  <!-- DYNAMIC NAVIGATION DOTS -->
  <div class="nav-dots">
    <!-- Dots generated based on actual slide count -->
  </div>

  <!-- PREV / NEXT ARROWS -->
  <div class="nav-arrows">...</div>

  <!-- EXPORT CONTROLS -->
  <div class="export-row">
    <button onclick="exportCurrent()">Export current slide</button>
    <button onclick="exportAll()">Export all slides</button>
  </div>

</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
<script>
  // Dynamic slide count variable
  const TOTAL_SLIDES = [DYNAMIC_COUNT_FROM_ANALYSIS];
  
  // Navigation logic adapts to slide count
  // exportSlide(idx) — renders one slide to PNG at 3× scale
  // exportCurrent() — exports active slide
  // exportAll() — loops all slides with 300ms delay between exports
</script>
</body>
</html>
```

### Export function (always use this exact implementation)
```javascript
async function exportSlide(idx) {
  const slide = document.getElementById('slide-' + (idx + 1));
  const wasActive = slide.classList.contains('active');
  slide.style.display = 'flex';
  await new Promise(r => setTimeout(r, 80));
  const canvas = await html2canvas(slide, {
    width: 400,
    height: 400,
    scale: 3,
    backgroundColor: null,
    useCORS: true,
    logging: false
  });
  if (!wasActive) slide.style.display = 'none';
  const a = document.createElement('a');
  a.download = 'ai-pm-insider-slide-' + (idx + 1) + '.png';
  a.href = canvas.toDataURL('image/png');
  a.click();
}

async function exportAll() {
  for (let i = 0; i < TOTAL_SLIDES; i++) {
    await exportSlide(i);
    await new Promise(r => setTimeout(r, 300));
  }
}
```

---

## Content Rules (Brand Voice on Instagram)

### Cover headline formula
One of these patterns:
- "Stop [doing wrong thing]" — contrarian hook
- "Why [surprising claim]" — curiosity hook
- "The [number]-[unit] [framework/rule]" — practical hook
- "Most AI PMs [mistake]. Here's the fix." — pain hook

Always: ONE key phrase or word in --accent color. Max 6 words per line. Max 3 lines.

### Slide titles
- 22px serif, cream + one phrase in --accent
- Max 8 words total
- Never start with "How to" — too generic

### Body text on slides
- Max 2 lines of body text per content block
- Max 20 words per bullet point
- If it needs more than 20 words, split into two bullets
- Never use full sentences — use fragments: "Adds retrieval latency" not "This approach adds retrieval latency"

### What NOT to put on Instagram slides
- No code blocks (too small to read)
- No tables (use comparison slide TYPE E instead)
- No more than 4 bullet points per slide
- No URLs except on CTA slide
- No hashtags inside slides (add in Instagram caption, not slide)

---

## Instagram Caption (generate alongside carousel)

Always output a caption block after the HTML file:

```
--- INSTAGRAM CAPTION ---

[Hook line — restate cover headline as a question or bold claim]

Swipe to learn:
→ [what slide 2 covers]
→ [what slide 3-4 covers]
→ [what slide 5-6 covers]
→ The [framework/rule/decision] that changes how you think about this

Save this for your next [roadmap / interview / sprint / design review].

Follow @aipminsider for weekly AI PM frameworks, system design teardowns,
and interview prep.

Full article + examples: aiskillshub.io

---
HASHTAGS (paste as first comment, not in caption):
#AIProductManager #AIPM #ProductManagement #ArtificialIntelligence
#MachineLearning #AIStrategy #ProductStrategy #TechLeadership
#AIEngineering #SystemDesign #[topic-specific tag] #[topic-specific tag]
```

---

## Dynamic Content Generation Process

### Skill Input Requirements
The skill expects:
1. **Full article content** - Complete markdown from the SEO/AEO skill
2. **Article metadata** - Title, primary keyword, topic focus
3. **Architecture elements** - Any workflows, diagrams, frameworks identified

### Generation Workflow
```javascript
function generateCarousel(articleContent, metadata) {
  // Step 1: Analyze article structure
  const analysis = analyzeArticle(articleContent);
  
  // Step 2: Plan slide sequence based on content
  const slidePlan = planSlides(analysis);
  
  // Step 3: Generate dynamic HTML
  const html = generateHTML(slidePlan, metadata);
  
  // Step 4: Create Instagram caption from article
  const caption = generateCaption(articleContent, slidePlan);
  
  return { html, caption, slideCount: slidePlan.length };
}
```

### Content Extraction Rules
- **Main claim**: Extract from article title + first paragraph
- **Problem points**: Find "Why this matters" or pain point sections
- **Workflows**: Scan for → arrows and convert to SVG diagrams
- **Frameworks**: Extract numbered steps and create visual flows
- **Comparisons**: Convert article tables to comparison slides
- **Statistics**: Pull key data points for stat slides
- **CTA**: Use standard newsletter promotion

---

## Auto-Save (Content-Driven)

After generating the dynamic HTML carousel, save two things:

**1. HTML file (the dynamic carousel):**
```
output/instagram/YYYY-MM-DD_[extracted-topic-slug].html
```

**2. Caption file (the Instagram caption + hashtags):**
```
output/instagram/YYYY-MM-DD_[extracted-topic-slug]-caption.md
```

**Where:**
- `YYYY-MM-DD` = today's date (e.g. `2026-04-23`)
- `[extracted-topic-slug]` = 3–5 word lowercase slug extracted from article title/content

**Dynamic examples:**
- `output/instagram/2026-04-23_rag-architecture-guide.html`
- `output/instagram/2026-04-23_ai-pm-interview-framework-caption.md`

**What to save in the HTML file:** The complete, self-contained HTML file including
dynamically generated slides based on article content, CSS, navigation, and export script.

**What to save in the caption file:** The Instagram caption block and hashtag block generated from article content.

After saving both, confirm with:
```
✓ Saved carousel to output/instagram/[dynamic-html-filename]
✓ Saved caption to output/instagram/[dynamic-caption-filename]

Open the HTML file in a browser → click "Export all slides" to download PNGs.
```

---

## Dynamic Output Checklist

Before outputting the HTML file, verify:

### Content Coverage
- [ ] All article key concepts covered in slides
- [ ] Architecture diagrams extracted and visualized
- [ ] Frameworks converted to step-by-step slides
- [ ] Comparisons from article tables included
- [ ] Problem statements addressed

### Technical Requirements
- [ ] Slide count matches article complexity (7-12 slides)
- [ ] Slide 1 is TYPE A cover with dynamic content
- [ ] Last slide is TYPE G CTA
- [ ] All slides are exactly 400×400px
- [ ] Brand colors match spec exactly (--accent: #F2C12D, --accent2: #FF69B4, --bg: #20B2AA)
- [ ] Each slide has 4px left accent bar
- [ ] Diagrams use max 8 nodes, 9px font minimum
- [ ] Export buttons present and wired to html2canvas
- [ ] html2canvas loaded from cdnjs.cloudflare.com

### Content-Driven Features
- [ ] Workflows (→ arrows) converted to SVG diagrams
- [ ] Article tables converted to comparison slides
- [ ] Numbered frameworks visualized as step flows
- [ ] Statistics extracted for dedicated slides
- [ ] Instagram caption generated from article content
- [ ] Hashtag block separated as "first comment" recommendation
- [ ] No code blocks, no tables, no URLs (except CTA slide)
- [ ] Cover headline has one word/phrase in --accent color
- [ ] "aiskillshub.io · Ashima Malik" brand credit on cover slide

### Dynamic Validation
- [ ] Navigation dots match actual slide count
- [ ] TOTAL_SLIDES variable set correctly
- [ ] All article sections mapped to appropriate slide types
- [ ] Content extraction preserves article's key insights