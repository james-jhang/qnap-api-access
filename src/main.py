import argparse
import os

from filestation import FileStation


def concat_path(*paths):
    paths = map(lambda p: os.path.normpath(p), paths)
    return os.path.join(*paths).replace('\\', '/')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Upload file/folder to QNAP QTS NAS.')
    parser.add_argument('host', type=str, metavar='host', help='URL or IP to the QNAP QTS NAS server.')
    parser.add_argument('user', type=str, metavar='user', help='Username')
    parser.add_argument('password', type=str, metavar='pwd', help='Password')
    parser.add_argument('upload_object', type=str, metavar='upload', help='The file or folder to be uploaded.')
    parser.add_argument('target_dir', type=str, metavar='target', help='The target directory on the NAS.')
    parser.add_argument('-o', '--overwrite', action='store_true', help='Whether overwrite the same name file/folder on the NAS.')
    parser.add_argument('-f', '--fullpath', action='store_true', help='Whether create the full path of the uploaded file on the NAS.')
    parser.set_defaults(overwrite=False)
    args = parser.parse_args()


    filestation = FileStation(args.host, args.user, args.password)

    if os.path.isdir(args.upload_object):
        items = filestation.list(args.target_dir)['datas']
        folders = [it['filename'] for it in items if it['isfolder']]
        root_dir = os.path.basename(args.upload_object)
        if root_dir not in folders:
            filestation.create_folder(
                args.target_dir,
                root_dir
            )
            print(f'Created folder: {concat_path(args.target_dir, root_dir)}')
        for (dirpath, dirnames, filenames) in os.walk(args.upload_object):
            norm_dirpath = concat_path(dirpath)
            target_folder = concat_path(args.target_dir, norm_dirpath)
            for folder in dirnames:
                filestation.create_folder(
                    target_folder,
                    folder
                )
                print(f"Created subfolder: {concat_path(target_folder, folder)}")
            for file in filenames:
                print(f'Upload {file} ...')
                with open(concat_path(norm_dirpath, file), 'rb') as f:
                    upload_file = concat_path(target_folder, file)
                    print(filestation.upload(
                        upload_file,
                        f.read(),
                        args.overwrite
                    ))
    else:
        if args.fullpath:
            # TODO
            raise NotImplementedError()
        else:
            with open(args.upload_object, 'rb') as f:
                upload_file = concat_path(
                    args.target_dir,
                    os.path.basename(args.upload_object)
                )
                filestation.upload(upload_file, f.read(), args.overwrite)
