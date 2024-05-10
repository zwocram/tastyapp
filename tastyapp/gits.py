import git
import secretdata


def force_pull_file(file_name):

    # get secrets file
    secrets = secretdata.read_secrets()
    git_repo = secrets.get("github_repo")

    # Initialize a Git repository object
    repo = git.Repo(git_repo)

    # Check if there are any local modifications that would be overwritten
    if repo.is_dirty():
        # Reset the working directory to match the remote branch
        repo.head.reset(index=True, working_tree=True)

    # Pull changes from the remote repository
    origin = repo.remote(github_repo)
    origin.pull()


