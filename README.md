# NVD Search

This is a command-line tool to search the National Vulnerability Database (NVD) to fetch Common Vulnerabilities and Exposures (CVEs) associated with a product.

The tool is based on [neondragonwarrior/CVE-Finder](https://github.com/neondragonwarrior/CVE-Finder).

## Get Started

```shell
git clone https://github.com:m-fr/nvd_search
cd nvd_search
pip install .
nvd_search
```

## Functionality

1. General keyword search
2. Search using product name when Common Platform Enumeration (CPE) info is not known
3. Search for CVEs of specific CPE - type, vendor name, product, and version
4. Search info for a CVE-ID
5. Search for all CVEs affiliated with versions `x.x` through `x.x` of a specific CPE
