from rich.highlighter import RegexHighlighter


class DescriptionHighlighter(RegexHighlighter):
    base_style = "repr."
    highlights = [
        r"(?P<url>https?://[^\s]+)",
        r"(?P<number>\d+(\.\d+)+)",
        r"(?P<str>\"[^\"]+\")"
    ]
