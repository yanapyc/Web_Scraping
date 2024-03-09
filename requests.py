import requests
from requests.exceptions import RequestException, Timeout

def get_content(url, max_retries=3, timeout=5):
    for retry_count in range(max_retries):
        try:
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()
            return response.text
        except RequestException as e:
            print(f"Fetching Error for URL {url} {retry_count + 1}: {e}")
            if retry_count < max_retries - 1:
                print(f"Retrying request/n")
            else:
                print(f"Failed to retrieve content from URL {url} after {max_retries} attempts.")
                return None
        except Timeout as e:
            print(f"Timeout error for URL {url}: {e}")
            return None



if __name__ == '__main__':
    urls = [
        "https://en.wikipedia.org/wiki/Computer_science",     # Existing page
        "https://en.wikipedia.org/wiki/",                     # Empty URL
        "https://en.wikipedia.org/wiki/Data_science.*",       # Nonexistent page 
        "https://exedsa.com"                                  # Nonexistent domain
        ]
    
    for url in urls:
        page_content = get_content(url)
        if page_content:
            print("\nThe page content:\n", page_content)
        else:
            print(f"Failed to retrieve content from the page {url}.")

    


    
