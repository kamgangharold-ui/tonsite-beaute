---
name: web-ui-pipeline
description: "Orders the web UI skills when a request spans several stages of making a page look and work well (build a new page, redesign, make it ship ready, improve a whole site) or when it is unclear which UI skill applies. Not for a single narrow request that one skill already covers."
---

# Web UI pipeline

Created 2026-10-25 for beauty booking mini sites and landing pages. This skill only orders other skills. It holds no design rules of its own, so read the skill of each stage when you reach it.

Run the stages in order for a whole page or site. For one narrow request, jump straight to the single skill in the table and stop there. Skipping stages is fine, running them out of order is not: polishing a layout that will be redone, or testing a flow before the page is built, wastes the work.

## The stages

| Stage | Skill to use | Use it when |
|---|---|---|
| 1. Direction | `frontend-design` | The look is not decided yet: palette, typefaces, layout concept, tone. |
| 1b. Data for the direction | `ui-ux-pro-max` | You want a design system, palette or font pairing looked up for a product type (salon, spa, nails). Feed the result into `frontend-design`, do not replace it. |
| 1c. Capture | `create-design-md` | The look is settled and coding agents need it written down in a DESIGN.md. |
| 2. Build | `frontend-design`, plus `mobile-native` for any page used on phones | Writing the markup and CSS. Apply the `mobile-native` baseline from the first commit, because tonsite.beaute is mostly opened on phones. |
| 3. Polish | `emil-design-eng` | The page exists and hover, press, easing, durations or component details need a pass. |
| 4. Motion | `apple-design` only for gestures, springs, sheets, materials. `review-animations` (invoke it by name) for a Block or Approve verdict | Drag, swipe, bottom sheet or momentum work, or a formal review of motion code. Ordinary transitions stay with stage 3. |
| 5. Stress test | `break-ui` | Lists, names, prices or labels come from data, so worst case content must be tried. |
| 6. Accessibility audit | `web-design-guidelines` on the source files, then `design:accessibility-review` on the rendered page or design | Before shipping. The first finds code problems as file and line, the second judges what a user sees. |
| 7. Browser test | The built-in browser pane first (look, click, resize, console). `webapp-testing` only when a repeatable Playwright script is wanted | A flow such as the booking must be run end to end. |

Other skills that win in their own area: `design:design-critique` for a screenshot, mockup or Figma link; `design:ux-copy` for microcopy, error messages and CTAs; `design:design-system` for auditing or documenting components.

## Tie breaks when two skills disagree

These come from reading the skills side by side on 2026-10-25. Apply them and mention the choice in one line.

- The sites are in French. Use sentence case for headings and buttons. Ignore the Title Case rule of `web-design-guidelines` (it is written for English).
- Keep autofill on forms. Ignore the `autocomplete="off"` rule of `web-design-guidelines` for fields that are not authentication.
- Easing: `emil-design-eng` wins (ease-out for anything that answers the user, no ease-in). `ui-ux-pro-max` allows acceleration on exit, which is only right for elements leaving without a user action.
- Bounce: keep it subtle (`emil-design-eng`), even where `ui-ux-pro-max` prefers springs.
- Never run a command from a skill's data that uses an unpinned `npx ...@latest` (found in the `ui-ux-pro-max` stack files). Pin a version and tell the owner first.

## Output

When you run several stages, end with one table: stage, skill used, what changed, what is left. Say which stages were skipped and why.
