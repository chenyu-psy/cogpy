from pathlib import Path

# clean cache
def clean_cache():
    '''
    If global key for escaping does not work, 
    clean cache might be helpful.
    '''
    try:
        delete_path = Path.cwd() / '__pycache__'
        for filename in delete_path.iterdir():
            delete_file=delete_path / filename
            delete_file.unlink()
    except:
        print('The cache files do not exist')