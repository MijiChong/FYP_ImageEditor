import os
import pandas as pd
import numpy as np

# RMSE Calculation Function (relative to mean only)
def calculate_rmse(file1, file2):
    encodings = ['utf-8', 'latin1', 'ISO-8859-1', 'cp1252']

    for encoding in encodings:
        try:
            # Load CSV files
            df1 = pd.read_csv(file1, index_col=0, encoding=encoding)
            df2 = pd.read_csv(file2, index_col=0, encoding=encoding)

            # Get common rows and columns
            common_index = df1.index.intersection(df2.index)
            common_columns = df1.columns.intersection(df2.columns)

            if len(common_index) == 0 or len(common_columns) == 0:
                return None, None

            # Filter to common data
            df1_filtered = df1.loc[common_index, common_columns]
            df2_filtered = df2.loc[common_index, common_columns]

            # Compute RMSE
            rmse = np.sqrt(((df1_filtered - df2_filtered) ** 2).values.mean())

            # Mean for Percentage Calculation
            mean_value = df1_filtered.values.mean()

            return rmse, mean_value

        except UnicodeDecodeError:
            continue

    raise UnicodeDecodeError("Failed to decode using available encodings.")

# Main Process Function
def process_directories_with_order(dir1, dir2, order_file, output_csv):
    # Read the order CSV
    order_df = pd.read_csv(order_file)
    ordered_files = order_df["Img_ID"].str.replace(".png", ".csv")

    results = []

    for img_name in ordered_files:
        file1_path = os.path.join(dir1, img_name)
        file2_path = os.path.join(dir2, img_name)

        if os.path.exists(file1_path) and os.path.exists(file2_path):
            try:
                rmse, mean_value = calculate_rmse(file1_path, file2_path)
                if rmse is not None:
                    # Calculate percentage difference (relative to mean only)
                    percent_mean = (rmse / mean_value * 100) if mean_value != 0 else np.nan

                    results.append([
                        img_name,
                        f"{rmse:.4f}",
                        f"{percent_mean:.4f}%"
                    ])
                else:
                    results.append([img_name, 'No common data', 'N/A'])
            except Exception as e:
                results.append([img_name, f"Error: {e}", 'N/A'])
        else:
            results.append([img_name, "Missing file", 'N/A'])

    # Save to CSV
    df_results = pd.DataFrame(results, columns=['File Name', 'RMSE', 'Percent (Mean)'])
    df_results.to_csv(output_csv, index=False)
    print(f"Results saved to {output_csv}")

# Usage Example
dir1 = r"C:\Users\Mijiiii MC\OneDrive\Desktop\FYP\colorr\ori"
dir2 = r"C:\Users\Mijiiii MC\OneDrive\Desktop\FYP\colorr\32b" 
order_file = r"C:\Users\Mijiiii MC\OneDrive\Desktop\FYP\newOrder.csv"
output_csv = "mean_percentage_results.csv"

process_directories_with_order(dir1, dir2, order_file, output_csv)
