import os
import glob
import time
from os import path
from pathlib import Path
import shutil

class FileOps:

    @staticmethod
    def read_all_lines(file_path , encoding ='utf8'):
        with open(file_path, encoding=encoding) as f:   
            lines = [line.rstrip() for line in f]
        
        not_empty_lines = list(filter(lambda t: len(t) > 0, lines))
        line_list = [line.strip() for line in not_empty_lines]
        return line_list

    @staticmethod
    def ensure_dir(dir_path):
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

    @staticmethod 
    def check_file_exist(check_dir, file_type):
        if len(glob.glob(check_dir + "//*" + file_type)) > 0:
            return True , glob.glob(check_dir + "//*" + file_type)
        else:
            return False , None
    
    @staticmethod
    def check_until_file_exist(check_dir, file_type):
        keepGoing = True
        while keepGoing:
            keepGoing , file_list = FileOps.check_file_exist(check_dir, file_type)
            time.sleep(1)

        return file_list

    @staticmethod
    def check_until_none(check_dir, file_regex):
        keepGoing = True
        while keepGoing:
            keepGoing , file_list = FileOps.check_file_exist(check_dir, file_regex)
            time.sleep(1)

    @staticmethod
    def get_file_ext(file_path):
        return Path(file_path).suffix
    
    @staticmethod
    def rename_file(old_file_name, new_file_name):
        path_name = path.realpath(old_file_name)
        dir_path = os.path.dirname(path_name)
        file_ext = FileOps.get_file_ext(old_file_name)
        new_file_name = os.path.join(dir_path , new_file_name)
        os.rename(old_file_name, new_file_name)
        return new_file_name

    @staticmethod
    def unblock_file_in_dir(dirpath):
        system_str = 'powershell.exe -Command Unblock-File -Path "{0}"'.format(os.path.normpath(dirpath))
        print("Unblock file : " + system_str)
        os.system(system_str)
        time.sleep(1)

    @staticmethod
    def remove_all_files_in_type(dir_path, file_type):
        file_list = []
        file_list = glob.glob(dir_path + "//*" + file_type)
        for f in file_list:
            try:
                os.remove(f)
            except OSError as e:
                print("Error: %s : %s" % (f, e.strerror))

    @staticmethod
    def copy_remove_file(src_file, dst_dir):
        dst_dir = dst_dir
        FileOps.ensure_dir(dst_dir)
        print("MOVE to {0}".format(dst_dir))
        shutil.copy(src_file,dst_dir)
        os.remove(src_file)

    @staticmethod
    def get_real_path(file_path):
        return path.realpath(file_path)

    @staticmethod
    def get_dir_path(file_path):
        return os.path.dirname(file_path)