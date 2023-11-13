import os, re, sys, random

folder = sys.argv[1]

# Define the directory paths for images and annotations
image_folder = "C:\\Users\\cchan\\Visual-Search-Research\\static\\{}\\Images".format(folder)
annotation_folder = "C:\\Users\\cchan\\Visual-Search-Research\\static\\{}\\Labels".format(folder)

# Get the list of file names in the folders
image_files = os.listdir(image_folder)
annotation_files = os.listdir(annotation_folder)

# Generate a random permutation of numbers from 0 to 100
random_permutation = random.sample(range(0, 104), 104)
print("the random permutation has length of {}".format(len(random_permutation)),'\n',random_permutation)

# Create a mapping between the original file names and the randomized file names
file_mapping = {}
# for f in image_files:
#     f = os.path.splitext(f)[0]  # Extract the file name without the extension
#     # file_mapping[file_name] = str(random_permutation[int(file_name)])
#     #print(file_name, random_permutation[int(file_name)])
image_files = [x.strip('.png') for x in image_files]
print("the image files has length of {}".format(len(image_files)),'\n',image_files)
print("We have processed the following files.", "\n")
# Rename the image files
for file in image_files:
    print(file)
    os.rename(os.path.join(image_folder, file  + ".png"), os.path.join(image_folder,  "image" + str(random_permutation[int(file)]) + ".png"))
    os.rename(os.path.join(annotation_folder, file + ".txt"), os.path.join(annotation_folder, "image" + str(random_permutation[int(file)]) + ".txt"))
print("Files have been successfully renamed.")