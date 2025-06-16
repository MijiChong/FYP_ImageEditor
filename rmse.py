import os
import pandas as pd
import numpy as np

def calculate_rmse(file1, file2):
    encodings = ['utf-8', 'latin1', 'ISO-8859-1', 'cp1252']
    for encoding in encodings:
        try:
            df1 = pd.read_csv(file1, index_col=0, encoding=encoding)
            df2 = pd.read_csv(file2, index_col=0, encoding=encoding)

            common_index = df1.index.intersection(df2.index)
            common_columns = df1.columns.intersection(df2.columns)

            if len(common_index) == 0 or len(common_columns) == 0:
                return None

            df1_filtered = df1.loc[common_index, common_columns]
            df2_filtered = df2.loc[common_index, common_columns]

            rmse = np.sqrt(((df1_filtered - df2_filtered) ** 2).values.mean())
            return rmse
        except UnicodeDecodeError:
            continue
        except Exception as e:
            raise e

    raise UnicodeDecodeError("None of the attempted encodings worked for these files")

def process_directories_with_order(dir1, dir2, order_file, output_csv):
    results = []

    # Read the order CSV
    order_df = pd.read_csv(order_file)

    # Ensure column name matches and extract base names
    order_df['BaseName'] = order_df['Img_ID'].str.replace('.png', '', regex=False)

    # Get list of CSV files in both directories
    files1 = {f.replace('.csv', ''): f for f in os.listdir(dir1) if f.endswith('.csv')}
    files2 = {f.replace('.csv', ''): f for f in os.listdir(dir2) if f.endswith('.csv')}

    for base_name in order_df['BaseName']:
        if base_name in files1 and base_name in files2:
            file1_path = os.path.join(dir1, files1[base_name])
            file2_path = os.path.join(dir2, files2[base_name])

            try:
                rmse = calculate_rmse(file1_path, file2_path)
                if rmse is not None:
                    results.append([base_name + '.csv', rmse])
                else:
                    results.append([base_name + '.csv', 'No common data'])
            except Exception as e:
                results.append([base_name + '.csv', f'Error: {str(e)}'])
        else:
            results.append([base_name + '.csv', 'File missing'])

    # Save results to CSV
    df_results = pd.DataFrame(results, columns=['File Name', 'Total RMSE'])
    df_results.to_csv(output_csv, index=False)
    print(f"Results saved to {output_csv}")

# Example usage
dir1 = r"C:\Users\Mijiiii MC\OneDrive\Desktop\FYP\colorr\ori"
dir2 = r"C:\Users\Mijiiii MC\OneDrive\Desktop\FYP\colorr\32b" 
order_file = r"C:\Users\Mijiiii MC\OneDrive\Desktop\FYP\newOrder.csv"
output_csv = "rmse_results.csv"

process_directories_with_order(dir1, dir2, order_file, output_csv)
