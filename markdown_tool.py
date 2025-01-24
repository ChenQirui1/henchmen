from smolagents import Tool, CodeAgent
import markdown
import re
from bs4 import BeautifulSoup


class MarkdownTool(Tool):
    name = "markdown_editor"
    description = "Edit and format markdown documents"
    parameters = {
        "type": "object",
        "properties": {
            "content": {"type": "string", "description": "Markdown content to edit"},
            "operation": {
                "type": "string",
                "enum": ["format", "clean", "extract_links", "tagging", "linking"],
            },
        },
    }

    def _run(self, content: str, operation: str) -> str:
        if operation == "format":
            return self._format_markdown(content)
        elif operation == "clean":
            return self._clean_markdown(content)
        elif operation == "extract_links":
            return self._extract_links(content)
        elif operation == "tagging":
            return "Not implemented"
        elif operation == "linking":
            return "Not implemented"
        return "Invalid operation"

    def _format_markdown(self, content: str) -> str:
        content = re.sub(r"#+([^ ])", r"# \1", content)
        content = re.sub(r"^(-|\*|\+)([^ ])", r"\1 \2", content, flags=re.M)
        return content

    def _clean_markdown(self, content: str) -> str:
        content = re.sub(r"\n{3,}", "\n\n", content)
        content = re.sub(r"^[-\*\+]", "-", content, flags=re.M)
        return content

    def _extract_links(self, content: str) -> str:
        html = markdown.markdown(content)
        soup = BeautifulSoup(html, "html.parser")
        links = [f"{a.text}: {a['href']}" for a in soup.find_all("a")]
        return "\n".join(links)

    def _tagging(self, content: str) -> str:
        """this method will tag the content, i.e. adding #tags to the subcontent

        Args:
            content (str): _description_

        Returns:
            str: _description_
        """

        return "Not implemented"


# Usage
# agent = CodeAgent(tools=[MarkdownTool()])
# response = agent.run("Format this markdown")
