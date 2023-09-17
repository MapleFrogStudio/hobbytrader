from hobbytrader.database import load_csv_prices_from_github, save_to_sqlite
from hobbytrader.github import Github

DBPATH = 'DB/minute.sqlite'

def main(github_repo, sub_folder, starts_with):
    print(f'\n\nStep 01: Starting DB generation/update process')

    # Step 01 : Get csv files to load
    github_object = Github(repository=github_repo)
    files_to_load = github_object.file_links(folder=sub_folder, starts_with=starts_with)
    print(f'Step 01: {len(files_to_load)} files detected in github repo: {github_repo}/{sub_folder}')
    print(f'         First file: {files_to_load[0]}, last file: {files_to_load[-1]}')

    # Step 02 : Load prices from github repo
    prices_df = load_csv_prices_from_github(file_links=files_to_load)
    print(f'\nStep 02: Loaded {prices_df.shape} price records in a pandas DataFrame')

    # Step 03 : Save data prices to database
    save_to_sqlite(DBPATH, prices_df)
    print(f'\nStep 03: Prices saved to {DBPATH} databse file')

if __name__ == '__main__':
    repo = 'DATASETS'
    subfolder = '/DAILY'
    starts_with = 'TSX-2023-08'
    main(repo, subfolder, starts_with)

    repo = 'DATASETS'
    subfolder = '/DAILY'
    starts_with = 'SP500-2023-08'
    main(repo, subfolder, starts_with)

    repo = 'DATA-2023-08'
    subfolder = '/'
    starts_with = 'NASDAQ-'
    main(repo, subfolder, starts_with)
