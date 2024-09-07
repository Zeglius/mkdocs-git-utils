import requests
from pygit2 import Signature


from functools import cached_property


class _SignatureWrapper:
    def __init__(
        self, signature: Signature | None = None, /, name: str | None = None
    ) -> None:
        self.signature = signature
        self._name = name or signature.name if signature else None

    def __hash__(self) -> int:
        return self.name.__hash__()

    @property
    def name(self):
        return self._name


class GithubUser:
    __session: requests.Session

    def __init__(
        self, username: str, email: str | None, /, *, signature: Signature | None = None
    ) -> None:
        self.username = username
        self._avatar_url = f"https://github.com/{username}.png"
        self.email = email
        self._signature = signature

    @property
    def session(self):
        if not self.__session:
            self.__session = requests.Session()
        return self.__session

    @cached_property
    def avatar_url(self):
        return self.session.head(self._avatar_url).url
