import logging
import json
import time
from whiskyInvest import WhiskyInvest


def main():
    wi = WhiskyInvest()

    pitches = wi.get_pitches()
    # pitches = [{'pitchId': 647, 'securityId': 'SPIRIT000401', 'distillery': 'TULLIBARDINE', 'categoryName': 'SINGLE_MALT', 'barrelTypeCode': 'HHR', 'bondYear': 2023, 'bondQuarter': 'Q2', 'soldOut': False, 'suspended': False, 'minorLine': False, 'openBtbOrderId': None, 'considerationCurrency': 'GBP', 'clientOwned': False, 'size': 13, 'formattedDistillery': 'tullibardine', 'barrelTypeName': 'Refill hogshead'}, {'pitchId': 627, 'securityId': 'SPIRIT000380', 'distillery': 'TULLIBARDINE', 'categoryName': 'SINGLE_MALT', 'barrelTypeCode': 'HHR', 'bondYear': 2022, 'bondQuarter': 'Q4', 'soldOut': False, 'suspended': False, 'minorLine': False, 'openBtbOrderId': None, 'considerationCurrency': 'GBP', 'clientOwned': False, 'size': 10, 'formattedDistillery': 'tullibardine', 'barrelTypeName': 'Refill hogshead'}, {'pitchId': 577, 'securityId': 'SPIRIT000362', 'distillery': 'TULLIBARDINE', 'categoryName': 'SINGLE_MALT', 'barrelTypeCode': 'HHR', 'bondYear': 2022, 'bondQuarter': 'Q1', 'soldOut': False, 'suspended': False, 'minorLine': False, 'openBtbOrderId': None, 'considerationCurrency': 'GBP', 'clientOwned': False, 'size': 9, 'formattedDistillery': 'tullibardine', 'barrelTypeName': 'Refill hogshead'}]
    

    with open("whisky.jsonl", "w") as file:
        for pitch in pitches:
            pitch["dealHistory"] = wi.get_dealHistory(pitch)
            line = json.dumps(pitch) + "\n"
            file.write(line)
            time.sleep(0.5)

    # print(json.dumps(pitches))


    

 
if __name__ == "__main__":
    logging.basicConfig(
        handlers=[
            logging.FileHandler(r"./whisky.log", mode="a"),
            logging.StreamHandler(),
        ],
        level=logging.INFO,
        format="%(asctime)s %(message)s",
        datefmt="%Y/%m/%d %H:%M:%S",
    )
    logging.info("Started")
    main()
    logging.info("Finished")
