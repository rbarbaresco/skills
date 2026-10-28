#!/usr/bin/env python3
"""Check an uncomplicate HTML output for structure and safety problems.

Usage: check_html.py FILE [FILE...]   prints OK or one failure per line; exit 1 on any failure.
       check_html.py --self-test
Standard library only. It does not judge meaning or visual layout.
"""
import re
import sys
from html.parser import HTMLParser

BANNED_TAGS = {"script", "iframe", "object", "embed", "form", "base", "frame", "frameset", "applet"}
LOADING_ATTRS = {"src", "srcset", "poster", "data", "background", "action", "formaction"}
SAFE_LINK = re.compile(r"^(https?:|mailto:|#)", re.I)
EXTERNAL = re.compile(r"^\s*(https?:)?//", re.I)


class Checker(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.fails, self.ids, self.anchors, self.headings = [], [], [], []
        self.lang = self.viewport = False
        self.title, self.style = "", ""
        self._in = None

    def handle_starttag(self, tag, attrs):
        a = {k.lower(): (v or "") for k, v in attrs}
        if tag in BANNED_TAGS:
            self.fails.append(f"banned tag <{tag}>")
        for k, v in a.items():
            if k.startswith("on"):
                self.fails.append(f"event attribute {k}= on <{tag}>")
            if re.match(r"^\s*(javascript|vbscript|data):", v, re.I) and k in LOADING_ATTRS | {"href", "xlink:href"}:
                self.fails.append(f"unsafe URL in {k}= on <{tag}>: {v[:40]}")
            if k in LOADING_ATTRS and v and not v.startswith("#"):
                self.fails.append(f"loads a resource: <{tag} {k}={v[:60]}>")
        classes = a.get("class", "").split()
        if ("gap" in classes or "editing-notes" in classes) and "editor" not in classes:
            self.fails.append(f"editor-only <{tag} class={a.get('class')}> lacks the editor class, so it would print")
        if tag == "a" and "href" in a:
            href = a["href"].strip()
            if href.startswith("#"):
                self.anchors.append(href[1:])
            elif href and not SAFE_LINK.match(href):
                self.fails.append(f"link scheme not allowed: {href[:60]}")
        if tag == "link" and (EXTERNAL.match(a.get("href", "")) or "stylesheet" in a.get("rel", "").lower()):
            self.fails.append(f"external <link>: {a.get('href', '')[:60]}")
        if tag == "html" and a.get("lang", "").strip() and "{{" not in a["lang"]:
            self.lang = True
        if tag == "meta" and a.get("name", "").lower() == "viewport":
            self.viewport = True
        if "id" in a:
            self.ids.append(a["id"])
        if re.fullmatch(r"h[1-6]", tag):
            self.headings.append(int(tag[1]))
        if tag in ("title", "style"):
            self._in = tag

    def handle_endtag(self, tag):
        if tag == self._in:
            self._in = None

    def handle_data(self, data):
        if self._in == "title":
            self.title += data
        elif self._in == "style":
            self.style += data


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
    if re.search(r"@import|url\(\s*['\"]?\s*(https?:)?//", c.style, re.I):
        f.append("stylesheet loads an external resource")
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


def self_test():
    good = ('<!doctype html><html lang="en"><head><meta name="viewport" content="x"><title>T</title>'
            '<style>@media print{a{}}</style></head><body><h1>T</h1><p><a href="#s">go</a> '
            '&lt;script&gt;alert(1)&lt;/script&gt; <a href="https://example.com">src</a></p>'
            '<h2 id="s">S</h2><h3 id="t">T</h3></body></html>')
    assert check(good) == [], check(good)
    bad = {
        "<script>x</script>": "banned tag <script>",
        '<img src="https://x/y.png">': "loads a resource",
        '<p onclick="x">': "event attribute",
        '<a href="javascript:alert(1)">': "unsafe URL",
        '<a href="#nope">': "has no target",
        "<h5>x</h5>": "skips from h3 to h5",
        "{{BODY}}": "unreplaced",
        '<aside class="gap">x</aside>': "lacks the editor class",
        '<link rel="stylesheet" href="https://f">': "external <link>",
    }
    for snippet, expect in bad.items():
        out = check(good.replace("</body>", snippet + "</body>"))
        assert any(expect in m for m in out), (snippet, out)
    assert any("@import" in m or "external" in m for m in check(good.replace("@media", "@import url(x);@media")))
    print("self-test OK")


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
