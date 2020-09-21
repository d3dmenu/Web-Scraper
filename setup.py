import sys
import subprocess
import pkg_resources


def installed():
    required = {
        "numpy",
        "re",
        "pandas",
        "bs4",
        "selenium",
        "lxml",
        "pygame",
        "requests",
    }

    installed = {pkg.key for pkg in pkg_resources.working_set}
    missing = required - installed

    if missing:
        # implement pip as a subprocess:
        subprocess.check_call([sys.executable, "-m", "pip", "install", *missing])
    else:
        print("[Log] Install module complete")
