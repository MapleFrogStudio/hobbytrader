from hobbytrader.github import Github

def main(github_repo, sub_folder, starts_with):
    github_object = Github(repository=github_repo)
    files_to_load = github_object.file_links(folder=sub_folder, starts_with=starts_with)
    return files_to_load

if __name__ == '__main__':
    repo = 'DATASETS'
    subfolder = '/DAILY'
    starts_with = 'SP500-2023-11'
    files = main(repo, subfolder, starts_with)    
    for file_url in files:
        print(file_url)