import argparse
import os

from .filestation import FileStation

# from rich.traceback import install
# install(show_locals=True)

def concat_path(*paths):
    paths = map(lambda p: os.path.normpath(p), paths)
    return os.path.join(*paths)

def upload(filestation: FileStation, upload_object, target_dir, fullpath, overwrite):
    target_path = list(filter(lambda p: p != '', os.path.normpath(target_dir).split(os.sep)))
    current_dir = target_path[0]
    for target_folder in target_path[1:]:
        remote_folders = filestation.list_folders(current_dir, nameonly=True)
        if target_folder not in remote_folders:
            filestation.create_folder(
                current_dir,
                target_folder
            )
            print(f'Created target folder: {concat_path(current_dir, target_folder)}')
        current_dir = concat_path(current_dir, target_folder)

    if fullpath:
        print('fullpath is set. Create path folders...')
        if os.path.isdir(upload_object):
            path = upload_object
        else:
            path = os.path.dirname(upload_object)
        upload_object_path = filter(lambda p: p != '', path.split(os.sep))
        current_dir = target_dir
        for folder in upload_object_path:
            remote_folders = filestation.list_folders(current_dir, nameonly=True)
            if folder not in remote_folders:
                filestation.create_folder(
                    current_dir,
                    folder
                )
                print(f'Created folder: {concat_path(current_dir, folder)}')
            else:
                print(f'Folder already exists: {concat_path(current_dir, folder)}')
            current_dir = concat_path(current_dir, folder)

    if os.path.isdir(upload_object):
        print('Upload object is a folder. Upload all objects in the folder.')
        if not fullpath:
            # if fullpath is not set, we need to check the upload_object folder is created or not;
            # otherwise, since the upload_object folder is created already, we do nothing.
            folders = filestation.list_folders(target_dir, nameonly=True)
            root_dir = os.path.basename(upload_object)
            if root_dir not in folders:
                filestation.create_folder(
                    target_dir,
                    root_dir
                )
                print(f'Created folder: {concat_path(target_dir, root_dir)}')
        for (dirpath, subfolders, filenames) in os.walk(upload_object):
            target_folder = concat_path(target_dir, dirpath)
            for subfolder in subfolders:
                filestation.create_folder(
                    target_folder,
                    subfolder
                )
                print(f"Created subfolder: {concat_path(target_folder, subfolder)}")
            for file in filenames:
                print(f'Upload {file} to {target_folder}...')
                with open(concat_path(dirpath, file), 'rb') as f:
                    upload_file = concat_path(target_folder, file)
                    filestation.upload(
                        upload_file,
                        f.read(),
                        overwrite
                    )
    else: # upload_object is a file
        with open(upload_object, 'rb') as f:
            upload_file = concat_path(
                target_dir,
                os.path.basename(upload_object)
            )
            filestation.upload(upload_file, f.read(), overwrite)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Upload file/folder to QNAP QTS NAS.')
    parser.add_argument('host', type=str, metavar='host', help='URL or IP to the QNAP QTS NAS server.')
    parser.add_argument('user', type=str, metavar='user', help='Username')
    parser.add_argument('password', type=str, metavar='pwd', help='Password')
    parser.add_argument('upload_object', type=str, metavar='upload', help='The file or folder to be uploaded.')
    parser.add_argument('target_dir', type=str, metavar='target', help='The target directory on the NAS.')
    parser.add_argument('-g', '--glob', action='store_true', help='Whether use the glob module to find all the pathnames matching a specified pattern.')
    parser.add_argument('-o', '--overwrite', action='store_true', help='Whether overwrite the same name file/folder on the NAS.')
    parser.add_argument('-f', '--fullpath', action='store_true', help='Whether create the full path of the uploaded file on the NAS.')
    parser.set_defaults(overwrite=False)
    args = parser.parse_args()

    filestation = FileStation(args.host, args.user, args.password)

    if args.glob:
        from glob import glob
        matching_names = glob(args.upload_object)
        for name in matching_names:
            upload(
                filestation,
                upload_object=os.path.normpath(name),
                target_dir=args.target_dir,
                fullpath=True,
                overwrite=args.overwrite
            )
    else:
        upload(
            filestation,
            upload_object=os.path.normpath(args.upload_object),
            target_dir=args.target_dir,
            fullpath=args.fullpath,
            overwrite=args.overwrite
        )
