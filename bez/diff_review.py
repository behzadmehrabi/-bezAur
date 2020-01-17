import os
import subprocess
import tarfile


import requests
from bs4 import BeautifulSoup


import utils
import caching

class DiffReview:
    def __init__(self, selected_pkg, args):
        self.args = args
        self.name = selected_pkg['name']

        self.base_url = 'https://aur.archlinux.org'
        self.cache_key = 'diff{}{}'.format(self.name, selected_pkg['version'])

        if self._diff_review_confirm():
            self.page_source = caching.cache.get(self.cache_key)
            if not self.page_source:
                self._get_diff_page()
                self.page_source = caching.cache.get(self.cache_key)

            commits = self._get_commits()
            for cc, link in self._find_tarball(commits):
                tar = self._get_tarball(cc, link)
                self._extract_tarball(tar)
            self._show_diff()
    
    def _diff_review_confirm(self):
        if self.args['--diff-review']:
            diff_check = True
        elif self.args['--no-diff-review']:
            diff_check = False
        else:
            text = 'do you want to diff review? [Y/n] '
            answer = utils.get_input(text)
            diff_check = utils.yes_no_checker(answer)

        return diff_check

    def _get_diff_page(self):
        url = '{}/cgit/aur.git/log/.SRCINFO?h={}'.format(self.base_url, self.name)
        response = requests.get(url)
        return caching.cache.set(self.cache_key, response.text)

    def _get_commits(self):
        soup = BeautifulSoup(self.page_source, 'html.parser')
        table = soup.find('table', attrs={'class': 'list nowrap'})
        last_two_commit = table.find_all('tr')[1:3]
        return last_two_commit

    def _find_tarball(self, commits):
        print(utils._cyan('>>>'), 'getting files to review...', sep=' ')
        for commit in commits:
            link = commit.find('a').get('href')
            url = '{}{}'.format(self.base_url, link)
            response = requests.get(url)

            soup = BeautifulSoup(response.text, 'html.parser')
            table = soup.find('table', attrs={'class': 'commit-info'})
            commit_code, link = [(a.text, a.get('href')) for a in table.find_all('a') if a.text.endswith('tar.gz')][0]
            yield commit_code, link

    def _get_tarball(self, cc, link):
        tarpath = '/tmp/bezaur/{}{}'.format(self.name, cc)
        if os.path.exists(tarpath):
            return tarpath
        tarball = requests.get('{}{}'.format(self.base_url, link))
        with open(tarpath, 'wb') as tf:
            tf.write(tarball.content)
            return tf.name
    
    def _extract_tarball(self, tar):
        with tarfile.open(tar, "r:gz") as tf:
             a = tf.extractall(path='/tmp/bezaur/')

    def _show_diff(self):
        first = utils.abs_path('/tmp/bezaur/aur-4369b2d562ca5a526c9e5d96df5949cb51f9cd6f/')
        second = utils.abs_path('/tmp/bezaur/aur-f380837df5229c7196d7d9805b06795033b1f5cf')
        with open('diffreview.txt', 'w+') as f:
            for file1, file2 in zip(first, second):
                subprocess.call(['diff', file1, file2, '--color=always', '--unified'], stdout=f)
                subprocess.call(['echo', '\n'], stdout=f)
            subprocess.call(['less', 'diffreview.txt'])

