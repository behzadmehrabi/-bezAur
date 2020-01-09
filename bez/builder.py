import os
import tempfile
import subprocess
from distutils import util


import requests


from util import _yellow, _cyan


class Builder:
    def __init__(self, selected_pkg, args):
        self.name = selected_pkg[0]

        if args["--pkgbuild-check"]:
            pkgbuild_check = True
        elif not args["--no-pkgbuild-check"]:
            print(_cyan(">>> "), end="")
            pkgbuild_check = input("Do you want to check PKGBUILD? [Y/n] ")
            try:
                pkgbuild_check = util.strtobool(pkgbuild_check)
            except ValueError:
                pkgbuild_check = False

            if pkgbuild_check:
                self.pkgbuild_path = self._get_pkgbuild()
                self._show_pkgbuild()

    def _get_pkgbuild(self):
        url = "https://aur.archlinux.org/cgit/aur.git/plain/PKGBUILD?h={}".format(
            self.name
        )
        response = requests.get(url)
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as pb:
            pb.write(response.text)
            return pb.name

    def _show_pkgbuild(self):
        editor = os.getenv("EDITOR")
        if not editor:
            editor = "nano"
        try:
            subprocess.call([editor, self.pkgbuild_path])
        except FileNotFoundError:
            print(_yellow("{} not found to open PKGBUILD!".format(editor)))
            exit(_yellow("check your EDITOR environment variable value and try again."))

    def _show_diff(self):
