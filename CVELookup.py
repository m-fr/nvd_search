import requests
import json
import click
#author:arunkumarv
#https://www.linkedin.com/in/arunkumarvenugopal/

click.echo(click.style('*' * 120, fg='cyan'))
click.echo(click.style('                                                 NIST NVD CVE Look-up                                             ', fg='green', bold=True))
click.echo(click.style('search tool to use the National Vulnerability Database (NVD) to fetch CVEs associated with a product @arun kumar v', fg='white'))
click.echo(click.style('*' * 120, fg='cyan'))

def print_cve_details(vulnerabilities):
    for vuln in vulnerabilities:
        cve_id = vuln['cve']['id']
        description = vuln['cve']['descriptions'][0]['value']
        print(f"{cve_id}: {description}")
        cve_link = f"https://nvd.nist.gov/vuln/detail/{cve_id}"
        click.echo(click.style(cve_link, fg='blue', underline=True))

def search_by_keyword(keyword):
    base_url =f"https://services.nvd.nist.gov/rest/json/cves/2.0?keywordSearch={keyword}"
    response = requests.get(base_url)
    response.raise_for_status()
    data = response.json()

    # Extract the CVE IDs and descriptions
    vulnerabilities = data['vulnerabilities']
    print_cve_details(vulnerabilities)
    return vulnerabilities

def search_by_cpe(cpe_name):
    base_url = f"https://services.nvd.nist.gov/rest/json/cves/2.0?cpeName={cpe_name}"
    response = requests.get(base_url)
    response.raise_for_status()
    data = response.json()

    # Extract the CVE IDs and descriptions
    vulnerabilities = data['vulnerabilities']
    print_cve_details(vulnerabilities)
    return vulnerabilities


def search_by_cve_id(cve_id):
    cve_id = cve_id.upper()
    base_url =f"https://services.nvd.nist.gov/rest/json/cves/2.0?cveId={cve_id}"
    response = requests.get(base_url)
    response.raise_for_status()
    data = response.json()

    # Extract the CVE IDs and descriptions
    vulnerabilities = data['vulnerabilities']
    print_cve_details(vulnerabilities)
    return vulnerabilities


def search_by_ver(cpe_name, version_start=None, version_end=None):
    base_url =f"https://services.nvd.nist.gov/rest/json/cves/2.0?virtualMatchString=cpe:2.3:{cpe_name}"
    if version_start:
        base_url +=f"&versionStart={version_start}&versionStartType=including"
    if version_end:
        base_url +=f"&versionEnd={version_end}&versionEndType=excluding"
    response = requests.get(base_url)
    response.raise_for_status()
    data = response.json()

    # Extract the CVE IDs and descriptions

    vulnerabilities = data['vulnerabilities']
    print_cve_details(vulnerabilities)
    return vulnerabilities

# Prompt the user to select the search option
def search():
    while True:
        click.echo('Select the option:')
        click.echo('1. General keyword search')
        click.echo('2. Search using type, vendor name, product, and version')
        click.echo('3. Search infor for a CVE-ID')
        click.echo('4. Search for all CVEs affiliated with versions x.x through x.x of a specific CPE')
        option = input('Please choose option 1/2/3/4 or 0 to exit:')

        if option == '1':
            keyword = input('Enter the keyword to search: ')
            print(f"CVEs for '{keyword}':")
            cves = search_by_keyword(keyword)
        elif option == '2':
            click.echo("""NOTE: use 'a' for application | 'o' for operating system | 'h' for hardware | 'p' for others""")
            cpe_type = input('Enter the CPE type (a/o/h/p): ')
            while cpe_type not in ['a', 'o', 'h', 'p']:
                  cpe_type = input('Please enter a valid CPE type (a/o/h/p): ')
            vendor_name = input('Enter the vendor name: ')
            while not vendor_name:
                  vendor_name = input('Please enter a valid vendor name: ')
            product_name = input('Enter the product name: ')
            while not product_name:
                  product_name = input('Please enter a valid product name: ')
            version = input('Enter the product version: ')
            while not version:
                    version = input('Please enter a valid product version: ')
            cpe_name = f"cpe:2.3:{cpe_type}:{vendor_name}:{product_name}:{version}"
             # Fetch the CVEs
            print(f"CVEs for {cpe_name}:")
            cves = search_by_cpe(cpe_name)
        elif option == '3':
            cve_id = input('Enter the CVE-ID to search: ')
            print(f"CVE details for {cve_id}:")
            cves = search_by_cve_id(cve_id)
        elif option == '4':
            cpe_name = input('Enter the CPE name (e.g. a:vendor:product):')
            version_start =input('Enter the starting version where start version included (optional): ')
            version_end =input('Enter the ending version where end version excluded (optional):')
            print(f"CVEs for '{cpe_name}' from versions {version_start} through {version_end}:")
            cves = search_by_ver(cpe_name, version_start, version_end)
        elif option == '0':
            # Exit program
            print("Thank you for using NVD lookup tool. Exiting program....")
            break
        else:
            print("Invalid option. Please try again.")

search()
