import re
from pathlib import Path

from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import BasePlugin
from mkdocs.structure.nav import Navigation
from mkdocs.structure.pages import Page
from mkdocs.utils.templates import TemplateContext
from pygit2 import Repository
from pygit2.enums import SortMode

from mkdocs_git_utils.types import author_from_name, author_from_signature

from .config import PluginConfig


class GitUtilsPlugin(BasePlugin[PluginConfig]):
    CO_AUTHOR_RE = r"^Co-authored-by:\s(?P<name>[^<]*)\s<(?P<email>[^>]*)"

    def on_config(self, config: MkDocsConfig):
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
        if not self.config.enabled:
            return super().on_page_context(context, page=page, config=config, nav=nav)

        context["committers"] = []  # type: ignore
        if not self.config.enabled:
            return context

        # Fetch all possible authors
        authors = []
        for c in self.repo.walk(self.head.target, SortMode.TIME):
            authors = list(
                set(
                    [
                        *authors,
                        *[author_from_signature(x) for x in [c.author, c.committer]],
                    ]
                )
            )
            # Fetch coauthors
            if m := re.search(self.CO_AUTHOR_RE, c.message, flags=re.M):
                name, email = m.group("name", "email")
                authors.append(author_from_name(name=name, email=email))
                del name, email
        # Adapt authors
        context["committers"] = authors  # type: ignore
        return context
