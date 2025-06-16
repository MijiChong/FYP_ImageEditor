import os

def rename_csv_files(directory):
    for filename in os.listdir(directory):
        if filename.endswith("r.csv"):  # Check if the file ends with 'r.csv'
            new_filename = filename[:-5] + ".csv"  # Remove the 'r' before '.csv'
            old_path = os.path.join(directory, filename)
            new_path = os.path.join(directory, new_filename)

            os.rename(old_path, new_path)
            print(f"Renamed: {filename} -> {new_filename}")

    print("Renaming complete!")

# Set your target directory
rename_csv_files(r"C:\Users\Mijiiii MC\OneDrive\Desktop\FYP\colorr\32b")
