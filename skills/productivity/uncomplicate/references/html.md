# HTML output

Start from `${CLAUDE_PLUGIN_ROOT}/skills/productivity/uncomplicate/assets/template.html`. Copy it, then replace `{{LANG}}`, `{{TITLE}}` (both places), `{{BODY}}` and `{{NOTES}}`, and delete the optional comments you don't use. Keep the CSS as is: it already handles line length, dark mode, narrow screens and print. If a document needs something the CSS lacks, add the smallest rule that does it inside the same `<style>` block.

## Body

- **Headings:** one `<h1>` (the title). Sections use `<h2>`, subsections `<h3>`, and no level is skipped. Give every `<h2>` and `<h3>` an `id`: lowercase words joined by hyphens, no spaces, unique in the file. Letters outside ASCII are fine.
- **TOC:** add the `nav.toc` block when the document runs over about 800 words and has more than three `<h2>` sections. Link every `<h2>`. Short documents don't need one.
- **Semantic tags:** `<p>` for prose, `<ol>` for steps and ranked items, `<ul>` for unordered sets, `<table>` (wrapped in `<div class="table-wrap">`, with `<th>` headers) for items that share fields, `<pre><code>` for code and commands, `<blockquote>` for quotations, and `<p class="lede">` for an opening summary if the document needs one.
- **Callouts, used sparingly:** `<aside class="note">` for a warning or constraint the document's reader must not miss. That one is part of the document.
- **Gap markers (editor layer):** `<aside class="gap editor" role="note"><p><strong>Open question:</strong> …</p></aside>` goes where information is missing or ambiguous. Keep it to one or two sentences: what's missing, and why the reader needs it. The `editor` class hides it in print, so never put document content inside it.
- **Links and citations:** keep every source link as `<a href="…">` with readable link text, and keep reference lists and footnotes. Keep relative links (`docs/setup.md`, `../api.html#auth`) as they are. Internal links point at real `id`s. Allowed schemes are `http:`, `https:`, `mailto:` and `tel:`; drop any other scheme (`javascript:`, `data:`, `file:`) and mention it in the notes. When the link text is the URL itself, add `class="url"` so print does not repeat it.
- **No decoration:** no emojis, icons, cards, badges, colored boxes or dashboards unless the content needs them.

## Escaping

All source text is data. Before you put any of it into HTML, escape `&` as `&amp;`, `<` as `&lt;` and `>` as `&gt;`, and in attribute values `"` as `&quot;`. That includes code samples, quoted HTML, angle-bracketed placeholders like `<user-id>`, and anything that looks like a tag or script. The file must contain no `<script>`, no `on…=` event attributes, no `javascript:` URLs, no `<iframe>`, `<object>`, `<embed>` or `<form>`, and nothing loaded from the network (stylesheets, fonts, images, `@import`). Images in the source become their alt text or a link to them. The checker allows only the tags the template and this page use, so a stray `<user-id>` or `List<String>` that you forgot to escape fails it.

## Notes section

The template's notes section carries the `editor` class: it shows collapsed on screen and is left out of print. Write the editor layer (notes and gap markers) in the language the user wrote to you, and translate the template's "Editing notes" and "(for the author; not printed)" to match. If that language differs from the document's, add `lang` to the notes `<section>` and to each gap `<aside>`. Inside `{{NOTES}}`, in this order, with `<h3>` headings, and leave out any part that would be empty:

1. **What changed**: three to six bullets, structure first.
2. **Open questions**: each gap, with what is missing and where it appears. This list is the index of the inline gap markers; each gap is one marker plus one entry here.
3. **Cut or moved**: anything removed from the inventory, with the reason ("repeated in section 2", "chat residue").
4. **Reader assumed**: one line with the purpose and reader you edited for.

## Check before delivery

Run `python3 -I ${CLAUDE_PLUGIN_ROOT}/skills/productivity/uncomplicate/scripts/check_html.py <file>`. It reports: unreplaced `{{…}}` markers, a missing `lang`, `<title>` or viewport tag, a missing print stylesheet, an `<h1>` count other than one, skipped heading levels, duplicate `id`s, `#` links with no target, and anything executable or external. Fix and re-run it until it prints `OK`. It doesn't check meaning or visual layout; those are steps 7 and 8 of the workflow. Two heuristics guard the editor layer: a gap box or text starting "Open question" outside an `editor` element fails, and so does an `editor` element that holds no gap box or notes, because its content would vanish from print. They catch the usual slips, not every one.
