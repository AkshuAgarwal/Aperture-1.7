import os
import pathlib
import json

if __name__ == "__main__":
    dirpath = str(pathlib.Path(__file__).parent.absolute()).split('\\')
    dirpath.append('requirements.txt')
    __requirements__ = "\\".join(i for i in dirpath)
    os.system('python -m pip install -r ' + __requirements__)

    try:
        from bot import client
    except ImportError as exc:
        raise ImportError(
            f"""Some Error Occured while Importing...
            Try installing requirements manually by command 'pip3 install -r {__requirements__}' and run the launcher.py again"""
        )

    with open("./data/config.json", "r", encoding="utf-8") as f:
        config = json.load(f)
        __version__ = config['__version__']

    client.run(__version__)