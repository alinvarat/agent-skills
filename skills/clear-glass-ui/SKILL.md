---
name: clear-glass-ui
description: Style UI controls as clear, see-through smoked glass with white text floating over a full-screen photo, video, 360° panorama or 3D scene. Use when the user asks for a transparent, see-through or glass UI ("โปร่งแสง", "ใสๆ", "UI transparent") over imagery. Not for UI on plain backgrounds or text-heavy pages.
---

# Clear-glass UI over imagery

Done means: every panel shows the image clearly through it, all text is readable over both the brightest and darkest part of the image, and the result was checked in screenshots at phone size.

## 1. Apply the recipe
1. Read [glass.css](references/glass.css). Copy its tokens into the page's `:root` (or the existing token block) and use its rules. Keep the page's own fonts, spacing and layout.
2. Use a dark smoked tint with white text, not a white frosted tint with dark text. Light frosted glass with dark text fails over dark parts of the image; the user rejected it as not transparent.
3. Panels and buttons use `--glass` (alpha 0.10) and blur of 2 px. Forms and dialogs use `--glass-thick` (alpha 0.30) and blur of 6 px. Do not raise these unless text fails the check in step 3.
4. Put `text-shadow: var(--text-lift)` on every text inside glass. Readability comes from the shadow, not from a thicker panel.
5. Make the single primary action a solid light pill (`--pill-light` with dark text, no text shadow). Secondary actions are outlined glass pills.
6. On an existing design system, override its colour tokens inside the glass scope instead of editing each rule, for example:
   `.panel, .button { color-scheme: dark; --color-ink: var(--on-glass); --color-muted: var(--on-glass-muted); --color-rule: var(--on-glass-rule); }`
7. Keep the `@supports not (backdrop-filter …)` fallback, and give small dots or icons inside glass the light text colour.

## 2. Hallmark pages
When the page carries a Hallmark stamp, record the style as `theme: by request (clear glass)` in the stamp, keep every colour in tokens, and run sloplint until clean. Do not blur the dialog scrim.

## 3. Verify
1. Run `sloplint --render` when the page uses Hallmark.
2. Take phone-size screenshots (about 412×860) of: the first screen, a screen where panels sit over a bright area (sky, white wall), one over a dark area, and an open dialog or form.
3. Read every label in those screenshots. When a label is hard to read, strengthen `--text-lift` first; raise panel alpha only for that panel.
4. Report that real-phone smoothness is unverified: `backdrop-filter` over a WebGL canvas or video costs GPU time every frame. Keep blur at or below the recipe values on scenes that move.
