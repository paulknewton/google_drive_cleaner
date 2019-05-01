import clean_google_drive


# simple case
def test_clean_simple():
    # test data
    keep = 7
    files = list(range(0, 10))

    dummy_query = (lambda x: files)  # returns the list of 'files'
    dummy_clean = (lambda x: deleted_files.append(x))  # keeps a track of which files are 'deleted'
    all_files = files.copy()
    deleted_files = []

    clean_google_drive.clean_drive("dummy_folder", keep, test_mode=False, query=dummy_query, clean=dummy_clean)

    assert sorted(deleted_files) == sorted(all_files[:-keep])


# keep zero files means delete everything
def test_zero_keep():
    keep = 0
    files = list(range(0, 10))

    dummy_query = (lambda x: files)  # returns the list of 'files'
    dummy_clean = (lambda x: deleted_files.append(x))  # keeps a track of which files are 'deleted'
    all_files = files.copy()
    deleted_files = []

    clean_google_drive.clean_drive("dummy_folder", keep, test_mode=False, query=dummy_query, clean=dummy_clean)

    assert sorted(deleted_files) == sorted(all_files)


# number of files to keep exactly equal to the number of files in the list
def test_clean_no_files_boundary():
    keep = 10
    files = list(range(0, 10))

    dummy_query = (lambda x: files)  # returns the list of 'files'
    dummy_clean = (lambda x: deleted_files.append(x))  # keeps a track of which files are 'deleted'

    deleted_files = []

    clean_google_drive.clean_drive("dummy_folder", keep, test_mode=False, query=dummy_query, clean=dummy_clean)

    assert not deleted_files


# files to keep exceeds the number of files in the list (so no cleaning done)
def test_clean_no_files():
    keep = 20
    files = list(range(0, 10))

    dummy_query = (lambda x: files)
    dummy_clean = (lambda x: deleted_files.append(x))

    deleted_files = []

    clean_google_drive.clean_drive("dummy_folder", keep, test_mode=False, query=dummy_query, clean=dummy_clean)

    assert not deleted_files


# try to keep a negative number (returns without touching the files)
def test_negative_clean():
    # test data
    keep = -7
    files = list(range(0, 10))

    dummy_query = (lambda x: files)  # returns the list of 'files'
    dummy_clean = (lambda x: deleted_files.append(x))  # keeps a track of which files are 'deleted'
    deleted_files = []

    clean_google_drive.clean_drive("dummy_folder", keep, test_mode=False, query=dummy_query, clean=dummy_clean)

    assert not deleted_files


# clean an empty set of files
def test_empty_clean():
    keep = 7
    files = []

    dummy_query = (lambda x: files)  # returns the list of 'files'
    dummy_clean = (lambda x: deleted_files.append(x))  # keeps a track of which files are 'deleted'
    deleted_files = []

    clean_google_drive.clean_drive("dummy_folder", keep, test_mode=False, query=dummy_query, clean=dummy_clean)

    assert not deleted_files
