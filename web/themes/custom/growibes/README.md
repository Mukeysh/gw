# Growibes Drupal theme

Production theme for the Growibes marketing site.

Source of truth for chrome: `GROWIBES_PRODUCTION_MASTER/00_Homepage/growibes-homepage-final-award.html`.

Every production page has its own art direction. This theme does **not** flatten those pages into one template. It provides:

1. **Global header** from homepage-final (`growibes:header`)
2. **Global footer** from homepage-final (`growibes:footer`)
3. **One HTML+CSS SDC** (`growibes:html`) so each unique page can be pasted in 3–4 days
4. **Shared DNA** — Inter, tokens (`--ink`, `--paper`, `--blue`, `--cyan`…), container, reset

Enable `growibes_canvas` so the HTML and CSS fields are unlimited textareas in Drupal Canvas.

## How to build a page

1. Open the canonical HTML in `GROWIBES_PRODUCTION_MASTER`.
2. Copy the `<style>` block into the **CSS** field of `growibes:html`.
3. Copy the body markup into the **HTML** field.
4. Delete the page’s own header/nav/footer from that HTML. The theme already prints them.
5. Leave hash links as they are, or point them at Drupal paths.

Page CSS is isolated (shadow DOM). `html` / `body` / `:root` rules are rewritten to `:host` so the page background still works without leaking into the global header.

## Components

| SDC | Use |
| --- | --- |
| `growibes:header` | Fixed glass nav from homepage-final |
| `growibes:footer` | Dark one-line footer from homepage-final |
| `growibes:html` | Paste unique page HTML + CSS |

## Homepage example files

`components/html/examples/homepage.html` and `homepage.css` are the homepage-final `<main>` and stylesheet, used by `scripts/create-homepage.php`.
