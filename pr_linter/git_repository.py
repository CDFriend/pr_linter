import pathlib
import re
import shutil
import subprocess
from .utils import on_permission_error


def check_git():
    """Checks that git is in your PATH. Throws an exception if not."""
    try:
        subprocess.check_call(["git", "--version"])
    except FileNotFoundError:
        raise FileNotFoundError("Could not find a git installation on your computer. Check git is on your PATH.")


class GitRepository:
    def __init__(self, source_url: str):
        self._source_url = source_url
        self._clone_path = None

        check_git()

    def clone(self, dest_path: str):
        """Clones the repository to dest_path."""
        subprocess.check_call(["git", "clone", self._source_url, dest_path])
        self._clone_path = dest_path

    def checkout(self, revision: str):
        """Checks out a specified revision in the repository."""
        subprocess.check_output(["git", "checkout", revision], cwd=self._clone_path)

    def get_clone_location(self) -> str:
        return self._clone_path

    def get_current_rev(self) -> str:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=self._clone_path).decode().strip()

    def delete_clone(self):
        if not self._clone_path:
            raise Exception("Can't delete a repository that wasn't cloned!")

        shutil.rmtree(pathlib.Path(self._clone_path), onerror=on_permission_error)
        self._clone_path = None
