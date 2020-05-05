import requests
from bs4 import BeautifulSoup, NavigableString


class Abbreviation:
    def __init__(self, exceptions=None):
        res = exceptions if exceptions is not None else []
        print("Downloading list of abbreviations...")
        url = 'https://www.utwente.nl/en/mc/abc-attachments/ml/abbreviation-list/?version=current-abbreviations'
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        rows = soup.find('tbody').findChildren("tr", {'data-version': "current-abbreviations"})
        for row in rows:
            name_en = ""
            name_nl = ""
            if len(row.contents[1].contents) > 0:
                name_en = row.contents[1].contents[0]
            if len(row.contents[2].contents) > 0:
                name_nl = row.contents[2].contents[0]
            name = str(name_en) + str(name_nl)
            abbreviation = isolate_abbreviation(row.contents[0])
            res.append({"name": name, "abbreviation": abbreviation})
        self.abbreviations = res
        print("Abbreviations downloaded and dictionary made.")

    def get_abbreviation(self, name: str):
        current_ab = "PLACEHOLDERPLACEHOLDER"
        for ab in self.abbreviations:
            if ab["name"].find(name) > -1:
                if len(ab["abbreviation"]) < len(current_ab):
                    current_ab = ab["abbreviation"]
        return current_ab if current_ab != "PLACEHOLDERPLACEHOLDER" else ""

    def add_abbreviation(self, studies):
        print("Adding abbreviations...")
        for study in studies:
            abbr = self.get_abbreviation(study.name)
            study.abbreviation = abbr
            study.tabb = study.morb[0] + "-" + abbr
        print("Adding abbreviations complete.")
        return studies


def isolate_abbreviation(element):
    done = False
    while not done:
        if isinstance(element, NavigableString):
            done = True
        else:
            element = element.contents[0]
    return str(element)
