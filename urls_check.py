import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def get_status_code(url):
    try:
        response = requests.get(url)
        return response.status_code, response.text
    except requests.exceptions.RequestException as e:
        return str(e), None

def find_hrefs(html_content, base_url):
    soup = BeautifulSoup(html_content, 'html.parser')
    hrefs = [urljoin(base_url, a.get('href')) for a in soup.find_all('a', href=True)]
    return [href for href in hrefs if href != '#' and 'javascript:void(0)' not in href]


def filter_valid_links(links):
    valid_links = []
    for link in links:
        if link.startswith("http") and "#" not in link and "javascript:void(0)" not in link:
            valid_links.append(link)
    return valid_links

def main():
    file_path = "urls.txt"

    try:
        with open(file_path, "r") as file:
            lines = [line.strip() for line in file.readlines()]
            valid_links = filter_valid_links(lines)
            for link in valid_links:
                status_code, html_content = get_status_code(link)
                print(f"URL: {link}, Status Code: {status_code}")

                if html_content:
                  
                    hrefs = find_hrefs(html_content, link)
                    print(f"HREFs found: {hrefs}")

                    for href in hrefs:
                        href_status_code, _ = get_status_code(href)
                        print(f"HREF: {href}, Status Code: {href_status_code}")

    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()

