from collections import namedtuple

import requests
from bs4 import BeautifulSoup


from util import cache, _cyan, _bcyan, _yellow


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
        self.sp = cache.get(self.cache_key)
        if not self.sp:
            self._get_source_page()
        self._parse_table()
        self._show_table()
        

    def _get_source_page(self):
        params = {
            'K': pkg,
            'SB': sort[0] if sort in SORT_CHOICES else 'v',
            'SO': order[0] if order in ORDER_CHOICES else 'd',
        }
        url = 'https://aur.archlinux.org/packages/'
        response = requests.get(url, params=params)
        return cache.set(self.cache_key, response.text)

    def _parse_table(self):
        soup = BeautifulSoup(self.sp, 'html.parser')
        tbody = soup.find('tbody')
        self.pkgs = tbody.find_all('tr')
        for i in range(len(self.pkgs)):
            self.pkgs[i] = [field.text.strip() for field in self.pkgs[i].find_all('td')]
        return self.pkgs[:self.max]
    
    def _show_table(self):
        package = namedtuple('Package', ['name', 'version', 'votes', 'popularity', 'description','maintainer'])
        headers = ('', 'name', 'version', 'votes', 'popularity')
        
        name_len = slice(0, 32)
        version_len = slice(0, 17)

        print(_bcyan('{: >2}  {: <35}{: <19}{: <8}{: <12}'.format(*headers)))
        for num, pkg in enumerate(map(package._make, self.pkgs), start=1):
            if len(pkg.name) > 35:
                pkg = pkg._replace(name=pkg.name[name_len])
            if len(pkg.version) > 20:
                pkg = pkg._replace(version=pkg.version[version_len])

            print(_cyan('{:>2}) '.format(num)), end='')
            print('{:<35}{:<20}{:<9}{:<8}'.format(pkg.name, pkg.version, pkg.votes, pkg.popularity))
        return True

    def user_confirm(self):
        while True:
            try:
                print(_cyan('>>> '), end='')
                text = 'Enter package number please[1-{}]: '.format(len(self.pkgs))
                pkg_number = int(input(text))
                return self.pkgs[pkg_number - 1]
            except IndexError:
                print(_yellow('Entered number is out of range!'))
            except ValueError:
                print(_yellow('Invalid input, please enter a number!'))


