import requests
import logging
from bs4 import BeautifulSoup
import re

class WhiskyInvest():
    # https://www.whiskyinvestdirect.com/ardmore/2017/Q4/BBR/chart.do
    def __init__(self, base_url="https://www.whiskyinvestdirect.com/"):
        self.base_url = base_url
        self.session = requests.Session()
    
    def _request_wrapper(self, method, path, body):
        url = self.base_url + path
        if method == "POST":
            req = requests.Request(method, url, json=body)
        else:
            req = requests.Request(method, url)

        prepped = self.session.prepare_request(req)

        try:
            response = self.session.send(prepped, timeout=3)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            logging.exception(f"HTTP error: {e}")
            raise SystemExit()
        except requests.exceptions.Timeout as e:
            logging.exception(f"The request timed out: {e}")
            raise SystemExit()
        except requests.exceptions.RequestException as e:
            logging.exception(f"Exception: {e}")
            raise SystemExit(e)
        
        if response.content:
            data = response.content
        # print(data)     
        return data
    

    def get_chart(self, whisky:dict):

        path = f"{whisky['formattedDistillery']}/{whisky['bondYear']}/{whisky['bondQuarter']}/{whisky['barrelTypeCode']}/chart.do"

        response = self._request_wrapper("GET", path, "")
        soup = BeautifulSoup(response, "html.parser")
        scriptTags = soup.find_all("script",src=None)
        pattern = r"\$\('#chartContainer'\),\s?(\[[^\]]+])"
        result = ""
        for tag in scriptTags:
            matches = re.findall(pattern, tag.string)
            if matches:
                result += matches[0]

        print(result)
    

    
if __name__ == "__main__":
    logging.basicConfig(
        handlers=[
            logging.StreamHandler()
        ],
        level=logging.INFO, 
        format="%(asctime)s %(message)s", datefmt="%Y/%m/%d %H:%M:%S"
    )
    wi = WhiskyInvest()
    whisky = {"formattedDistillery":"cameronbridge", "barrelTypeCode":"BBF","bondYear":"2017","bondQuarter":"Q1"}
    wi.get_chart(whisky)


