import os
import sys
import subprocess
import importlib

def github(repo):
    """
    Clone or update a GitHub repository and import it as a Python module, without having to restart runtime.

    Parameters
    repo : str
        The GitHub repository in the format "username/repo_name".
        Example: "pallets/flask"

    Returns
    ModuleType
        The imported and reloaded Python module corresponding to the repository.

    Raises
    subprocess.CalledProcessError
        If the git clone or pull command fails.
    ModuleNotFoundError
        If the repository does not contain a Python module with the same name.

    Usage example:
    flask = github_repo("pallets/flask")
    """

    # Clone or update the repository
    local = repo.split("/")[-1]
    if not os.path.exists(local):
        subprocess.run(
            ["git", "clone", f"https://github.com/{repo}.git"],
            check=True
        )
    else:
        subprocess.run(
            ["git", "-C", local, "pull"],
            check=True
        )

    # Import and reload the module
    if local not in sys.path:
        sys.path.insert(0, local)
    mod = importlib.import_module(local)
    importlib.reload(mod)

    return mod

