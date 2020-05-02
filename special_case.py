import re
import requests
from bs4 import BeautifulSoup
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class SpecialCase:
    def __init__(self, url, croho):
        self.checking_url = url
        self.croho = croho

    def check_validity(self):
        print('Starting validitycheck for ' + self.checking_url)
        page = requests.get(self.checking_url, timeout=10, verify=False)
        soup = BeautifulSoup(page.content, 'html.parser')
        text = soup.find_all(text=True)
        only_text = ''
        blacklist = [
            '[document]',
            'noscript',
            'header',
            'html',
            'meta',
            'head',
            'input',
            'script',
            # there may be more elements you don't want, such as "style", etc.
        ]
        for t in text:
            if t.parent.name not in blacklist:
                only_text += '{} '.format(t)
        probability = 0
        regex = re.compile('\w*(?<!(niversity\sof\s)|(universiteit\s))twente', flags=re.IGNORECASE)
        ens_occ = only_text.upper().count('Enschede'.upper())
        twent_occ = len(re.findall(regex, only_text))
        uni1_occ = only_text.upper().count('University of Twente'.upper())
        uni2_occ = only_text.upper().count('Universiteit Twente'.upper())
        print('Occurrences found:\nEnschede\tTwente\tUniversity of Twente\tUniversiteit Twente\n'
              '%s\t\t\t%s\t\t%s\t\t\t\t\t\t%s'
              % (ens_occ, twent_occ, uni1_occ, uni2_occ))
        trust = ens_occ + 2 * twent_occ + 4 * uni1_occ + 4 * uni2_occ
        print('Leading to a total trust of %s.\nThis %s the test.\n' % (trust, 'passes' if trust >= 4 else 'fails'))
        return trust >= 4
