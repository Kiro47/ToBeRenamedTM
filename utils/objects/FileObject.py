import os
import stat

class FileObj(object):

    is_valid = True
    filename = None
    abs_file_path = None
    file_type = None
    file_size = None

    def __init__(self, directory:str, filename:str):
        self.filename = filename
        self.abs_file_path = os.path.join(directory, filename)
        if not os.path.exists(self.abs_file_path):
            self.is_valid = False
            return
        # Set stat_block
        self.stat_block = os.stat(self.abs_file_path, follow_symlinks=False)
        # Get filetype
        self.file_type = self.set_file_type()
        if self.file_type == None:
            return
        self.file_size = self.stat_block.st_size

    def set_file_type(self) -> str:
        # Using stat only requires one file access
        if stat.S_ISREG(self.stat_block.st_mode):
            return "file"
        elif stat.S_ISDIR(self.stat_block.st_mode):
            return "dir"
        elif stat.S_ISLNK(self.stat_block.st_mode):
            return "link"
        # Don't want to return anything else
        else:
            self.is_valid = False
            return None

    def to_JSON_dict(self) -> dict:
        if self.is_valid:
            return {
                    "filename": self.filename,
                    "size": self.file_size,
                    "type": self.file_type
                }
        else:
            return None

