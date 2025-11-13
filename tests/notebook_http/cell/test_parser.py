# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import unittest
from unittest.mock import Mock
from kernel_gateway.notebook_http.cell.parser import APICellParser

class TestAPICellParser(unittest.TestCase):
    def test_markdown_cells_are_rendered(self):
        mock_markdown_cell = Mock()
        mock_markdown_cell.cell_type = "markdown"
        mock_markdown_cell.source = "# GET /try\n\nThis is a markdown cell."

        mock_code_cell = Mock()
        mock_code_cell.cell_type = "code"
        mock_code_cell.source = "# GET /hello\nprint('hello')"

        notebook_cells = [
            mock_markdown_cell,
            mock_code_cell
        ]
        parser = APICellParser(comment_prefix="#", notebook_cells=notebook_cells)
        endpoints = dict(parser.endpoints())
        self.assertEqual(len(endpoints), 2)
        self.assertIn("/hello", endpoints)
        self.assertIn("/try", endpoints)
        self.assertEqual(endpoints["/try"]["GET"]['cell_type'], "markdown")
        self.assertEqual(endpoints["/try"]["GET"]['source'], "<p>This is a markdown cell.</p>")