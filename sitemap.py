import os

def read_urls_from_file(file_path):
    with open(file_path, 'r') as file:
        urls = [line.strip() for line in file.readlines()]
    return urls

def add_url_to_sitemap(sitemap, url_parts):
    if not url_parts:
        return
    part = url_parts.pop(0)
    if part not in sitemap:
        sitemap[part] = {}
    add_url_to_sitemap(sitemap[part], url_parts)

def generate_sitemap(urls):
    sitemap = {}
    for url in urls:
        url_parts = url.strip('/').split('/')
        add_url_to_sitemap(sitemap, url_parts)
    return sitemap

def print_sitemap(sitemap, indent=0):
    for part, sub_sitemap in sitemap.items():
        print('  ' * indent + part)
        print_sitemap(sub_sitemap, indent + 1)

def main():
    file_path = 'rhs webscraped links.txt'  # Update this to your file path
    urls = read_urls_from_file(file_path)
    sitemap = generate_sitemap(urls)
    print_sitemap(sitemap)

if __name__ == "__main__":
    main()
