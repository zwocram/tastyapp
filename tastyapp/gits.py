import pdb
import git
import secretdata


def force_pull_file(file_path):

    # get secrets file
    secrets = secretdata.read_secrets()
    git_repo = secrets.get("github_repo")

    # Initialize a Git repository object
    repo = git.Repo()

    if file_path in repo.index.diff(None) or file_path in repo.untracked_files:
        repo.remotes.origin.fetch()
        repo.git.checkout('origin/master', '--', file_path)

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

