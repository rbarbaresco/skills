# uncomplicate

Hand Claude a document that is hard to follow, whether that's dense, rambling, buried in AI filler, or just badly ordered, and get back a version its reader can follow on one read. The result comes as a standalone HTML page you can open, share or print.

**Type:** model-invoked. Claude uses it when you ask to make a document clearer, simpler or better organized. You can also call it by name: `/rbarbaresco-skills:uncomplicate`.

## Usage

```
uncomplicate docs/rate-limit-spec.md — it's going to partner engineers who don't know our internals
```

```
this email is impossible to follow, can you clean it up so the team gets what was decided?
```

It works on human-written text as well as AI-heavy text. If the reader or purpose isn't clear from the document and the answer would change the rewrite, Claude asks; otherwise it infers them and tells you what it assumed.

## What you get

- **`<name>.uncomplicated.html`** next to the source (or `uncomplicated.html` for pasted text). It's one self-contained file: no scripts, no external fonts or images, readable on a phone, with dark mode and print styles. Long documents get a linked table of contents.
- **Plain English for every reader.** On documents that need a rewrite, it writes as if the reader's first language were something else: common words, no idioms, short sentences, one name for each thing. That makes it easy for everyone.
- **Two layers in one page.** Your notes (what changed, open questions) show on screen, collapsed, and are left out when you print or save as PDF, so the printout is ready to share.
- **Gaps flagged in place.** Where the document refers to something it never gives (a threshold, a missing section, "the numbers above"), the page marks it instead of making something up. In a plan or spec sent for review, the gaps also go in an "Open items" list that prints, because the reviewers decide them.
- A short handoff in chat with the path and the changes that matter.

## What it won't do

- It won't drop a fact, number, qualification or citation. "Only in adults under 65" survives simplification.
- It won't invent facts, numbers, examples or decisions to fill a gap. It may explain a stated fact in plainer words.
- It won't apply blanket rules: no dash bans, no forced bullet points, no "always shorter". A clear explanation sometimes needs more words.
- It won't rewrite a document that is already clear. It says so and changes little.
- It won't translate (unless asked), fact-check, write a document from scratch, or try to beat AI detectors.

## How it works

Structure before wording: Claude states the reader and the core message, lists every fact and qualification, reorganizes (conclusion first where it helps, definitions before use, duplicates merged), then fixes wording (one term per concept, plain words, jargon explained). It checks the draft against the fact list, renders the page from a fixed template, and runs `scripts/check_html.py` (standard-library Python). It allows only the tags the template uses, so it catches most unescaped markup, like `<user-id>` or a stray `<title>` (not ordinary element names like `<p>`), scripts and anything that would load from the network, as well as broken internal links and skipped heading levels.

## Credits

The editing approach draws on ideas from [clarify-doc](https://github.com/jaal/claude-code-skills) (MIT), [declaude](https://github.com/AbhinavMir/declaude) (MIT), [humanizer](https://github.com/blader/humanizer) (MIT), Anthropic's [doc-coauthoring](https://github.com/anthropics/skills) skill (its reader test) and Wikipedia's [Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing). No text was copied.
