import click

from nvd_search.__version__ import __version__
from nvd_search.cli.utils import AliasedGroup, handle_exceptions
from nvd_search.models.version import CPEVersion
from nvd_search.search import search_by_cpe, search_by_keyword, search_by_cve_id, search_by_prod, search_by_ver


@click.group(cls=AliasedGroup, context_settings={'help_option_names': ['-h', '--help']})
@click.version_option(version=__version__)
def cli():
    """NVD Search Tool.
    """


@cli.command()
@handle_exceptions
@click.argument("cpe_name")
def cpe(cpe_name: str):
    """Search by CPE.
    """
    search_by_cpe(cpe_name=cpe_name)


@cli.command()
@handle_exceptions
@click.argument("keyword")
def keyword(keyword: str):
    """Search by keyword.
    """
    search_by_keyword(keyword=keyword)


@cli.command()
@handle_exceptions
@click.argument("cve")
def cve(cve: str):
    """Search by CVE id.
    """
    search_by_cve_id(cve_id=cve)


@cli.command()
@handle_exceptions
@click.argument("keyword")
def product(keyword: str):
    """Search by product keyword.
    """
    search_by_prod(prod=keyword)


@cli.command()
@handle_exceptions
@click.argument("cpe")
@click.option("-s", "--start", help="First product version to be included in search")
@click.option("-e", "--end", help="First product version to be excluded from search")
def version(start: CPEVersion | None, end: CPEVersion | None, cpe: str):
    """Search by CPE version.
    """
    search_by_ver(cpe_name=cpe, version_start=start, version_end=end)
