import re


class HtmlRenderer:
    """Transforma a lista de elementos do MdParser numa string HTML."""

    def render(self, elements):
        # estado por-render: zera a cada chamada, porque a numeração das
        # notas tem que ser global pro artigo inteiro, não por parágrafo
        self.footnotes = []
        self.footnote_counter = 0

        body = "\n".join(self._render_element(el) for el in elements)

        if self.footnotes:
            body += "\n" + self._render_footnotes()

        return body

    def _render_element(self, el):
        t = el["type"]
        if t == "h1":
            return f"<h1>{self._inline(el['content'])}</h1>"
        if t == "h2":
            return f"<h2>{self._inline(el['content'])}</h2>"
        if t == "h3":
            return f"<h3>{self._inline(el['content'])}</h3>"
        if t == "h4":
            return f"<h4>{self._inline(el['content'])}</h4>"
        if t == "p":
            return f"<p>{self._inline(el['content'])}</p>"
        if t == "hr":
            return "<hr>"
        if t == "blockquote":
            return f"<blockquote>\n<p>{self._inline(el['content'])}</p>\n</blockquote>"
        if t == "code":
            return self._render_code(el)
        if t == "image":
            return self._render_image(el)
        if t == "table":
            return self._render_table(el)
        if t in ("ul", "ol"):
            return self._render_list(el)
        return ""

    def _render_code(self, el):
        lang_class = f' class="lang-{el["lang"]}"' if el["lang"] else ""
        escaped = (
            el["content"]
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
        )
        return f"<pre><code{lang_class}>{escaped}</code></pre>"

    def _render_image(self, el):
        return (
            "<figure>\n"
            f'<img src="{el["src"]}" alt="{el["alt"]}">\n'
            f"<figcaption>{self._inline(el['alt'])}</figcaption>\n"
            "</figure>"
        )

    def _render_table(self, el):
        head_cells = "".join(f"<th>{self._inline(h)}</th>" for h in el["headers"])
        rows_html = []
        for row in el["rows"]:
            cells = "".join(f"<td>{self._inline(c)}</td>" for c in row)
            rows_html.append(f"<tr>\n{cells}\n</tr>")
        rows_str = "\n".join(rows_html)
        return (
            "<table>\n<thead>\n<tr>\n"
            f"{head_cells}\n"
            "</tr>\n</thead>\n<tbody>\n"
            f"{rows_str}\n"
            "</tbody>\n</table>"
        )

    def _render_list(self, el):
        tag = el["type"]
        items_html = []
        for item in el["items"]:
            content = self._inline(item["content"])
            if item.get("children"):
                child_html = self._render_list(item["children"])
                items_html.append(f"<li>{content}\n{child_html}\n</li>")
            else:
                items_html.append(f"<li>{content}</li>")
        items_str = "\n".join(items_html)
        return f"<{tag}>\n{items_str}\n</{tag}>"

    # ---------- notas de rodapé ----------
    # sintaxe no markdown: termo^[explicação do termo aqui]
    # gera um número clicável no texto e guarda o conteúdo pra
    # renderizar a lista de notas no final do artigo

    def _render_footnotes(self):
        items = "\n".join(
            f'<li id="fn{i}">{text} '
            f'<a href="#fnref{i}" class="footnote-back">↩</a></li>'
            for i, text in enumerate(self.footnotes, start=1)
        )
        return (
            '<section class="footnotes">\n'
            "<hr>\n"
            "<ol>\n"
            f"{items}\n"
            "</ol>\n"
            "</section>"
        )

    def _footnote_sub(self, match):
        self.footnote_counter += 1
        n = self.footnote_counter
        # formatação básica (negrito, código etc) é permitida dentro
        # da nota, mas não outra nota de rodapé aninhada
        self.footnotes.append(self._inline_basic(match.group(1)))
        return (
            '<sup class="footnote-ref">'
            f'<a href="#fn{n}" id="fnref{n}">{n}</a>'
            "</sup>"
        )

    # ---------- formatação inline ----------
    # roda dentro de qualquer texto: parágrafo, item de lista, célula de
    # tabela, legenda de imagem, etc.

    def _inline_basic(self, text):
        text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
        text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)
        text = re.sub(r"~~(.+?)~~", r"<del>\1</del>", text)
        text = re.sub(r"`(.+?)`", r"<code>\1</code>", text)
        text = re.sub(r"\[(.+?)\]\((.+?)\)", r'<a href="\2">\1</a>', text)
        return text

    def _inline(self, text):
        text = self._inline_basic(text)
        text = re.sub(r"\^\[(.+?)\]", self._footnote_sub, text)
        return text