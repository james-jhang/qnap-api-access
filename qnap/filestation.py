import os

from .qnap import Qnap

class FileStation(Qnap):
    """
    Access QNAP FileStation.
    """

    def list_share(self):
        """
        List all shared folders.
        """
        return self.status_checker(
            self.req(self.endpoint(
                func='get_tree',
                params={
                    'is_iso': 0,
                    'node': 'share_root',
                }
            ))
        )

    def list(self, path, limit=10000):
        """
        List files in a folder.
        """
        return self.status_checker(
            self.req(self.endpoint(
                func='get_list',
                params={
                    'is_iso': 0,
                    'limit': limit,
                    'path': path.replace('\\', '/')
                }
            ))
        )

    def list_folders(self, path, nameonly=False):
        items = self.list(path.replace('\\', '/'))
        items = items['datas']
        folders = []
        for it in items:
            if it['isfolder']:
                if nameonly:
                    folders.append(it['filename'])
                else:
                    folders.append(it)
        return folders

    def get_file_info(self, path):
        """
        Get file information.
        """
        dir_path = os.path.dirname(path)
        file_name = os.path.basename(path)
        return self.status_checker(
            self.req(self.endpoint(
                func='stat',
                params={
                    'path': dir_path.replace('\\', '/'),
                    'file_name': file_name
                }
            ))
        )

    def search(self, path, pattern):
        """
        Search for files/folders.
        """
        return self.status_checker(
            self.req(self.endpoint(
                func='search',
                params={
                    'limit': 10000,
                    'start': 0,
                    'source_path': path.replace('\\', '/'),
                    'keyword': pattern
                }
            ))
        )

    def delete(self, path):
        """
        Delete file(s)/folder(s)
        """
        dir_path = os.path.dirname(path)
        file_name = os.path.basename(path)
        return self.status_checker(
            self.req(self.endpoint(
                func='delete',
                params={
                    'path': dir_path.replace('\\', '/'),
                    'file_total': 1,
                    'file_name': file_name
                }
            ))
        )

    def download(self, path):
        """
        Download file.
        """
        dir_path = os.path.dirname(path)
        file_name = os.path.basename(path)
        return self.status_checker(
            self.req_binary(self.endpoint(
                func='download',
                params={
                    'isfolder': 0,
                    'source_total': 1,
                    'source_path': dir_path.replace('\\', '/'),
                    'source_file': file_name
                }
            ))
        )

    def create_folder(self, path, name):
        """
        Create folder.
        """
        return self.status_checker(
            self.req_post(self.endpoint(
                func='createdir'
                ),
                data={
                    'dest_path': path.replace('\\', '/'),
                    'dest_folder': name,
                }
            )
        )

    def upload(self, path, data, overwrite=True):
        """
        Upload file.
        """
        dir_path = os.path.dirname(path)
        file_path = path.replace('/', '-')
        file_name = os.path.basename(path)
        return self.status_checker(
            self.req_post(self.endpoint(
                func='upload',
                params={
                    'type': 'standard',
                    'overwrite': 1 if overwrite else 0,
                    'dest_path': dir_path.replace('\\', '/'),
                    'progress': file_path
                }),
                files={
                    'file': (
                        file_name,
                        data,
                        'application/octet-stream'
                    )
                }
            )
        )

    def status_checker(self, resp):
        if 'success' in resp:
            if resp['success'] != 'true' or resp['status'] != 1:
                raise Exception(str(resp))
        return resp
