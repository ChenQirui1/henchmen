from smolagents import Tool
import markdown
import re
from bs4 import BeautifulSoup
from bertopic import BERTopic


class MarkdownTool(Tool):
    name = "markdown_editor"
    description = "Edit and format markdown documents"
    inputs = {
        "content": {
            "type": "string",
            "description": "The markdown content to edit",
        },
        "operation": {
            "type": "string",
            "description": "The operation to perform on the markdown content",
            "enum": ["write", "update", "tagging", "linking"],
        },
        # "type": "dict",
        # "properties": {
        # "documents": {
        #     "items": {
        #         "type": "object",
        #         "properties": {
        #             "text": {"type": "string"},
        #             "metadata": {"type": "object"},
        #         },
        #     },
        # },
        # "operation": {"type": "string", "enum": ["format", "clean"]},
        # },
    }
    output_type = "string"

    def forward(self, content: str, operation: str) -> str:

        if operation == "write":
            content = self._write(content)
        elif operation == "update":
            content = self._update(content)
        elif operation == "tagging":
            content = self._tagging(content)
        elif operation == "linking":
            content = self._linking(content)

    def analyze(self, content: str) -> str:
        # Analyze content
        # derive topic from content
        # derive keywords from content

        return "Not implemented"

    def _write(self, content: str) -> str:
        # infer title from content

        print("Title:", title)

        with open(f"knowledge_base/{title}.md", "w") as f:
            f.write(content)
        return content

    def _update(self, content: str, title: str) -> str:

        # find existing file
        # if not found, create new file
        # reorganise content in file
        # write file

        with open(f"{title}.md", "a") as f:
            f.write(content)
        return content

    def _tagging(self, content: str) -> str:
        # add
        return "Not implemented"

    def _linking(self, content: str) -> str:
        # find

        return "Not implemented"


# Usage
# agent = CodeAgent(tools=[MarkdownTool()])
# response = agent.run("Format this markdown")
