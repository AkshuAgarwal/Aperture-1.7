import os
import pathlib
import json

def main():
    from bot import client

    with open("./data/config.json", "r", encoding="utf-8") as f:
        config = json.load(f)
        __version__ = config['__version__']

    client.run(__version__)

if __name__ == '__main__':
    try:
        main()
    except ImportError:
        dirpath = str(pathlib.Path(__file__).parent.absolute()).split('\\')
        dirpath.append('requirements.txt')
        __requirements__ = "\\".join(i for i in dirpath)
        os.system('python -m pip install -r ' + __requirements__)

        try:
            main()
        except ImportError as exc:
            raise ImportError(
                f"""Some Error Occured while Importing...
                Error: {exc}
                Try installing requirements manually by command 'python -m pip install -r {__requirements__}' and run the launcher.py again""")