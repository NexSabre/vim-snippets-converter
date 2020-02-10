import copy
import json
import os
from dataclasses import dataclass
from typing import List

import requests

from constants import Constants
from snippet import basedir, Snippet


@dataclass
class Converter:
    snippet_db = None

    def __post_init__(self):
        self.download_snippets()
        self.snippet_db = self.find_snippet()

    @staticmethod
    def download_snippets():
        r = requests.get(Constants.VIM_SNIPPETS_URL)
        if r.status_code != 200:
            print("Something went wrong. Script cannot download snippets from Github")
        with open(os.path.join(basedir, Constants.PYTHON_SNIPPETS_FILE), 'w') as snippets:
            snippets.write(r.content.decode("UTF-8"))

    @staticmethod
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

    def save_for_vscode(self):
        if not len(self.snippet_db):
            print(f"Converter cannot open temporary file with snippets at {basedir}")
            exit(1)

        snippet_json = {}
        for snippet in self.snippet_db:
            snippet_json[snippet.name] = {
                "prefix": snippet.prefix,
                "body": snippet.body,
                "description": snippet.description
            }

        with open(os.path.join(basedir, Constants.PYTHON_SNIPPETS_VSCODE_FILE), "w") as python_json:
            python_json.write(json.dumps(snippet_json))
