import uuid
import pytest
import os
import shutil
import subprocess

from .git_repository import GitRepository


def add_commit_to_repo(repo: GitRepository) -> str:
    """Adds a dummy commit to a repo for testing purposes.
    :return Hash of the dummy commit.
    """
    clone_folder = repo.get_clone_location()
    subprocess.check_output("cd %s && git commit --allow-empty -m \"Test\"" % clone_folder, shell=True)
    return repo.get_current_rev()


@pytest.fixture
def source_repo():
    # Create an empty git repo to test with
    folder_name = str(uuid.uuid4())
    os.mkdir(folder_name)
    subprocess.check_output("cd %s && git init" % folder_name, shell=True)

    yield folder_name

    shutil.rmtree(folder_name)


@pytest.fixture
def cloned_repo(source_repo):
    repo = GitRepository(source_repo)
    repo.clone(str(uuid.uuid4()))

    yield repo

    repo.delete_clone()


def test_clone_repo(source_repo: str):
    """Git repository should clone without error."""
    repo = GitRepository(source_repo)
    repo.clone(str(uuid.uuid4()))

    # Cloned folder should be a valid git repository
    subprocess.check_output("cd %s && git status" % repo.get_clone_location(), shell=True)

    # Clean up
    repo.delete_clone()


def test_checkout(cloned_repo: GitRepository):
    """Should be able to check out various revisions of a repository."""
    r1 = add_commit_to_repo(cloned_repo)
    r2 = add_commit_to_repo(cloned_repo)

    cloned_repo.checkout(r1)
    assert cloned_repo.get_current_rev() == r1

    cloned_repo.checkout(r2)
    assert cloned_repo.get_current_rev() == r2
