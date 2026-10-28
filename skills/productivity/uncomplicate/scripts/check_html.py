#!/usr/bin/env python3
"""Check an uncomplicate HTML output for structure and safety problems.

Usage: check_html.py FILE [FILE...]   prints OK or one failure per line; exit 1 on any failure.
       check_html.py --self-test
Standard library only. It does not judge meaning or visual layout, and the editor-layer
checks are heuristics: they catch the usual mistakes, not every one.
"""
import re
import sys
from html.parser import HTMLParser
from urllib.parse import unquote

# Every tag the template and html.md use. Anything else is either unsafe (script, svg, img, link)
# or source text that was not escaped (<user-id>, List<String>), which a browser would swallow.
ALLOWED_TAGS = set("""html head meta title style body main article section nav header footer
    details summary h1 h2 h3 h4 h5 h6 p ul ol li dl dt dd table thead tbody tfoot tr th td caption
    colgroup col div span a strong em b i u s small sub sup mark abbr dfn q cite code pre kbd samp
    var blockquote figure figcaption hr br wbr aside time del ins""".split())
VOID_TAGS = {"meta", "br", "wbr", "hr", "col"}
URL_ATTRS = {"href", "xlink:href", "src", "srcset", "poster", "data", "background", "action",
             "formaction", "ping"}
SAFE_SCHEMES = {"http", "https", "mailto", "tel"}
SCHEME = re.compile(r"^([a-z][a-z0-9+.-]*):", re.I)
# Browsers strip ASCII whitespace and control characters from URLs before reading the scheme.
URL_JUNK = re.compile(r"[\x00-\x20\x7f]")
# Any of these in CSS can load something, or hide a load behind an escape.
CSS_LOADS = re.compile(r"url\s*\(|image-set|@import|@font-face|expression\s*\(|\\", re.I)
# The template's gap label. A source's own "Open question 1:" has no colon right after "question".
EDITOR_TEXT = re.compile(r"^\s*open question:", re.I)
# Page-structure tags: once <body> has opened, one of these is source text that was not escaped.
HEAD_ONLY = {"html", "head", "body", "title", "style", "meta"}


