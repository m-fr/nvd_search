# NIST-NVD-CVE-Look-Up
This is a command-line tool to search the National Vulnerability Database (NVD) to fetch CVEs (Common Vulnerabilities and Exposures) associated with a product.

REQUIREMENTS :

pip install click

pip install requests

HOW TO RUN 

$ python3 CVELooup.py

$ ************************************************************************************************************************
                                                 NIST NVD CVE Look-up                                             
search tool to use the National Vulnerability Database (NVD) to fetch CVEs associated with a product @arun kumar v
************************************************************************************************************************
Select the option:
1. General keyword search
2. Search using type, vendor name, product, and version
3. Search infor for a CVE-ID
4. Search for all CVEs affiliated with versions x.x through x.x of a specific CPE
Please choose option 1/2/3/4 or 0 to exit:


For 1 : you can search anything using keyword

2 : input application type , vendorname , product name , version 
for ex: a > xmlsoft > libxml2 > 2.9.11 

3. input CVE id cve-xxxx-xxxx

4. You can specify a range of version after supplying the product details a:xmlsoft:libxml2:2.9.11 
