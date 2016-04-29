import os, h5py
from . import ROOT_DIR
HDF5_DIR = os.path.join(ROOT_DIR, "hdf5/")

class HDFHelper:
    # Specify name without extension
    @staticmethod
    def open_hdf5_file(path):
        return h5py.File(os.path.join(HDF5_DIR, path+".hdf5"), "w")
