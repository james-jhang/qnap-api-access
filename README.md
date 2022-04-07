qnap
====

QNAP is a network attached storage device that comes with Linux installed on it. They provide a REST API for doing operations on files stored on the device. This repository contains a Python binding for the QNAP NAS API. The following operations are currently supported:

- List shares
- List directory
- Get file info
- Search files
- Delete files
- Download files
- Upload files


```
(venv) qnap on master ≡
➜ python ./main.py -h
usage: main.py [-h] [-o] [-f] host user pwd upload target

Upload file/folder to QNAP QTS NAS.

positional arguments:
  host             URL or IP to the QNAP QTS NAS server.
  user             Username
  pwd              Password
  upload           The file or folder to be uploaded.
  target           The target directory on the NAS.

optional arguments:
  -h, --help       show this help message and exit
  -o, --overwrite  Whether overwrite the same name file/folder on the NAS.
  -f, --fullpath   Whether create the full path of the uploaded file on the NAS.
```