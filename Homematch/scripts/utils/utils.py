import os


class Utils:

    @staticmethod
    def get_resource_path(folder_name: str, file_name: str) -> str:
        dir_path = os.path.dirname(__file__)
        return os.path.join(dir_path, folder_name, file_name)
