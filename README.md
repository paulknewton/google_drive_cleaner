[![Build Status](https://travis-ci.org/paulknewton/google_drive_cleaner.svg?branch=master)](https://travis-ci.org/paulknewton/google_drive_cleaner)
[![codecov](https://codecov.io/gh/paulknewton/google_drive_cleaner/branch/master/graph/badge.svg)](https://codecov.io/gh/paulknewton/google_drive_cleaner)
[![pyup](https://pyup.io/repos/github/paulknewton/google_drive_cleaner/shield.svg)](https://pyup.io/account/repos/github/paulknewton/google_drive_cleaner)
[![python3](https://pyup.io/repos/github/paulknewton/google_drive_cleaner/python-3-shield.svg)](https://pyup.io/account/repos/github/paulknewton/google_drive_cleaner)

[![DeepSource](https://static.deepsource.io/deepsource-badge-light.svg)](https://deepsource.io/gh/paulknewton/google_drive_cleaner/?ref=repository-badge)

# Google Drive Cleaner

Simple script to query a Google Drive folder, and remove any more than X files. Useful to avoid excessive use of cloud storage space.

## What is it?
Google Drive is a low-cost cloud storage that can be accessed from many different devices. This can be accessed via a web interface or using one of the many sync clients.
Google also provide a Google Drive API with bindings to many popular languages (Java, .NET, PHP, Python, GO...).

I am using Google Drive to automatically upload files from some scripts. This works great, but what happens over time as the drive space starts to fill up...? The idea I had was to use the Python API to query a specific folder on my Google Drive space and remove old files. The number of files to keep was set at some arbitrary figure (1000), and any older files above this number would be removed.

This is a simple way to keep the storage use under control, assuming that old files are no longer needed (and that all files to be cleaned are in a single folder)

## How does it work?
The script is written in python and uses the Google Drive API. In this case, v3 of the API is used.

The Google Drive API uses OAuth2 to provide secure access. This means the script will need to be granted access to your Google Drive, and the corresponding credentials/tokens stored.

Once the script has the correct access, it is just a matter of calling the relevant API calls:
- instantiate a service
- call .list() to retrieve the files in a specific folder, ordered by modification date
- keep the 1000 newest files
- call .delete(id) to remove the other files

## Installation and setup
### Get the code
Make sure you have 'git' installed (if you are looking at this git repo then you probably already do!)
```
git clone https://github.com/paulknewton/google-drive-cleaner
```

### Install the dependencies
The code is written in python3.
Install the google API and OAuth2 python libraries. Using pip, either install directly from the requirements.txt file:
```
pip install -r requirements.txt
```
or install the libraries manually:
```
pip install --upgrade google-api-python-client oauth2client
```

The unit tests are written in ```pytest``` so install this as well:
```
pip install -r requirements_dev.txt
```

### Setup OAuth2
In order to access Google Drive, the program will need the relevant permissions to query and delete files.
Google API access rights are managed using OAuth2. This section describes the setup of OAuth2 and the generation of the necessary credentials.

* Create a Google API project

    Open https://console.developers.google.com and create a new project (choose the dropdown list at the top of the page).
    Give your project a name.

* Create the OAuth consent screen

    This is used the first time the application requests access.
    Choose a name and enter the other details requested (default values should be okay).

* Create an OAuth client ID

    This will be downloaded and used by the python script when it connects to Google Drive each time. Open ‘Credentials’ from the side menu and 'Create Credential'. Choose type OAuth client ID. Enter the values for the client ID (use 'Other’ for the application type and give it a name).

    The client ID is now created. Open it by clicking on the name and ‘Download JSON’. Save this file as ‘cleaner_client_secrets.json’ in the directory above where you are storing this python code.

* Authorise the python program (1 time)

    The first time you run the program you will be asked to authorise the access. This only needs to be done once. Run the program:
    ```
    python clean_google_drive.py blah 99
    ```

    This will open a connection via the Google API and print a URL. This needs to be opened in your web browser. If you are running the program on a headless machine then invoke the python program instead with
    ```
    python clean_google_drive.py --noauth_local_webserver blah 99
    ```

    You will be asked to choose the Google account and grant the permission. Click ‘Allow’. You will be a given an authentication code - paste this back into the application.

    The program will then continue and run as normal.
    Note: this permission approval is only needed 1 time. The next time the program runs it will not ask for permission.

## Command-line args
The program must be run with the ID of the Google Drive folder to query. The cleaner only cleans files in this specified folder. This prevents the script doing any damage elsewhere and it also suited my use case (the files I am trying to cleanup all reside in the same folder). Note: the ID of the folder is not the name, but rather the internal Google folder reference. You will need to get this from the Google Drive interface via a web browser.

The program also requires the number of files to keep. This is a mandatory parameter and cannot be negative.

The program also supports an optional flag to enable test-mode. This test-mode connects to Google Drive but does not actually remove any files.

```
usage: clean_google_drive.py [-h] [-t] folder_id files_to_keep

Script to query a Google Drive folder, and remove any more than X files.
Useful to avoid excessive use of storage space.

positional arguments:
  folder_id      google ID of the folder to query
  files_to_keep  number of files to keep

optional arguments:
  -h, --help     show this help message and exit
  -t             test mode (do not delete files)```
