import pdb
import git
import secretdata
from datetime import datetime
import os.path


def force_pull_file(file_path):

    # get secrets file
    secrets = secretdata.read_secrets()
    git_repo = secrets.get("github_repo")

    # Initialize a Git repository object
    repo = git.Repo()

    # Get the last commit date of the file in the GitHub repository
    try:
        last_commit_date_str = repo.git.log("-1", "--format=%cd", "--date=iso", "--", file_path)
        last_commit_date = datetime.fromisoformat(last_commit_date_str.strip())
        last_commit_date = last_commit_date.astimezone(last_commit_date.tzinfo).replace(tzinfo=None)
    except git.GitCommandError:
        # Handle the case where the file doesn't exist in the GitHub repository
        last_commit_date = None

    # Get the last modified date of the local file
    local_last_modified_date = datetime.fromtimestamp(os.path.getmtime(file_path))

    # Compare the dates
    if last_commit_date is not None and local_last_modified_date > last_commit_date:
        print(f"Local file '{file_path}' is more recent than the file in the GitHub repository.")
    elif last_commit_date is None:
        print(f"File '{file_path}' doesn't exist in the GitHub repository.")
    else:
        print(f"Local file '{file_path}' is not more recent than the file in the GitHub repository.")


    # Check if the file is modified in the index
    if file_path in [item.a_path for item in repo.index.diff(None)]:
        print(f"File '{file_path}' is modified in the index (staged changes).")
    elif file_path in repo.untracked_files:
        print(f"File '{file_path}' is untracked (not staged).")
    else:
        print(f"File '{file_path}' is clean (no modifications).")

    repo.remotes.origin.fetch()
    repo.git.checkout('origin/master', '--', file_path)

    #if file_path in repo.index.diff(None) or file_path in repo.untracked_files:
    #    repo.remotes.origin.fetch()
    #    repo.git.checkout('origin/master', '--', file_path)

    # Pull changes from the remote repository
    # origin = repo.remote(git_repo)
    # origin.pull()

def push_file(file_name, message="new commit"):

    # get secrets file
    secrets = secretdata.read_secrets()
    git_repo = secrets.get("github_repo")

    repo = git.Repo()
    repo.index.add(file_name)
    repo.index.commit(message)
    origin = repo.remote(name='origin')
    origin.push()

