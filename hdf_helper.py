import os, h5py
from . import ROOT_DIR
HDF5_DIR = os.path.join(ROOT_DIR, "hdf5/")

def printname(name):
    print name

class HDFHelper:
    # Specify name without extension
    def __init__(self, filename):
        try:
            self.hdf5_file = h5py.File(os.path.join(HDF5_DIR, filename+".h5"), "r+")
        except IOError as err:
            print("File does not exist. Creating file.")
            self.hdf5_file = h5py.File(os.path.join(HDF5_DIR, filename+".h5"), "w")

    def get_file(self):
        return self.hdf5_file


    def print_file_structure(self):
        self.hdf5_file.visit(printname)

    def delete_path(self, path):
        del self.hdf5_file[path]

    def create_group(self, group_name):
        return self.hdf5_file.create_group(group_name)


    def save_data(self, group_path, name, data):
        grp = self.hdf5_file[group_path]
        dataset = grp.create_dataset(name, data.shape, dtype='f')

    def get_data(self, group_path, name):
        grp = self.hdf5_file[group_path]
        return grp[name]


    def flush(self):
        self.hdf5_file.flush()

    def close(self):
        self.hdf5_file.flush()
        self.hdf5_file.close()
