import re
import urllib
from pathlib import Path
from zipfile import ZipFile

import openpyxl
import os

from compare import compare
from scraper import scrape_croho_codes
from special_case import SpecialCase
from study import Study
from abbreviations import Abbreviation


def read_croho_xlsx():
    ZIPFILE = "./temp_croho_sheet_zip.zip"
    print('Beginning file download with urllib2...')

    url = 'https://duo.nl/zakelijk/images/downloaden-actueel-croho-in-excel.zip'
    urllib.request.urlretrieve(url, ZIPFILE)
    print('Download complete\nUnzipping...')
    with ZipFile(ZIPFILE) as zipfile:
        zipfile.extractall()
    os.remove('temp_croho_sheet_zip.zip')
    os.remove('Toelichting CROHO actueel in Excel v2019.doc')
    print("Unzipping complete\n")

    scraped_croho_codes = scrape_croho_codes()

    regex = re.compile('Croho.*')
    crohofile = list(filter(regex.match, os.listdir()))[0]
    xlsx_file = Path(crohofile)
    print('Loading in downloaded CROHO registry. This might take a while.')
    wb_obj = openpyxl.load_workbook(xlsx_file)
    wsheet = wb_obj.active
    print("Loading complete. Starting checks for special cases.\n")
    activeutstudies = []
    crohocodes = []
    special_cases_codes = []
    special_cases_tuples = []
    special_cases = [SpecialCase('https://www.msc-gima.nl/programme-introduction/', '60732',
                                 'Geographical Information Management and Applications')]
    for case in special_cases:
        if case.check_validity():
            special_cases_codes.append(case.croho)
    print("Now searching for studies in downloaded CROHO registry...")
    for row in wsheet.iter_rows():
        if (row[2].value.find('Universiteit Twente') > -1 or str(row[6].value) in scraped_croho_codes)\
                and str(row[12].value).find('00-00-000') > -1\
                and row[6].value not in crohocodes:
            crohocodes.append(row[6].value)
            activeutstudies.append(row)
        else:
            for special in special_cases:
                if str(row[6].value) == special.croho and special.croho not in crohocodes:
                    crohocodes.append(special.croho)
                    special_cases_tuples.append((row, special))
    print("Searching complete.\n")
    res = []
    for row in activeutstudies:
        res.append(Study("", "", get_without_type_prefix(row[7].value), "Bachelor" if row[7].value[0:2] == "B " else "Master"))
    for tup in special_cases_tuples:
        res.append(Study("", "", tup[1].name, "Bachelor" if tup[0][7].value[0:2] == "B " else "Master"))
    abbr_gen = Abbreviation()
    abbr_gen.add_abbreviation(res)
    identical = compare(res)
    print("Process complete. The current list has been found to be " + "up to date." if identical else "outdated.")


def get_without_type_prefix(input: str):
    return input[2:len(input)]


read_croho_xlsx()
