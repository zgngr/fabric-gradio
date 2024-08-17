import requests
import re

ALLOWLIST_PATTERN = re.compile(r"^[a-zA-Z0-9\s.,;:!?\-]+$") 

class Patterns:
    def __init__(self):
        self.url = "https://api.github.com/repos/zgngr/fabric/contents/patterns?ref=main"
        self.base_url = "https://raw.githubusercontent.com/zgngr/fabric/main/patterns/"

    def get_prompt_list(self):
        response = requests.get(self.url, headers={"Accept": "application/vnd.github.v3+json"})

        if response.status_code == 200:
            contents = response.json()
            names = [item['name'] for item in contents]
            return names
        else:
            return f"Failed to retrieve contents: {response.status_code}"
    
    def get_prompt(self, prompt):
        url = self.base_url + prompt
        return self.fetch_content_from_url(url+'/system.md'), self.fetch_content_from_url(url+'/user.md') 
    
    def fetch_content_from_url(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            sanitized_content = self.sanitize_content(response.text)
            return sanitized_content
        except requests.RequestException as e:
            print(e)
            return ''
        
    def sanitize_content(self, content):
        return "".join(char for char in content if ALLOWLIST_PATTERN.match(char))