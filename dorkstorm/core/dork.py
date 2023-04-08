from urllib.parse import urlencode
import requests
from bs4 import BeautifulSoup
import re
import random

class DorkEngine:
    def __init__(self):
        pass
    
    def build_query(self, query_context):
        """
        Function to build a query with the query context
        """
        query_params_string = ""
        
        base_query_param = query_context["configs"]["base_query_params"]
        extra_query_param = query_context["configs"]["extra_query_params"]
        
        query_params_string += base_query_param
        
        # customized query params building
        for param, value in extra_query_param.items():
            if value is not None and value != "":
               query_params_string += f" {param}:{value}"
        
        encoded_query_params = urlencode({'q': query_params_string})
        
        google_search_url = f"https://www.google.com/search?{encoded_query_params}"
        
        query_context["builded_query"] = google_search_url
        
        return google_search_url
        
    def __random_user_agent(self):
        """
        Generate a random user agent from a list of pre-defined user agents. Used to bypass google detection.
        """
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0",
            "Mozilla/5.0 (iPad; CPU OS 13_2_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/111.0 Mobile/15E148 Safari/605.1.15",
            "Mozilla/5.0 (iPad; CPU OS 16_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (iPod touch; CPU iPhone 16_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 OPR/96.0.4693.80",
            "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0",
            "Mozilla/5.0 (X11; Linux x86_64; rv:111.0) Gecko/20100101 Firefox/111.0",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
            
        ]
        return random.choice(user_agents)
    
    def __title_extractor(self, s):
        """
        Private function to extract title from the anchor text output
        """
        
        # Find the index of the first occurrence of "http"
        index = s.find("http")

        # Extract the substring from the start of the string until the index
        title = s[:index].strip()

        # Return the extracted title
        return title


    
    def google_search(self, query, limit=1):
        """
        Execute a Google search for the given query and return a list of result URLs.
        """
        
        page = 0
        result_urls = []
        headers = {"Cookie": "CONSENT=YES+cb.20220404-01-p0.en-GB+FX+142", 
                   "user-agent": self.__random_user_agent(),
                   "referer": "https://www.google.com/"
                }
        
        while page < limit:
            url = f"{query}&start={page*10}"
        
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.content, "html.parser")
            
            if "Our systems have detected unusual traffic from your computer network.  This page checks to see if it's really you sending the requests, and not a robot." in soup.text:
                raise Exception("Google detected suspicious traffic, bot protection detected you. Please try again later.")
            
            results = []
            for g in soup.find_all('div', class_='g'):
                anchors = g.find_all('a')
              
                if anchors:
                    title = self.__title_extractor(anchors[0].text)
                    url = anchors[0]['href']
                    result = {'title': title, 'url': url}
                    results.append(result)
                    if limit < page:
                        break
                 
            page += 1
      
        return results
