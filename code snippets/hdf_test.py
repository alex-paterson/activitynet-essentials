from ActivityNet import *
import numpy as np

frames = np.array(['1.0','2.0','3.0'])

hdf5_object = HDFHelper("test")

print("\n\nCreating group and saving data to it.\n")
hdf5_object.create_group("/test_dir_1/test_dir_2")
hdf5_object.save_data("/test_dir_1/test_dir_2", "test_item", frames)

hdf5_object.print_file_structure()

print("\n\nNow reading the data we saved.\n")
data = hdf5_object.get_data("/test_dir_1/test_dir_2", "test_item")
print(data)

print("\n\nNow deleting only item in the root directory.\n")
hdf5_object.delete_path("/test_dir_1")

# Will print nothing - file is empty
hdf5_object.print_file_structure()

hdf5_object.close()
