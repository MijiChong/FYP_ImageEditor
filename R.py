import os

# Set the path to the directory containing your CSV files
folder_path = r'C:\Users\Mijiiii MC\OneDrive\Desktop\FYP\colorr\32b'  # change this to your actual folder path

# Loop through all files in the directory
for filename in os.listdir(folder_path):
    if filename.endswith('.csv') and not filename.endswith('r.csv'):
        old_path = os.path.join(folder_path, filename)
        name_part = filename[:-4]  # remove '.csv'
        new_filename = f"{name_part}r.csv"
        new_path = os.path.join(folder_path, new_filename)
        os.rename(old_path, new_path)
        print(f"Renamed: {filename} -> {new_filename}")
