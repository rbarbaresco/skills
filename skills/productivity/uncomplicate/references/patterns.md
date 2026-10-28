# Patterns worth checking

Each pattern costs the reader something. Edit it only when it does. None of these is a ban: a careful writer uses every one of them on purpose sometimes, so each comes with a "leave it" case. One sighting in a human-written document is rarely enough; a repeated habit is.

## Structure (fix these first)

| Pattern | What it costs the reader | Fix | Leave it when |
|---|---|---|---|
| **Buried decision or conclusion.** The ask, the result or the decision sits in the last paragraph. | They read everything before learning why. | Move it to the top, keep the reasoning after it. | The document is a narrative or a teaching sequence where the conclusion depends on build-up. |
| **Use before definition.** A term, acronym or number is used paragraphs before it is explained. | They stop, guess, or scroll. | Define it at, or before, first use. | The term is common for this reader. |
| **Thesis restated.** The same claim appears in the intro, the body and the conclusion in near-identical words. | Re-reading what they already know. | State it once, where it belongs. | A long document's summary deliberately serves skimmers. Keep one summary, not three. |
| **Forecast outline.** "This document covers X, then Y, then Z," followed by X, Y and Z. | A table of contents in prose. | Cut it, or use a real TOC for long documents. | The reader needs to pick a section, and there is no TOC. |
| **Split topic.** One subject spread over three places, mixed with others. | Assembling it themselves. | Group it. | The document's order is fixed (legal clauses, numbered steps). |
| **Templated items.** Every list item or section built from the same mold, often with a bold label. | Scanning labels that carry no information. | Plain sentences, or a table if items really share fields. | Items really are parallel records. |
| **Empty framing.** Openers ("In today's fast-paced world"), send-offs ("The future looks bright"), headings that restate the next sentence. | Reading words with no content. | Cut. Start with the first real fact; end on the last. | Never, unless it is a quote. |
| **Carryover context.** "As discussed", "the other approach", "per the earlier thread": references to something the reader has not seen. | Missing context they cannot recover. | Flag it as a gap, unless the document itself explains it elsewhere. | The reader certainly has that context (a reply in a thread). |

## Wording

| Pattern | Fix | Leave it when |
|---|---|---|
| **Shifting terms.** One thing called "client", "customer" and "account" in turn. | Pick one term and use it everywhere; mention the alias once if readers know both. | The words really name different things. Then make that explicit. |
| **Dangling "this", "it", "that".** | Name the thing. | The referent is the one noun in the previous sentence. |
| **Inflated words and claims.** "Pivotal", "robust", "seamless", "leverage", "unlock", "a testament to". | State the specific property or cut it. | The word is used in its technical sense (a robust estimator, a key in a map). |
| **Staged contrast.** "It's not just X, it's Y" when nobody claimed X. | Say Y. | X is a belief the reader actually holds. |
| **Stacked hedges.** "Could potentially possibly." | One hedge, if the uncertainty is real. | Never collapse a real, specific uncertainty. "Preliminary results suggest" is information. |
| **Nominalizations and hidden actors.** "A decision was made to perform a migration." | "We decided to migrate." Name who. | The actor is unknown, and then say so if it matters. |
| **Long tangled sentences.** Several ideas joined by "and", "which" and dashes. | Split into one idea per sentence. | The ideas really are one thought, and splitting breaks the logic. |
| **Chat residue.** "Great question!", "I hope this helps", "Let me know if…". | Cut. | It is a real letter's greeting or sign-off. |

## Words a second-language reader trips on

The reader may be reading in their second language. Each of these makes them stop and decode, so replace it with a plain, literal version that keeps the meaning. Not in an already-clear document: there, leave the wording alone (see SKILL.md).

| Pattern | Instead | Leave it when |
|---|---|---|
| **Idioms and figures of speech.** "Ballpark figure", "low-hanging fruit", "on the same page", "drop the ball". | "Rough estimate", "easy first fixes", "agree", "miss". | It is quoted speech or a name. |
| **Phrasal verbs** with a one-word equivalent. "Call off", "come across", "put off", "figure out". | "Cancel", "find", "delay", "work out" or "understand". | The phrasal verb is the common form and the alternative is rarer ("log in", "set up", "back up" in software). |
| **Rare or formal words.** "Commence", "utilize", "ascertain", "forthwith", "aforementioned". | "Start", "use", "find out", "now", "this". | The term is legal or technical and the reader must recognize it. Then explain it once, from its dictionary meaning. |
| **Unexplained abbreviations** and in-group shorthand. "EOD", "WFH", "TBD", "LGTM". | Spell it out the first time, or use the plain phrase. | The abbreviation is the common name (API, PDF, URL). |
| **Negatives stacked or delayed.** "Not unlikely", "it is not the case that we won't". | Say it positively: "likely", "we will". | The double negative carries a real nuance the source intends. Then keep it, and flag it if it is unclear. |
| **Cultural references, irony, humour that depends on wordplay.** | State the point directly. | It is the author's voice in a personal piece and the meaning is clear without it. |

## What not to do

- **Don't apply mechanical rules.** No dash bans, no "always shorter", no "always add a summary", no "everything into bullets". Each would make some documents worse.
- **Don't swap one cliché for another.** Rewrite the sentence around its actual point.
- **Don't strip voice.** A specific odd detail, a real aside, or a stated mixed feeling is the author's, and it often carries meaning.
- **Don't optimize for AI detectors**, and never add deliberate errors or "imperfections".

## Sources of ideas

These patterns draw on ideas from clarify-doc (Aleksander Jaworski, MIT), declaude (AbhinavMir, MIT), humanizer (Siqi Chen, MIT) and Wikipedia's "Signs of AI writing" guide. The wording here is original.
