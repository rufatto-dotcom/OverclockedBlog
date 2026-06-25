import re


class MdParser:
    """Lê um arquivo .md com front-matter e devolve (metadata, elements)."""

    def parse_file(self, path):
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
        metadata, body = self._extract_front_matter(text)
        elements = self._parse_body(body)
        return metadata, elements

    # ---------- front matter ----------
    # Espera um bloco assim no topo do arquivo:
    # ---
    # title: Como funciona um parser de Markdown
    # tag: C
    # date: jun 2026
    # ---

    def _extract_front_matter(self, text):
        metadata = {"title": "", "tag": "", "date": ""}
        lines = text.split("\n")

        if lines and lines[0].strip() == "---":
            end = None
            for i in range(1, len(lines)):
                if lines[i].strip() == "---":
                    end = i
                    break
            if end is not None:
                for line in lines[1:end]:
                    if ":" in line:
                        key, value = line.split(":", 1)
                        metadata[key.strip()] = value.strip()
                body = "\n".join(lines[end + 1:])
                return metadata, body

        return metadata, text

    # ---------- corpo do markdown ----------

    def _parse_body(self, text):
        lines = text.split("\n")
        elements = []
        i = 0
        n = len(lines)

        while i < n:
            line = lines[i]
            stripped = line.strip()

            if not stripped:
                i += 1
                continue

            # bloco de código: ```lang ... ```
            if stripped.startswith("```"):
                lang = stripped[3:].strip()
                code_lines = []
                i += 1
                while i < n and not lines[i].strip().startswith("```"):
                    code_lines.append(lines[i])
                    i += 1
                i += 1  # pula a linha de fechamento ```
                elements.append({
                    "type": "code",
                    "lang": lang,
                    "content": "\n".join(code_lines)
                })
                continue

            # divisor: --- (3 ou mais hifens, linha isolada)
            if re.fullmatch(r"-{3,}", stripped):
                elements.append({"type": "hr"})
                i += 1
                continue

            # headings
            if stripped.startswith("#### "):
                elements.append({"type": "h4", "content": stripped[5:]})
                i += 1
                continue
            if stripped.startswith("### "):
                elements.append({"type": "h3", "content": stripped[4:]})
                i += 1
                continue
            if stripped.startswith("## "):
                elements.append({"type": "h2", "content": stripped[3:]})
                i += 1
                continue
            if stripped.startswith("# "):
                elements.append({"type": "h1", "content": stripped[2:]})
                i += 1
                continue

            # imagem: ![alt](src) numa linha isolada
            img_match = re.fullmatch(r"!\[(.*?)\]\((.*?)\)", stripped)
            if img_match:
                elements.append({
                    "type": "image",
                    "alt": img_match.group(1),
                    "src": img_match.group(2)
                })
                i += 1
                continue

            # blockquote: linhas começando com >
            if stripped.startswith(">"):
                quote_lines = []
                while i < n and lines[i].strip().startswith(">"):
                    quote_lines.append(lines[i].strip()[1:].strip())
                    i += 1
                elements.append({
                    "type": "blockquote",
                    "content": " ".join(quote_lines)
                })
                continue

            # tabela: linhas começando com |
            if stripped.startswith("|"):
                table_lines = []
                while i < n and lines[i].strip().startswith("|"):
                    table_lines.append(lines[i].strip())
                    i += 1
                elements.append(self._parse_table(table_lines))
                continue

            # lista (ul ou ol), com aninhamento por indentação
            list_match = re.match(r"^(\s*)([-*]|\d+\.)\s+", line)
            if list_match:
                top_ordered = list_match.group(2)[0].isdigit()
                list_lines = []
                while i < n and self._belongs_to_list(lines, i, top_ordered):
                    if lines[i].strip() != "":
                        list_lines.append(lines[i])
                    i += 1
                elements.append(self._parse_list(list_lines))
                continue

            # parágrafo: junta linhas seguidas até achar linha em branco
            # ou o começo de outro tipo de bloco
            para_lines = [stripped]
            i += 1
            while i < n and lines[i].strip() and not self._starts_new_block(lines[i]):
                para_lines.append(lines[i].strip())
                i += 1
            elements.append({"type": "p", "content": " ".join(para_lines)})

        return elements

    def _starts_new_block(self, line):
        stripped = line.strip()
        if stripped.startswith(("#", ">", "```", "|", "![")):
            return True
        if re.match(r"^(\s*)([-*]|\d+\.)\s+", line):
            return True
        if re.fullmatch(r"-{3,}", stripped):
            return True
        return False

    def _belongs_to_list(self, lines, i, top_ordered):
        n = len(lines)
        line = lines[i]

        if line.strip() == "":
            # linha em branco só "cola" a lista se a próxima linha
            # ainda for item de lista
            return i + 1 < n and bool(
                re.match(r"^(\s*)([-*]|\d+\.)\s+", lines[i + 1])
            )

        match = re.match(r"^(\s*)([-*]|\d+\.)\s+", line)
        if not match:
            return False

        indent = len(match.group(1))
        ordered = match.group(2)[0].isdigit()

        if indent == 0 and ordered != top_ordered:
            # mudou de ul pra ol (ou vice-versa) no nível raiz ->
            # é uma lista nova, não continuação desta
            return False

        return True

    # ---------- tabela ----------

    def _parse_table(self, table_lines):
        def split_row(row):
            cells = row.strip("|").split("|")
            return [c.strip() for c in cells]

        headers = split_row(table_lines[0])
        # table_lines[1] é a linha separadora (---|---|---), por isso pula
        rows = [split_row(r) for r in table_lines[2:]]
        return {"type": "table", "headers": headers, "rows": rows}

    # ---------- listas (com aninhamento) ----------

    def _parse_list(self, list_lines):
        first_match = re.match(r"^(\s*)([-*]|\d+\.)\s+", list_lines[0])
        ordered = first_match.group(2)[0].isdigit()
        root = {"type": "ol" if ordered else "ul", "items": []}
        stack = [(0, root)]

        for line in list_lines:
            match = re.match(r"^(\s*)([-*]|\d+\.)\s+(.*)", line)
            indent = len(match.group(1))
            content = match.group(3)
            is_ordered = match.group(2)[0].isdigit()

            # sobe na pilha enquanto a indentação atual for MENOR
            # que o nível em que estamos (volta pro pai)
            while len(stack) > 1 and indent < stack[-1][s0]:
                stack.pop()

            parent_indent, parent_node = stack[-1]

            if indent > parent_indent and parent_node["items"]:
                # item mais indentado que o anterior -> vira filho do último item
                last_item = parent_node["items"][-1]
                child_list = last_item.get("children")
                if child_list is None:
                    child_list = {"type": "ol" if is_ordered else "ul", "items": []}
                    last_item["children"] = child_list
                stack.append((indent, child_list))
                child_list["items"].append({"content": content, "children": None})
            else:
                parent_node["items"].append({"content": content, "children": None})

        return root