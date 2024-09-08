from dataclasses import dataclass

from git import Commit


class DummyAuthor:
    """Dummy class for author types"""

    pass


@dataclass
class Coauthor(DummyAuthor):
    """Dummy dict for coauthors"""

    name: str
    email: str


@dataclass
class AuthorDict:
    name: str
    avatar: str
    url: str
    login: str
    email: str
    _commit: Commit | None = None

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, self.__class__):
            return False
        return self.name == value.name

    def __hash__(self) -> int:
        return hash(self.name)


def author_from_name(*, name: str, email: str = "", **kargs):
    return AuthorDict(
        name=name,
        avatar=f"https://github.com/{name}.png",
        url=f"https://github.com/{name}/",
        login=name,
        email=email,
        _commit=kargs.get("commit", None),
    )


def author_from_signature(sign):
    name, email = sign.name, sign.email
    return author_from_name(name=name, email=email)
