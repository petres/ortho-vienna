
def createEmptyFolders(f, empty = True):
    for p in f:
        p.mkdir(parents=True, exist_ok=True)
        if empty:
            for f in p.glob('*'):
                f.unlink()