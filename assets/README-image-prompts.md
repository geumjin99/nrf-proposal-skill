# README Hero-Image Prompt

One representative hero image is enough for the repo. Use the prompt below for the README top
banner (16:9). Keep a consistent palette — muted blue-gray + one warm amber/orange accent — and
always add a negative prompt like *"no gibberish text, no fake logos, no watermark, no readable
letters"* since image models mangle text. Add any real labels later in an editor, not in the prompt.

---

## HERO — "From idea to fundable proposal" (isometric workflow, 16:9)

**Vibe:** a clean little factory turning a spark of an idea into a polished Korean proposal — it
shows *what the skill actually does* (the 7-step pipeline) and renders reliably, since a clay-style
isometric diorama has no realistic faces/hands for the model to botch.

> A clean isometric 3D illustration of a small assembly line winding across a soft desk landscape,
> miniature diorama, soft clay-render look. On the far left a glowing amber lightbulb (the research
> idea) enters the track. It travels through a few tiny charming stations: a magnifying glass
> scanning floating paper cards (literature search), a blueprint being drawn (the logic skeleton),
> a little machine printing a document, a robot arm drawing a Gantt chart and a box-and-arrow flow
> diagram, and a panel of three tiny judge figurines holding blank score paddles. At the far right
> the line outputs one neat, elegant finished document standing upright with a soft glow. Muted
> blue-gray palette with warm amber highlights, gentle soft shadows, shallow depth of field,
> playful but professional, high detail, no readable text. --ar 16:9

**Knobs:** drop the judge panel for a simpler 5-station line; warm the lighting and add a tiny
plant/coffee cup for coziness; for a 1:1 social/badge crop, tighten on the lightbulb-in and
document-out ends. To soften it, give the stations rounded edges and a pastel toy aesthetic.

---

### Tips
- This single image works as both the README top banner and (cropped) the GitHub social-preview
  card (1280×640) — overlay the repo title yourself in an editor.
- Keep the one amber accent color consistent if you ever add more images later.
- Models butcher text — keep the prompt text-free; never ask it to render the proposal's words.
- The output station is a generic document, **not** a PDF icon — the skill produces HWP(`.hwpx`),
  so avoid a red PDF badge if you label it later.
