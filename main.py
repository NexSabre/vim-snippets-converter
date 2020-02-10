import copy
import json
import os
from dataclasses import dataclass, field
from typing import List

import requests

from constants import Constants

basedir = os.path.abspath(os.path.dirname(__file__))

@dataclass
class Snippet:
    name: str = None
    prefix: List = field(default_factory=list)
    body: List = field(default_factory=list)
    description: str = None

    def __repr__(self):
        return f"<Snippet {self.prefix}: {self.name}>"

    def clean(self):
        self.name, self.description = (None, ) * 2
        self.prefix, self.body = ([], ) * 2


def download_snippets():
    r = requests.get(Constants.VIM_SNIPPETS_URL)
    if r.status_code != 200:
        print("Something went wrong. Script cannot download snippets from Github")
    with open(os.path.join(basedir, Constants.PYTHON_SNIPPETS_FILE), 'w') as snippets:
        snippets.write(r.content.decode("UTF-8"))


def find_snippet(filename: str = Constants.PYTHON_SNIPPETS_FILE) -> List[Snippet]:
    with open(filename) as snippets_file:
        snippets_db = []
        snippet = Snippet()
        for line in snippets_file.readlines():
            if "snippet " in line:
                if (snippet.name and snippet.prefix) is not None:
                    snippets_db.append(copy.deepcopy(snippet))
                    snippet.clean()

                snippet.name = line.replace("snippet", "").lstrip().rstrip()
                snippet.prefix = snippet.name.split()[0]
                continue
            if line.find("#") == 0:
                continue

            clean_line = line.replace("\t", "", 1).replace("\n", "")
            if line:
                snippet.body.append(clean_line)
        return snippets_db


def save_for_vscode(snippet_db: List[Snippet]):
    if not len(snippet_db):
        exit(1)

    snippet_json = {}
    for snippet in snippet_db:
        snippet_json[snippet.name] = {
            "prefix": snippet.prefix,
            "body": snippet.body,
            "description": snippet.description
        }

    with open(os.path.join(basedir, Constants.PYTHON_SNIPPETS_VSCODE_FILE), "w") as python_json:
        python_json.write(json.dumps(snippet_json))


if __name__ == "__main__":
    download_snippets()
    save_for_vscode(find_snippet())