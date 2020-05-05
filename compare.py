import json

from study import Study


def compare(studies_from_scraper: []):
    print("Now comparing the acquired list to the existing list...\nThis process currently depends on:\n - List length\n")
    return len(get_studies_from_json()) == len(studies_from_scraper)


def get_studies_from_json():
    with open('ut-studies/studies.json', 'r') as f:
        studies_dict = json.load(f)
    studies = []
    for study in studies_dict:
        studies.append(Study(study['abbreviation'], study['tabb'], study['name'], study['type']))
    return studies
