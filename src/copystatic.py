import os
import shutil

def recursive_copy(source, destination):
    # copy all from source
    if os.path.exists(destination) == False:
        os.mkdir(destination)

    for name in os.listdir(source):
        full_source_path = os.path.join(source, name)
        full_dest_path = os.path.join(destination,name)
        print(f"{full_source_path} --> {full_dest_path}")
        if os.path.isfile(full_source_path):
            shutil.copy(full_source_path, full_dest_path)
        else:
            recursive_copy(full_source_path, full_dest_path)
