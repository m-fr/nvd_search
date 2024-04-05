import requests
import re

from rich import box, print
from rich.markup import escape
from rich.table import Table
from rich.prompt import Prompt, IntPrompt, Confirm

from semver import Version

from nvd_search.cli.console import Console
from nvd_search.metrics import severity


def print_cve_details(vulnerabilities):
    table = Table("ID", "Description", "Link", title="CVEs", box=box.HORIZONTALS, show_lines=True)

    for vuln in vulnerabilities:
        cve_id = escape(vuln['cve']['id'])
        description = escape(vuln['cve']['descriptions'][0]['value'])
        cve_link = escape(f"https://nvd.nist.gov/vuln/detail/{cve_id}")
        risk = str(severity(vuln['cve']['metrics']))
        color = severity(vuln['cve']['metrics']).to_color()
        table.add_row(f"{color}{cve_id}\n({risk})", description.strip(), f"[link={cve_link}]{cve_link}[/]")

    Console().print(table, justify="center")


def search_by_keyword(keyword):
    base_url = f"https://services.nvd.nist.gov/rest/json/cves/2.0?keywordSearch={keyword}"
    response = requests.get(base_url)
    response.raise_for_status()
    data = response.json()

    # Extract the CVE IDs and descriptions
    vulnerabilities = data['vulnerabilities']
    print_cve_details(vulnerabilities)
    print(f"Total {len(vulnerabilities)} CVEs found for keyword '{escape(keyword)}'.")
    return vulnerabilities


def search_by_cpe(cpe_name):
    base_url = f"https://services.nvd.nist.gov/rest/json/cves/2.0?cpeName={cpe_name}"
    response = requests.get(base_url)
    response.raise_for_status()
    data = response.json()

    # Extract the CVE IDs and descriptions
    vulnerabilities = data['vulnerabilities']
    print_cve_details(vulnerabilities)
    print(f"Total {len(vulnerabilities)} CVEs found for CPE '{escape(cpe_name)}'.")
    return vulnerabilities


def search_by_cve_id(cve_id):
    cve_id = cve_id.upper()
    base_url = f"https://services.nvd.nist.gov/rest/json/cves/2.0?cveId={cve_id}"
    response = requests.get(base_url)
    response.raise_for_status()
    data = response.json()

    # Extract the CVE IDs and descriptions
    vulnerabilities = data['vulnerabilities']
    print_cve_details(vulnerabilities)
    return vulnerabilities


def match_cpe(cpe):
    input_string = cpe
    url = f"https://services.nvd.nist.gov/rest/json/cpes/2.0?cpeMatchString={input_string}"
    response = requests.get(url)
    response.raise_for_status()

    response_json = response.json()
    if not ("resultsPerPage" in response_json and "products" in response_json):
        print("[logging.level.warning]Invalid response from the NVD API")
        return

    cpe_matches = [product["cpe"]["cpeName"] for product in response_json["products"]]

    if not cpe_matches:
        print(f"[logging.level.info]'{escape(input_string)}' not found in any CPEs")
        return

    selected_num = 0
    if len(cpe_matches) > 1:
        table = Table("#", "CPE", title="CPEs", box=box.HORIZONTALS)
        for i, cpe in enumerate(cpe_matches):
            table.add_row(str(i), escape(cpe))
        Console().print(table, justify="center")

        # Ask the user to select the CPE
        while True:
            selected_num = IntPrompt.ask("Select the serial number tagged to CPE")
            if selected_num not in range(len(cpe_matches)):
                print(f"[prompt.invalid]Please enter a number between 0 and {len(cpe_matches)}.")
                continue
            if Confirm.ask(f"Selected '{escape(cpe_matches[selected_num])}'?", default=True):
                break

    vulnerabilities = search_by_cpe(cpe_matches[selected_num])
    return vulnerabilities


def search_by_prod(prod):
    input_string = prod
    url = f"https://services.nvd.nist.gov/rest/json/cpes/2.0?keywordSearch={input_string}"
    response = requests.get(url)
    response.raise_for_status()

    response_json = response.json()
    if not ("resultsPerPage" in response_json and "products" in response_json):
        print("[logging.level.warning]Invalid response from the NVD API")
        return

    # Look for all occurrences of the input string in the response
    cpe_matches = []
    for product in response_json["products"]:
        cpe_match = re.search(r'cpe:2\.3:.*?:.*?:'+input_string, product["cpe"]["cpeName"])
        if cpe_match:
            cpe_matches.append(cpe_match.group(0))

    if not cpe_matches:
        print(f"[logging.level.info]'{escape(input_string)}' not found in any CPEs")
        return

    # Print all unique matching CPEs with numbered responses
    table = Table("#", "CPE", title="CPEs", box=box.HORIZONTALS)
    unique_cpes = list(set(cpe_matches))
    for i, cpe in enumerate(unique_cpes):
        table.add_row(str(i), escape(cpe))
    Console().print(table, justify="center")

    # Ask the user to select the CPE
    while True:
        selected_num = IntPrompt.ask("Select the serial number tagged to CPE")
        if selected_num not in range(len(unique_cpes)):
            print(f"[prompt.invalid]Please enter a number between 0 and {len(unique_cpes)}.")
            continue
        if Confirm.ask(f"Selected '{escape(unique_cpes[selected_num])}'?", default=True):
            break
    selected_cpe = unique_cpes[selected_num]

    # Ask the user to supply the CPE version
    while True:
        version = Prompt.ask("Enter the product version")
        if Version.is_valid(version):
            break
        print("[prompt.invalid]Please enter a valid version.")
    cpe_s = f"{selected_cpe}:{version}"

    vulnerabilities = match_cpe(cpe_s)
    return vulnerabilities


def search_by_ver(cpe_name, version_start=None, version_end=None):
    base_url = f"https://services.nvd.nist.gov/rest/json/cves/2.0?virtualMatchString={cpe_name}"
    if version_start:
        base_url += f"&versionStart={version_start}&versionStartType=including"
    if version_end:
        base_url += f"&versionEnd={version_end}&versionEndType=excluding"
    response = requests.get(base_url)
    response.raise_for_status()
    data = response.json()

    # Extract the CVE IDs and descriptions

    vulnerabilities = data['vulnerabilities']
    print_cve_details(vulnerabilities)
    print(f"Total {len(vulnerabilities)} CVEs found for CPE '{escape(cpe_name)}'"
          + f" version [{version_start or '0'}, {version_end or 'inf'}).")
    return vulnerabilities
