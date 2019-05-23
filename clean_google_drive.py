import argparse
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from apiclient import errors
from functools import partial

# If modifying these scopes, delete the file token.json.
# SCOPES = 'https://www.googleapis.com/auth/drive.metadata.readonly'
SCOPES = 'https://www.googleapis.com/auth/drive'


def google_logon():
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    store = file.Storage('../cleaner_credentials.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('../cleaner_client_secrets.json', SCOPES)
        creds = tools.run_flow(flow, store)
    return build('drive', 'v3', http=creds.authorize(Http()))


def google_delete(service, file):
    service.files().delete(fileId=file['id']).execute()
    # batch.add(service.files().delete(fileId=f['id']).execute())


def clean_drive(folder_id, files_to_keep, test_mode=False, query=None, clean=None):
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    if test_mode:
        print("--- TEST MODE ---")

    if files_to_keep < 0:
        print("Files to keep cannot be < 0")
        return

    print("Keeping %d files" % files_to_keep)

    files = query(folder_id)
    print("Found %d files" % len(files))

    # strip last X files
    if files_to_keep > 0:   # special case: 0 files_to_keep means delete all
        del files[-files_to_keep:]
    if not files:
        print('No files found to remove')
    else:
        print('Removing %s files' % len(files))

        if test_mode:  # skip file removal if in test mode
            print("Skipping file removal (test mode)")
            return

        # Cannot batch delete requests
        # batch = service.new_batch_http_request(callback=delete_file)
        for f in files:
            # print(f['name'])
            clean(f)
        # service.files().emptyTrash()


def google_query(service, folder_id):
    """Retrieve a list of File resources.

    Args:
      service: Drive API service instance.
    Returns:
      List of File resources.
    """
    params = {
        # "spaces": "drive",
        # "pageSize": 10,
        # id of folder to scan e.g. {'q': "trashed=false and parents in '1PCOXZPwaVlMh93lIm27RNLVxwBRqOvZX'"}
        "q": "trashed=false and parents in '" + folder_id + "'",
        "orderBy": "modifiedTime"   # latest files at the end
    }
    result = []
    page_token = None
    while True:
        try:
            if page_token:
                params['pageToken'] = page_token
            files = service.files().list(**params).execute()

            result.extend(files.get('files'))
            page_token = files.get('nextPageToken')  # more results may be available

            if not page_token:
                break
        except errors.HttpError as error:
            print('An error occurred: %s' % error)
            break
    return result


if __name__ == '__main__':
    # parser = argparse.ArgumentParser(
    #    description="Script to query a Google Drive folder, and remove any more than X files. Useful to avoid excessive use of storage space.")
    # The Google API creates its own argparse instance. Re-use this one.
    parser = tools.argparser
    parser.add_argument("-t", dest="test_mode", action="store_true", help="test mode (do not delete files)",
                        default=False)
    parser.add_argument("folder_id", help="google ID of the folder to query")
    parser.add_argument("files_to_keep", help="number of files to keep", type=int)
    args = parser.parse_args()

    service = google_logon()
    clean_drive(args.folder_id, args.files_to_keep, test_mode=args.test_mode, query=partial(google_query, service),
                clean=partial(google_delete, service))
