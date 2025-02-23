import requests
import logging
import re
import json
import datetime

class WhiskyInvest():
    # https://www.whiskyinvestdirect.com/ardmore/2017/Q4/BBR/chart.do
    barrelType = {
                "SHF": "First fill sherry hogshead",
                "SBR": "Refill sherry butt",
                "HHR": "Refill hogshead",
                "BBR": "Refill bourbon",
                "SBF": "First fill sherry butt",
                "HHF": "First fill hogshead",
                "BRF": "Refill butt",
                "BBF": "First fill bourbon",
                "SHR": "Refill sherry hogshead",
                "SBN": "New wood sherry butt",
                "HHN": "New wood hogshead",
                "BBN": "New wood bourbon"
            }
    
    def __init__(self, base_url="https://www.whiskyinvestdirect.com/"):
        self.base_url = base_url
        self.session = requests.Session()
        self.cookies = {"considerationCurrency":"GBP"}
    
    def _request_wrapper(self, method, path, body):
        url = self.base_url + path
        if method == "POST":
            req = requests.Request(method, url, json=body, cookies=self.cookies)
        else:
            req = requests.Request(method, url, cookies=self.cookies)

        prepped = self.session.prepare_request(req)

        try:
            response = self.session.send(prepped, timeout=30)
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
            data = response.text

        # print(response.request.__dict__)
        return data
    

    def get_dealHistory(self, whisky:dict) -> dict:

        path = f"{whisky['formattedDistillery']}/{whisky['bondYear']}/{whisky['bondQuarter']}/{whisky['barrelTypeCode']}/chart.do"

        response = self._request_wrapper("GET", path, "")
        pattern = r"\$\('#chartContainer'\),\s?(\[[^\]]+])"
        result = ""
        matches = re.findall(pattern, response)
        if matches:
            result += matches[0]

        try:
            dealHistory = json.loads(result)
        except:
            raise SystemExit(e)
        
        # format date
        for hist in dealHistory:
            hist["date"] = datetime.datetime.fromtimestamp(hist["dealDate"]/1000, tz=datetime.timezone.utc).strftime("%Y-%m-%d")

        logging.info(f"Deal history for {whisky['formattedDistillery']} {whisky['bondYear']} {whisky['bondQuarter']} {whisky['barrelTypeCode']} fetched")
        return dealHistory

    

    def get_pitches(self) -> dict:

        path = f"view_market_json.do"

        response = self._request_wrapper("GET", path, "")
        try:
            market = json.loads(response)
        except:
            raise SystemExit(e)
        
        pitches = market["market"]["pitches"]

        pitches = [pitch for pitch in pitches if pitch.get("considerationCurrency") == "GBP"] #filter out non GBP

        for pitch in pitches:
            pitch["formattedDistillery"] = pitch["distillery"].lower().replace("_", "-")
            pitch["barrelTypeName"] = WhiskyInvest.barrelType.get(f"{pitch['barrelTypeCode']}")
            pitch.pop("prices",None) #remove current prices
            pitch.pop("sellPrices",None) #remove current sell
            pitch.pop("buyPrices",None) #remove current offers
        
        logging.info(f"{len(pitches)} pitches fetched")
        return pitches
    

    
if __name__ == "__main__":
    logging.basicConfig(
        handlers=[
            logging.StreamHandler()
        ],
        level=logging.INFO, 
        format="%(asctime)s %(message)s", datefmt="%Y/%m/%d %H:%M:%S"
    )
    wi = WhiskyInvest()
    # whisky = {"formattedDistillery":"cameronbridge", "barrelTypeCode":"BBF","bondYear":"2017","bondQuarter":"Q1"}
    
    # print(wi.get_dealHistory(whisky))

    # pitches = wi.get_pitches()

