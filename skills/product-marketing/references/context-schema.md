# Product marketing context schema

Use this for a new context document or for sections relevant to the requested update. Unknown facts stay explicitly unknown; supplied prices and claims do not change without instruction. Examples are template placeholders, not product facts.

## Sections to Capture

### 1. Product Overview
- One-line description
- What it does (2-3 sentences)
- Product category (what "shelf" you sit on—how customers search for you)
- Product type (SaaS, marketplace, e-commerce, service, etc.)
- Business model and pricing

### 2. Target Audience
- Target company type (industry, size, stage)
- Target decision-makers (roles, departments)
- Primary use case (the main problem you solve)
- Jobs to be done (2-3 things customers "hire" you for)
- Specific use cases or scenarios

### 3. Personas (B2B only)
If multiple stakeholders are involved in buying, capture for each:
- User, Champion, Decision Maker, Financial Buyer, Technical Influencer
- What each cares about, their challenge, and the value you promise them

### 4. Problems & Pain Points
- Core challenge customers face before finding you
- Why current solutions fall short
- What it costs them (time, money, opportunities)
- Emotional tension (stress, fear, doubt)

### 5. Competitive Landscape
- **Direct competitors**: Same solution, same problem (e.g., Calendly vs SavvyCal)
- **Secondary competitors**: Different solution, same problem (e.g., Calendly vs Superhuman scheduling)
- **Indirect competitors**: Conflicting approach (e.g., Calendly vs personal assistant)
- How each falls short for customers

### 6. Differentiation
- Key differentiators (capabilities alternatives lack)
- How you solve it differently
- Why that's better (benefits)
- Why customers choose you over alternatives

### 7. Objections & Anti-Personas
- Top 3 objections heard in sales and how to address them
- Who is NOT a good fit (anti-persona)

### 8. Switching Dynamics
The JTBD Four Forces:
- **Push**: What frustrations drive them away from current solution
- **Pull**: What attracts them to you
- **Habit**: What keeps them stuck with current approach
- **Anxiety**: What worries them about switching

### 9. Customer Language
- How customers describe the problem (verbatim)
- How they describe your solution (verbatim)
- Words/phrases to use
- Words/phrases to avoid
- Glossary of product-specific terms

### 10. Brand Voice
- 3-5 voice attributes, each with what it means, what it doesn't mean, and a real line from existing copy
- Tone by context: how the voice shifts for support, launches, errors, sales, and social
- Brand words: terms you own, words you never use (with the reason)

Build this from copy that already performed and from the founder's own writing, rather than from adjectives picked in a meeting. See [references/brand-voice.md](brand-voice.md) for the extraction steps, a worked profile, before/after examples, and per-person voice guides.

### 11. Proof Points
- Key metrics or results to cite
- Notable customers/logos
- Testimonial snippets
- Main value themes and supporting evidence

### 12. Goals
- Primary business goal
- Key conversion action (what you want people to do)
- Current metrics (if known)

### 13. Paid Ads (optional, only if they run ads)
The **ads** skill reads this so the user doesn't re-explain the account every session.
- Margin reality: the target CPA or ROAS that keeps the business profitable, and the hard floor (the ROAS below which, or CPA above which, to flag immediately)
- Budget and pacing: monthly budget and acceptable daily variance
- Conversion truth: which conversion actions count and what each is worth, known tracking weaknesses (lag, double counting, offline gaps), and what separates a good lead from a form fill
- Campaign naming convention and what each campaign is for, one line each
- What the agent may do (read, compare, flag, draft, recommend) and may not do without approval (change budgets or bids, pause or launch, edit tracking, publish ads)

### 14. Learnings
Start this empty unless the user supplied existing, evidenced learnings to include. Add later results using "Maintaining Learnings" in the skill entrypoint.

---

## Step 3: Create the Document

After gathering information, create `.agents/product-marketing.md` with this structure:

```markdown
# Product Marketing Context

**Document version:** v1
**Last updated:** [date]

## Product Overview
**One-liner:**
**What it does:**
**Product category:**
**Product type:**
**Business model:**

## Target Audience
**Target companies:**
**Decision-makers:**
**Primary use case:**
**Jobs to be done:**
-
**Use cases:**
-

## Personas
| Persona | Cares about | Challenge | Value we promise |
|---------|-------------|-----------|------------------|
| | | | |

## Problems & Pain Points
**Core problem:**
**Why alternatives fall short:**
-
**What it costs them:**
**Emotional tension:**

## Competitive Landscape
**Direct:** [Competitor] — falls short because...
**Secondary:** [Approach] — falls short because...
**Indirect:** [Alternative] — falls short because...

## Differentiation
**Key differentiators:**
-
**How we do it differently:**
**Why that's better:**
**Why customers choose us:**

## Objections
| Objection | Response |
|-----------|----------|
| | |

**Anti-persona:**

## Switching Dynamics
**Push:**
**Pull:**
**Habit:**
**Anxiety:**

## Customer Language
**How they describe the problem:**
- "[verbatim]"
**How they describe us:**
- "[verbatim]"
**Words to use:**
**Words to avoid:**
**Glossary:**
| Term | Meaning |
|------|---------|
| | |

## Brand Voice
| Attribute | Means | Doesn't mean | Example line |
|-----------|-------|--------------|--------------|
| | | | |

**Tone by context:**
- Support:
- Launch:
- Errors:
- Sales:
- Social:
**Terms we own:**
**Never use (and why):**

## Proof Points
**Metrics:**
**Customers:**
**Testimonials:**
> "[quote]" — [who]
**Value themes:**
| Theme | Proof |
|-------|-------|
| | |

## Goals
**Business goal:**
**Conversion action:**
**Current metrics:**

## Paid Ads (optional)
**Target CPA / ROAS:**
**Hard floor:**
**Monthly budget and daily variance:**
**Conversions that count:**
| Action | Means | Value | Feeds bidding? |
|--------|-------|-------|----------------|
| | | | |
**Known tracking weaknesses:**
**Good lead vs. form fill:**
**Campaigns:** [name] — [what it's for]
**Agent may:** read, compare, flag, draft, recommend
**Agent may not (without approval):** change budgets or bids, pause or launch, edit tracking, publish ads

## Learnings
*Decisions and tested lessons. Newest first. Keep it to about 20 active entries.*
| Date | Learning | Evidence | Applies to | Status |
|------|----------|----------|------------|--------|
| | | | | |

## Changelog
*Newest first. One line per revision: what changed and why.*
- v1 ([date]) — Initial context.
```

---

