import clean_google_drive


def test_clean_simple():
    """
    Test simple remove
    """
    # test data
    keep = 7
    files = list(range(0, 10))

    all_files = files.copy()
    deleted_files = []
    dummy_query = (lambda x: files)     # returns the list of 'files'
    dummy_clean = deleted_files.append  # keeps a track of which files are 'deleted'

    clean_google_drive.clean_drive("dummy_folder", keep, test_mode=False, query=dummy_query, clean=dummy_clean)

    assert sorted(deleted_files) == sorted(all_files[:-keep])


def test_zero_keep():
    """
    Test cleaning with 0 files (delete everything)
    """
    keep = 0
    files = list(range(0, 10))

    all_files = files.copy()
    deleted_files = []
    dummy_query = (lambda x: files)     # returns the list of 'files'
    dummy_clean = deleted_files.append  # keeps a track of which files are 'deleted'

    clean_google_drive.clean_drive("dummy_folder", keep, test_mode=False, query=dummy_query, clean=dummy_clean)

    assert sorted(deleted_files) == sorted(all_files)


def test_clean_no_files_boundary():
    """
    Delete X files where the folder contains exactly X files
    """
    keep = 10
    files = list(range(0, 10))

    deleted_files = []

    dummy_query = (lambda x: files)     # returns the list of 'files'
    dummy_clean = deleted_files.append  # keeps a track of which files are 'deleted'

    clean_google_drive.clean_drive("dummy_folder", keep, test_mode=False, query=dummy_query, clean=dummy_clean)

    assert not deleted_files


def test_clean_no_files():
    """
    Delete X files where the folder contains < X files
    :return:
    """
    keep = 20
    files = list(range(0, 10))

    deleted_files = []

    dummy_query = (lambda x: files)
    dummy_clean = deleted_files.append

    clean_google_drive.clean_drive("dummy_folder", keep, test_mode=False, query=dummy_query, clean=dummy_clean)

    assert not deleted_files


def test_negative_clean():
    """
    Delete -ve number of files (returns without removing anything)
    """
    # test data
    keep = -7
    files = list(range(0, 10))

    deleted_files = []

    dummy_query = (lambda x: files)     # returns the list of 'files'
    dummy_clean = deleted_files.append  # keeps a track of which files are 'deleted'

    clean_google_drive.clean_drive("dummy_folder", keep, test_mode=False, query=dummy_query, clean=dummy_clean)

    assert not deleted_files


def test_empty_clean():
    """
    Delete from an empty folder
    """
    keep = 7
    files = []

    deleted_files = []
    dummy_query = (lambda x: files)     # returns the list of 'files'
    dummy_clean = deleted_files         # keeps a track of which files are 'deleted'

    clean_google_drive.clean_drive("dummy_folder", keep, test_mode=False, query=dummy_query, clean=dummy_clean)

    assert not deleted_files
