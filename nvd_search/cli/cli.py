import click

from rich import print
from rich.tree import Tree
from rich.prompt import Prompt

from semver import Version

from nvd_search.__version__ import __version__
from nvd_search.cli.console import Console
from nvd_search.cli.utils import AliasedGroup, handle_exceptions
from nvd_search.search import search_by_cpe, search_by_keyword, search_by_cve_id, search_by_prod, search_by_ver


@click.group(cls=AliasedGroup, context_settings={'help_option_names': ['-h', '--help']})
@click.version_option(version=__version__)
def cli():
    """NVD Search Tool.
    """


@cli.command()
@handle_exceptions
def cpe():
    """Search for CVEs of against specific CPE - type, vendor name, product, and version.
    """
    tree = Tree("CPE type hint")
    tree.add("[bold]a[/] application")
    tree.add("[bold]o[/] operating system ")
    tree.add("[bold]h[/] hardware ")
    tree.add("[bold]p[/] others")
    Console().print(tree)

    cpe_type = Prompt.ask("Enter the CPE type", choices=['a', 'o', 'h', 'p'], default='a')
    vendor_name = Prompt.ask("Enter the vendor name")
    product_name = Prompt.ask("Enter the product name")

    # Ask the user to supply the CPE version
    while True:
        version = Prompt.ask("Enter the product version")
        if Version.is_valid(version):
            break
        print("[prompt.invalid]Please enter a valid version.")

    cpe_name = f"cpe:2.3:{cpe_type}:{vendor_name}:{product_name}:{version}"
    search_by_cpe(cpe_name=cpe_name)


@cli.command()
@handle_exceptions
@click.argument("keyword")
def keyword(keyword: str):
    """General keyword search.
    """
    search_by_keyword(keyword=keyword)


@cli.command()
@handle_exceptions
@click.argument("cve")
def cve(cve: str):
    """Search info for a CVE-ID.
    """
    search_by_cve_id(cve_id=cve)


@cli.command()
@handle_exceptions
@click.argument("keyword")
def product(keyword: str):
    """Search using product name when CPE info is not known.
    """
    search_by_prod(prod=keyword)


@cli.command()
@handle_exceptions
def version():
    """Search for all CVEs affiliated with versions x.x through y.y of a specific CPE.
    """
    tree = Tree("CPE type hint")
    tree.add("[bold]a[/] application")
    tree.add("[bold]o[/] operating system ")
    tree.add("[bold]h[/] hardware ")
    tree.add("[bold]p[/] others")
    Console().print(tree)

    cpe_type = Prompt.ask("Enter the CPE type", choices=['a', 'o', 'h', 'p'], default='a')
    vendor_name = Prompt.ask("Enter the vendor name")
    product_name = Prompt.ask("Enter the product name")

    start = Prompt.ask("Enter the lowest version", default=None)
    end = Prompt.ask("Enter the highest version", default=None)

    search_by_ver(cpe_name=f"cpe:2.3:{cpe_type}:{vendor_name}:{product_name}", version_start=start, version_end=end)
