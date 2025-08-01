from textual import on
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Footer, Input, TabbedContent, TabPane, DataTable, Button, RadioButton, RadioSet, Label
from textual.containers import Container
from requests.exceptions import HTTPError

from nvd_search.search import search_by_keyword, search_cpe_by_keyword, search_by_cpe
from nvd_search.vulnerability import Vulnerability
from nvd_search.tui.table import Table, CveTable, CpeTable


class Tui(App):
    """A Textual User Interface for NVD Search.
    """
    BINDINGS = [
        Binding("q", "quit", "Quit the app")
    ]

    CPE_TYPES = ["*", "a", "o", "h", "-"]

    def compose(self) -> ComposeResult:
        """Create the app UI.
        """
        with TabbedContent():
            with TabPane("CPE", id="cpe"):
                with RadioSet(id="cpe_type"):
                    yield RadioButton("Any")
                    yield RadioButton("Application")
                    yield RadioButton("Operating System")
                    yield RadioButton("Hardware")
                    yield RadioButton("Not Applicable")
                with Container(id="cpe_input"):
                    yield Input(placeholder="Enter the vendor name", id="vendor")
                    yield Input(placeholder="Enter the product name", id="product")
                    yield Input(placeholder="Enter the product version", id="version")
                yield Button("Search", id="search_cpe")
                yield CpeTable()
            with TabPane("CVE", id="cve"):
                yield Input(placeholder="Enter the keyword to search", id="keyword")
                yield CveTable()
        with Footer(show_command_palette=False, id="footer"):
            yield Label("Ready. Press 'q' to quit.", id="status")

    def on_mount(self) -> None:
        self.query_one("#cpe_type", RadioSet).styles.layout = "horizontal"
        self.query_one("#cpe_input", Container).styles.layout = "horizontal"
        for input in self.query_one("#cpe_input", Container).children:
            input.styles.width = "1fr"

    @on(Button.Pressed, "#search_cpe")
    @on(Input.Submitted, "#vendor")
    @on(Input.Submitted, "#product")
    @on(Input.Submitted, "#version")
    def process_wizard(self, event: Button.Pressed) -> None:
        """Search for the CPE based on the wizard input.
        """
        cpe_type = self.query_one("#cpe_type", RadioSet).pressed_index
        vendor = self.query_one("#vendor", Input).value
        product = self.query_one("#product", Input).value
        version = self.query_one("#version", Input).value
        cpe = ":".join([
            "cpe:2.3",
            self.CPE_TYPES[cpe_type] if cpe_type > 0 else "*",
            vendor if vendor else "*",
            product if product else "*",
            version if version else "*"
        ])
        try:
            result = search_cpe_by_keyword(keyword=cpe)
        except HTTPError as e:
            self.query_one("#status", Label).update(f"HTTP Error: {e}")
        else:
            table = self.query_one("#cpe_table", Table)
            table.clear()
            for i, cpe in enumerate(result):
                row = [str(i), cpe]
                table.add_row(*row)

    @on(Input.Submitted, "#keyword")
    def process_search(self, event: Input.Submitted) -> None:
        """Search for the keyword based on active pane.
        """
        keyword = event.value
        pane = self.query_one(TabbedContent).active_pane.id

        if pane == "cpe":
            self.search_cpe(keyword)
        elif pane == "cve":
            self.search_cve(keyword)

    @on(DataTable.CellSelected, "#cpe_table")
    def process_cpe_selection(self, event: DataTable.CellSelected) -> None:
        """Search for the selected CPE.
        """
        row = event.data_table.get_row(event.cell_key[0])
        table = self.query_one("#cve_table", Table)
        try:
           result = search_by_cpe(row[1])
        except HTTPError:
            print("HTTP Error")
        else:
           table.clear()
           for idx, vuln in enumerate(result):
               row = [str(idx)] + Vulnerability.from_dict(vuln).to_annotation()
               table.add_row(*row)

    def search_cpe(self, keyword: str) -> None:
        """Search for the keyword in CPE.
        """
        result = search_cpe_by_keyword(keyword=keyword)
        table = self.query_one("#cpe_table", Table)
        table.clear()
        for idx, cpe in enumerate(result):
            row = [str(idx), cpe]
            table.add_row(*row)

    def search_cve(self, keyword: str) -> None:
        """Search for the keyword in CVE.
        """
        result = search_by_keyword(keyword=keyword)
        table = self.query_one("#cve_table", Table)
        table.clear()
        for idx, vuln in enumerate(result):
            row = [str(idx)] + Vulnerability.from_dict(vuln).to_annotation()
            table.add_row(*row)

    def quit(self) -> None:
        """Quit the app.
        """
        self.exit()
