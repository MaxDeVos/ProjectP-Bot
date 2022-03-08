from markdownify import markdownify


def html_to_markdown(text):
    return markdownify(str(text)).replace("\n\n\n", "\n").replace("\n\n", "\n")


# TODO - To Embed Maybe?
class CategoryParser:
    def __init__(self, html_content, title):
        self.src = html_content
        self.title = title

    def to_markdown(self):
        return html_to_markdown(self.title) + html_to_markdown(self.src)