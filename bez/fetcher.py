from collections import namedtuple

import requests
from bs4 import BeautifulSoup


import caching
from utils import _cyan, _boldcyan, _yellow, get_input


class Fetcher():
    SORT_CHOICES = (
        "n", "name",
        "v", "Votes",
        "p", "Popularity",
    )
    ORDER_CHOICES = (
        "a", "Ascending",
        "d", "Descending",
    )

    def __init__(self, args):
        self.pkg = args['<package>']
        self.sort = args['--sort']
        self.order = args['--order']
        self.max = args['--max-number']

        self.cache_key = '{}{}{}'.format(self.pkg, self.sort, self.order)
        self.sp = caching.cache.get(self.cache_key)
        if not self.sp:
            self._get_source_page()
            self.sp = caching.cache.get(self.cache_key)
        self._parse_table()
        self._show_table()
        

    def _get_source_page(self):
        params = {
            'K': self.pkg,
            'SB': self.sort[0] if self.sort in self.SORT_CHOICES else 'v',
            'SO': self.order[0] if self.order in self.ORDER_CHOICES else 'd',
        }
        url = 'https://aur.archlinux.org/packages/'
        response = requests.get(url, params=params)
        return caching.cache.set(self.cache_key, response.text)

    def _parse_table(self):
        soup = BeautifulSoup(self.sp, 'html.parser')
        tbody = soup.find('tbody')
        self.pkgs = tbody.find_all('tr')
        headers = ('name', 'version', 'votes', 'popularity', 'desc', 'maintainer')
        for i in range(len(self.pkgs)):
            self.pkgs[i] = [field.text.strip() for field in self.pkgs[i].find_all('td')]
            self.pkgs[i] = dict(zip(headers, self.pkgs[i]))
        return self.pkgs[:self.max]
    
    def _show_table(self):
        headers = ('', 'name', 'version', 'votes', 'popularity')
        
        name_len = slice(0, 32)
        version_len = slice(0, 17)

        print(_boldcyan('{: >2}  {: <35}{: <19}{: <8}{: <12}'.format(*headers)))
        for num, pkg in enumerate(self.pkgs, start=1):
            if len(pkg['name']) > 35:
                pkg['name'] = pkg['name'][name_len]

            if len(pkg['version']) > 20:
                pkg['version'] = pkg['version'][version_len]

            print(_cyan('{:>2}) '.format(num)), end='')
            print('{:<35}{:<20}{:<9}{:<8}'.format(pkg['name'], pkg['version'], pkg['votes'], pkg['popularity']))
        return True

    def user_confirm(self):
        while True:
            try:
                text = 'Enter package number please[1-{}]: '.format(len(self.pkgs))
                pkg_number = get_input(text, int)
                return self.pkgs[pkg_number - 1]
            except ValueError:
                print(_yellow('Invalid input, please enter a number!'))
            except IndexError:
                print(_yellow('Entered number is out of range!'))