class Checker(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.fails, self.ids, self.anchors, self.headings = [], [], [], []
        self.lang = self.viewport = False
        self.title, self.style = "", ""
        self._in = None
        self._stack = []  # [tag, is_editor, holds_editor_content]
        self._body = False

    def _editor_depth(self):
        return any(f[1] for f in self._stack)

    def handle_starttag(self, tag, attrs):
        pairs = [(k.lower(), v or "") for k, v in attrs]
        a = dict(reversed(pairs))  # browsers keep the first of duplicate attributes
        if tag not in ALLOWED_TAGS:
            self.fails.append(f"tag <{tag}> not allowed (unsafe, or source text that needs escaping as &lt;{tag}&gt;)")
        elif self._body and tag in HEAD_ONLY:
            self.fails.append(f"<{tag}> inside the body: source text that needs escaping as &lt;{tag}&gt;")
        if tag == "body":
            self._body = True
        if tag == "a" and "href" not in a and "id" not in a:
            self.fails.append("<a> with no href or id: source text that needs escaping as &lt;a&gt;?")
        if tag == "details" and "editor" not in a.get("class", "").split() and not self._editor_depth():
            self.fails.append("<details> outside the editor layer: its content would not print")
        for k, v in pairs:
            if k.startswith("on"):
                self.fails.append(f"event attribute {k}= on <{tag}>")
            if k == "ping":
                self.fails.append(f"ping= on <{tag}>")
            if k in URL_ATTRS and k not in ("href", "xlink:href") and v and not v.startswith("#"):
                self.fails.append(f"loads a resource: <{tag} {k}={v[:60]}>")
            if k in ("href", "xlink:href"):
                m = SCHEME.match(URL_JUNK.sub("", v))
                if m and m.group(1).lower() not in SAFE_SCHEMES:
                    self.fails.append(f"link scheme not allowed in {k}= on <{tag}>: {v[:60]!r}")
            if k == "style" and CSS_LOADS.search(v):
                self.fails.append(f"style= on <{tag}> can load a resource: {v[:60]}")
            if k == "http-equiv":
                self.fails.append(f"<meta http-equiv> not allowed: {a.get('content', '')[:60]}")
        classes = a.get("class", "").split()
        is_editor = "editor" in classes
        editor_only = "gap" in classes or "editing-notes" in classes
        if editor_only and not (is_editor or self._editor_depth()):
            self.fails.append(f"editor-only <{tag} class={a.get('class')}> is outside the editor layer, so it would print")
        if editor_only:
            for f in self._stack:
                f[2] = True
        if tag == "a" and "href" in a:
            href = a["href"].strip()
            if href.startswith("#") and len(href) > 1:
                self.anchors.append(unquote(href[1:]))
        if tag == "html" and a.get("lang", "").strip() and "{{" not in a["lang"]:
            self.lang = True
        if tag == "meta" and a.get("name", "").lower() == "viewport":
            self.viewport = True
        if "id" in a:
            self.ids.append(a["id"])
            if re.search(r"\s", a["id"]):
                self.fails.append(f"id with whitespace: {a['id']!r}")
        if re.fullmatch(r"h[1-6]", tag):
            self.headings.append(int(tag[1]))
        if tag in ("title", "style"):
            self._in = tag
        if tag not in VOID_TAGS:
            self._stack.append([tag, is_editor, editor_only])

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID_TAGS and self._stack and self._stack[-1][0] == tag:
            self._close(self._stack.pop())

    def _close(self, frame):
        if frame[1] and not frame[2]:
            self.fails.append(f"<{frame[0]} class=editor> holds no gap or notes: editor content never prints, so document text there would be lost")

    def handle_endtag(self, tag):
        if tag == self._in:
            self._in = None
        if any(f[0] == tag for f in self._stack):
            while self._stack:
                frame = self._stack.pop()
                self._close(frame)
                if frame[0] == tag:
                    break

    def handle_data(self, data):
        if self._in == "title":
            self.title += data
        elif self._in == "style":
            self.style += data
        elif EDITOR_TEXT.match(data) and not self._editor_depth():
            self.fails.append(f"editor text outside the editor layer, so it would print: {data.strip()[:60]!r}")


def check(text):
    c = Checker()
    c.feed(text)
    c.close()
    f = c.fails
    if "{{" in text and re.search(r"\{\{[A-Z_]+\}\}", text):
        f.append("unreplaced template marker: " + ", ".join(sorted(set(re.findall(r"\{\{[A-Z_]+\}\}", text)))))
    if not c.lang:
        f.append("<html> has no lang attribute")
    if not c.title.strip():
        f.append("empty or missing <title>")
    if not c.viewport:
        f.append("no viewport <meta>")
    if "@media print" not in c.style:
        f.append("no @media print rules")
    if CSS_LOADS.search(c.style):
        f.append("stylesheet can load an external resource (url(), image-set, @import, @font-face or a CSS escape)")
    if c.headings.count(1) != 1:
        f.append(f"expected exactly one <h1>, found {c.headings.count(1)}")
    for prev, cur in zip(c.headings, c.headings[1:]):
        if cur > prev + 1:
            f.append(f"heading level skips from h{prev} to h{cur}")
    dupes = sorted({i for i in c.ids if c.ids.count(i) > 1})
    if dupes:
        f.append("duplicate ids: " + ", ".join(dupes))
    for a in sorted(set(c.anchors) - set(c.ids)):
        f.append(f"internal link #{a} has no target")
    return f


# (snippet injected into a passing page, whether a correct checker fails it). Includes the bypasses
# and false positives found in review.
CASES = [
    ("<script>x</script>", True), ("<SCRIPT>alert(1)</SCRIPT>", True),
    ('<img src="https://x/y.png">', True), ('<p onclick="x">', True), ("<svg onload=alert(1)></svg>", True),
    ('<a href="javascript:alert(1)">x</a>', True), ('<a href=" javascript:alert(1)">x</a>', True),
    ('<a href="&#106;avascript:alert(1)">x</a>', True), ('<a href="java&#9;script:alert(1)">x</a>', True),
    ('<map name=m><area href="java&#9;script:alert(1)"></map>', True),
    ('<svg><a xlink:href="java&#9;script:alert(1)"><text>x</text></a></svg>', True),
    ('<svg><image href="https://evil.example/p.png"/></svg>', True),
    ('<svg><use href="https://evil.example/s.svg#a"/></svg>', True),
    ('<link rel=icon href=favicon.png>', True), ('<link rel=prefetch href="/x">', True),
    ("<style>body{background:url(//evil.example/x.png)}</style>", True),
    (r"<style>body{background:u\72l(https://evil.example/x.png)}</style>", True),
    ('<style>body{background-image:image-set("https://evil.example/x.png" 1x)}</style>', True),
    ('<style>@font-face{font-family:x;src:url("https://evil.example/f.woff")}</style>', True),
    ('<p style="background:url(https://evil.example/x.png)">x</p>', True),
    ('<meta http-equiv="refresh" content="0;url=https://evil.example/">', True),
    ('<a href="https://ok.example" ping="https://evil.example/track">x</a>', True),
    ('<a href="data:text/html;base64,PHNjcmlwdD4=">x</a>', True),
    ('<math><mi href="javascript:alert(1)">x</mi></math>', True),
    ("<p>GET /users/<user-id>/keys</p>", True), ("<pre><code>List<String> xs;</code></pre>", True),
    ("<p>use <textarea> for input</p>", True), ('<a href="#nope">', True), ("<h5>x</h5>", True),
    ("{{BODY}}", True), ('<aside class="gap">x</aside>', True), ("<h1>Notes</h1>", True),
    ("<p><strong>Open question:</strong> who owns this?</p>", True),
    ('<p class="editor">Dosage: 5 mg daily.</p>', True),
    ('<h3 id="my section">x</h3><a href="#my section">go</a>', True),
    ('<div class="editor"><aside class="gap">x</aside></div>', False),
    ('<aside class="gap editor"><p><strong>Open question:</strong> who?</p></aside>', False),
    ('<h3 id="über-uns">x</h3><a href="#%C3%BCber-uns">go</a>', False),
    ('<a href="#">top</a>', False), ('<a href="other.html">x</a>', False),
    ('<a href="../docs/x.md#setup">x</a>', False), ('<a href="tel:+15551234">call</a>', False),
    ('<p>a<br>b<br/>c</p><hr><p>&lt;user-id&gt; and List&lt;String&gt;</p>', False),
    ("<p>put the name in the <title> element</p>", True), ("<p>a <style> block</p>", True),
    ("<p>wrap it in <body></p>", True), ('<a href="javascript:alert(1)" href="https://ok">x</a>', True),
    ("<p>use <a> for links</p>", True), ("<details><summary>More</summary><p>5 mg daily</p></details>", True),
    ('<section class="editing-notes editor"><details><summary>N</summary></details></section>', False),
    ("<p>Open question 1: do we shard?</p>", False), ("<p>Note to the author: keep this.</p>", False),
    ('<p>Dose<sup><a href="#fn1" id="r1">1</a></sup></p><dl><dt>T</dt><dd>D</dd></dl><p id="fn1">x</p>', False),
]


def self_test():
    good = ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="x">'
            '<title>T</title><style>@media print{a{}}</style></head><body><h1>T</h1><p><a href="#s">go</a> '
            '&lt;script&gt;alert(1)&lt;/script&gt; <a href="https://example.com">src</a></p>'
            '<h2 id="s">S</h2><h3 id="t">T</h3>INJECT</body></html>')
    assert check(good.replace("INJECT", "")) == [], check(good.replace("INJECT", ""))
    wrong = []
    for snippet, should_fail in CASES:
        out = check(good.replace("INJECT", snippet))
        if bool(out) != should_fail:
            wrong.append((snippet, out))
    assert check(good.replace("INJECT", "").replace('lang="en"', 'lang=" "'))
    assert not wrong, "\n".join(f"{s!r}: {o}" for s, o in wrong)
    print(f"self-test OK ({len(CASES)} cases)")


def main(argv):
    if argv == ["--self-test"]:
        return self_test()
    if not argv:
        print(__doc__.strip())
        return 2
    failed = False
    for path in argv:
        with open(path, encoding="utf-8") as fh:
            fails = check(fh.read())
        prefix = f"{path}: " if len(argv) > 1 else ""
        if fails:
            failed = True
            for m in fails:
                print(f"{prefix}FAIL {m}")
        else:
            print(f"{prefix}OK")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
