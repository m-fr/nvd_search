from textual.widgets import DataTable


class Table(DataTable):
    """Custom DataTable widget for NVD Search.
    """

    COLUMNS = []

    def __init__(self, id: str = "table"):
        super().__init__(zebra_stripes=True, id=id)
        self.styles.height = '10fr'
        for column in self.COLUMNS:
            self.add_column(column)


class CveTable(Table):
    """Custom DataTable widget for CVEs.
    """

    COLUMNS = ["#", "CVE ID", "Risk", "Description", "Link"]

    def __init__(self):
        super().__init__(id="cve_table")


class CpeTable(Table):
    """Custom DataTable widget for CPEs.
    """

    COLUMNS = ["#", "CPE"]

    def __init__(self):
        super().__init__(id="cpe_table")
