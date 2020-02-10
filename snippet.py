import os
from dataclasses import dataclass, field
from typing import List

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
