from mkdocs.config import config_options as c
from mkdocs.config.base import Config


class PluginConfig(Config):
    enabled = c.Type(bool, default=True)

    branch = c.Type(str, default="main")
    """Git branch we want to extract logs from. Default is `main`"""

    repo = c.Type(str)
    """Repo owner/name. Only compatible with Github.

       Ex.: `owner/name`"""
