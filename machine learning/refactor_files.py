import os

# Replace 'root_directory' with the path to your main folder
root_directory = 'C:\\Users\\cchandel\\Visual-Search-Research\\machine learning\\runs\\detect - Copy'

# Function to delete everything except 'best.pt'
def delete_except_best_pt(folder):
    for item in os.listdir(folder):
        item_path = os.path.join(folder, item)
        if os.path.isfile(item_path):
            if item != 'best.pt':
                os.remove(item_path)
        elif os.path.isdir(item_path):
            delete_except_best_pt(item_path)


# Start the process
if __name__ == '__main__':
    list_of_folders = os.listdir(root_directory)
    for folder in list_of_folders:
        folder_path = os.path.join(root_directory, folder)
        if os.path.isdir(folder_path):
            print(f"Processing folder: {folder}")
            delete_except_best_pt(folder_path)