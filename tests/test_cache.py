import tempfile
from pathlib import Path

import pytest

from minato.cache import Cache
from minato.exceptions import CacheNotFoundError


def test_cache_add_list_and_delete() -> None:
    with tempfile.TemporaryDirectory() as _tempdir:
        tempdir = Path(_tempdir)
        cache = Cache(tempdir / "artifacts", tempdir / "sqlite.db")

        with cache:
            cached_file = cache.add("https://example.com/path/to/file_1")
            _ = cache.add("https://example.com/path/to/file_2")
            _ = cache.add("https://example.com/path/to/file_3")

        with cached_file.local_path.open("w") as fp:
            fp.write("Hello, world!")
        assert cached_file.local_path.exists()

        files = cache.list()
        assert len(files) == 3

        with cache:
            cache.delete(cached_file)

        with pytest.raises(CacheNotFoundError):
            cache.by_id(cached_file.id)


def test_cache_contains() -> None:
    with tempfile.TemporaryDirectory() as _tempdir:
        tempdir = Path(_tempdir)
        cache = Cache(tempdir / "artifacts", tempdir / "sqlite.db")

        url = "https://example.com/path/to/file"
        with cache:
            _ = cache.add(url)

        assert url in cache
