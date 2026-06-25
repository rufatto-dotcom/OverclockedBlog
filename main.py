from md_parser import MdParser
from html_renderer import HtmlRenderer

markdown = 'firstPost'
postFileName = 'firstPost'

def main():
    parser = MdParser()
    metadata, elements = parser.parse_file("projetos/" + markdown + ".md")

    renderer = HtmlRenderer()
    article_html = renderer.render(elements)

    with open("template.html", "r", encoding="utf-8") as f:
        template = f.read()

    placeholders = {
        "title": metadata.get("title", ""),
        "tag": metadata.get("tag", ""),
        "date": metadata.get("date", ""),
        "content": article_html,
        # navegação entre posts: ajuste manualmente por enquanto
        "prev_title": "",
        "prev_link": "#",
        "next_title": "",
        "next_link": "#",
    }

    for key, value in placeholders.items():
        template = template.replace(f"{{{{{key}}}}}", value)

    with open("posts/" + postFileName + ".html", "w", encoding="utf-8") as f:
        f.write(template)

    print("post.html gerado com sucesso.")


if __name__ == "__main__":
    main()