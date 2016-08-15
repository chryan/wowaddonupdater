from . import git_updater, svn_updater
from enum import Enum

class RepoType(Enum):
	git = 1,
	svn = 2

def select_repo_updater(repo_type):
	if (repo_type == RepoType.git):
		return '.git', git_updater
	if (repo_type == RepoType.svn):
		return '.svn', svn_updater
	return None, None