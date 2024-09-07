import re
from pathlib import Path

from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import BasePlugin
from mkdocs.structure.nav import Navigation
from mkdocs.structure.pages import Page
from mkdocs.utils.templates import TemplateContext
from pygit2 import Repository
from pygit2.enums import SortMode

from mkdocs_git_utils.types import _SignatureWrapper

from .config import PluginConfig


class GitUtilsPlugin(BasePlugin[PluginConfig]):
    CO_AUTHOR_RE = re.compile(r"^Co-authored-by:\s(?P<name>[^<]*)\s<(?P<email>[^>]*)")

    def on_config(self, config: MkDocsConfig):
        if not config["enabled"]:
            return

        self.repo = Repository(".")
        self.head = self.repo.head
        self.cache_dir = (
            Path(config.config_file_path).parent / ".cache/plugins/git-utils"
        )

    def on_page_context(
        self,
        context: TemplateContext,
        /,
        *,
        page: Page,
        config: MkDocsConfig,
        nav: Navigation,
    ) -> TemplateContext | None:
        if not config["enabled"]:
            return super().on_page_context(context, page=page, config=config, nav=nav)

        context["commiters"]  # type: ignore
        # Fetch all possible authors
        authors: set[_SignatureWrapper] = set()
        for c in self.repo.walk(self.head.target, sort_mode=SortMode.TIME):
            authors.add(_SignatureWrapper(c.author))
            authors.add(_SignatureWrapper(c.committer))
            # Fetch coauthors
            if m := self.CO_AUTHOR_RE.search(c.message):
                name, email = m.group("name", "email")
                authors.add(_SignatureWrapper(name=name))
        context["commiters"] = list(authors)  # type: ignore
