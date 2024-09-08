from mkdocs.config import config_options as c
from mkdocs.config.base import Config


class PluginConfig(Config):
    enabled = c.Type(bool, default=True)
