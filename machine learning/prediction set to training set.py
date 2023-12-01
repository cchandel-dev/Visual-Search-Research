import os, shutil

source_folder =  os.path.join(os.getcwd(), "prediction dataset")
destination_folder = os.path.join(os.getcwd(), "training dataset")
subfolders = ['train', 'test', 'val']

for subfolder in subfolders:
    print('working on {}.'.format(subfolder))
    image_files = os.listdir(os.path.join(source_folder, subfolder, 'images'))
    label_files = os.listdir(os.path.join(source_folder, subfolder, 'labels'))
    for image_file in image_files:
        # Copy the image file from source to destination
        shutil.copyfile(os.path.join(source_folder, subfolder, 'images', image_file), os.path.join(destination_folder, subfolder, 'images', image_file))
    for label_file in label_files:
        # Copy the label file from source to destination and modify it to be yolo compliant
        dest_file = os.path.join(destination_folder, subfolder, 'labels', label_file)
        shutil.copyfile(os.path.join(source_folder, subfolder, 'labels', label_file), dest_file)
        with open(dest_file, 'r') as lbls:
            lines = lbls.readlines()
            copy = lines[0].split()
            del lines[0]
        with open(dest_file, 'w') as file:
                file.writelines(copy[0]+'\t'+copy[1]+'\t'+copy[2]+'\t'+copy[3]+'\t'+copy[4])


            


