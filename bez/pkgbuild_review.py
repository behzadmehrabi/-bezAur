import os
import tempfile
import subprocess


import requests


import caching
import utils


class PkgbuildReview:
    def __init__(self, selected_pkg, args):
        self.args = args
        self.name = selected_pkg['name']

        if self._pkgbuild_review_confirm():
            self.pkgbuild_path = self._get_pkgbuild()
            self._show_pkgbuild()

    def _pkgbuild_review_confirm(self):
        '''
        get user input to see whether user want to check PKGBUILD or not.
        return True if user want to check.
        '''
        if self.args["--pkgbuild-check"]:
            pkgbuild_check = True
        elif self.args["--no-pkgbuild-check"]:
            pkgbuild_check = False
        else:
            text = 'do you want to check PKGBUILD? [Y/n] '
            answer = utils.get_input(text)
            pkgbuild_check = utils.yes_no_checker(answer)

        return pkgbuild_check


    def _get_pkgbuild(self):
        '''
        getting plain text of PKGBUILD from AUR repository and write it a
        in temp file.
        return file path if things go right.
        '''
        url = "https://aur.archlinux.org/cgit/aur.git/plain/PKGBUILD?h={}".format(
            self.name
        )
        response = requests.get(url)
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as pb:
            pb.write(response.text)
            return pb.name

    def _show_pkgbuild(self):
        '''
        show PKGBUILD in user desired editor.
        return True if open correctly.
        '''
        editor = os.getenv("EDITOR")
        if not editor:
            editor = "nano"
        try:
            subprocess.call([editor, self.pkgbuild_path])
        except FileNotFoundError:
            exit(_yellow('{} editor not found!'.format(editor)))
        return True
