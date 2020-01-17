"""AURHelper written in Python.

Usage:
    bez.py [options] <package>...
    bez.py --clear-cache
    bez.py (-v | --version)

Arguments:
    pacakge                     package name or url

Options:
    -S, --sync                  install the package from AUR
    -s SORT, --sort=SORT        sort by which field [default: votes]
    -o ORDER, --order=ORDER     sort order of shown pacakges [default: descending]
    -m NUM, --max-number        max number of result that can be list [default: 20]
    -f FIELDS , --fields FIELDS fields you want to display on the table result
    -v, --version               displays the current version of bez
    -h, --help                  show this help message and exit

    --clear-cache               clear the cache.
    --remove-make-dependencies  remove make dependencies after installation.
    --remove-build              remove package source after installation.
    --pkgbuild-check            check PKGBUILD without confirmation.
    --no-pkgbuild-check         not checking PKGBUILD(NOT RECOMMENDED!).
    --diff-review               diff review files without confiramtion.
    --no-diff-review            not diff review files.
"""

__version__ = "0.1"

import os


import docopt


import caching
from fetcher import Fetcher
from pkgbuild_review import PkgbuildReview
from diff_review import DiffReview
from utils import _yellow


def command_line_runner():
    args = docopt.docopt(__doc__, version=__version__)

    if args["--clear-cache"]:
        if caching._clear_cache():
            exit("Cache cleared successfully.")
        else:
            exit("Clearing cache failed.")

    if args["--max-number"]:
        try:
            args["--max-number"] = int(args["--max-number"])
        except ValueError:
            exit(_yellow("--max-number value should be a number!"))
    fetcher = Fetcher(args)
    selected_pkg = fetcher.user_confirm()
    PkgbuildReview(selected_pkg, args)
    DiffReview(selected_pkg, args)


if __name__ == "__main__":
    if not os.path.exists('/tmp/bezaur/'):
        os.mkdir('/tmp/bezaur/')
    command_line_runner()
