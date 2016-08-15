from update_modules import RepoType

all_repos = [
	['elvui',            'http://git.tukui.org/Elv/elvui.git'],
	['deadly-boss-mods', 'git://git.curseforge.com/wow/deadly-boss-mods/mainline.git'],
	['gtfo',             'svn://svn.curseforge.com/wow/gtfo/mainline/trunk'],
	['skada',            'svn://svn.wowace.com/wow/skada/mainline/trunk'],
	['tellmewhen',       'git://git.curseforge.com/wow/tellmewhen/mainline.git'],
]

base_repo_path="f:/World of Warcraft/Interface/Repos/"
output_addon_path="f:/World of Warcraft/Interface/AddOns/"

def get_repo_type(repo_url):
	if "git" in repo_url:
		return RepoType.git
	if "svn" in repo_url:
		return RepoType.svn
	return None