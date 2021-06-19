from __future__ import annotations

import dataclasses
from configparser import ConfigParser
from pathlib import Path
from typing import List, Optional, Union

MINATO_ROOT = Path.home() / ".minato"
DEFAULT_CACHE_ROOT = MINATO_ROOT / "cache"
ROOT_CONFIG_PATH = MINATO_ROOT / "config.ini"
LOCAL_CONFIG_PATH = Path.cwd() / "minato.ini"


@dataclasses.dataclass
class Config:
    cache_root: Path = DEFAULT_CACHE_ROOT

    @classmethod
    def load(cls, cache_root: Optional[Union[str, Path]] = None) -> Config:
        config = cls()
        config.read_files([ROOT_CONFIG_PATH, LOCAL_CONFIG_PATH])
        if cache_root:
            config.cache_root = Path(cache_root)
        return config

    def read_files(self, files: List[Union[str, Path]]) -> None:
        parser = ConfigParser()
        parser.read([str(path) for path in files])
        self._update_from_configparser(parser)

    def _update_from_configparser(self, parser: ConfigParser) -> None:
        if parser.has_section("cache"):
            section = parser["cache"]
            if "root" in section:
                self.cache_root = Path(parser["cache"]["root"])

    @property
    def cache_db_path(self) -> Path:
        return self.cache_root / "cache.db"

    @property
    def cache_artifact_dir(self) -> Path:
        return self.cache_root / "artifacts"
