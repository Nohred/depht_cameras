### EXPLICACION PROGRAMA


import os
import pandas as pd
import numpy as np

## Esta funcion se encarga de verificar si los archivos csv tienen las dimensiones correctas

def check_csv_dimensions(base_path):
    for folder_name in os.listdir(base_path):
        folder_path = os.path.join(base_path, folder_name)
        if os.path.isdir(folder_path):
            for file_name in os.listdir(folder_path):
                if file_name.endswith('.csv'):
                    file_path = os.path.join(folder_path, file_name)
                    df = pd.read_csv(file_path)
                    if df.shape != (100, 99):
                        print(f"File: {file_name} in Folder: {folder_name} has dimensions {df.shape}")

## Esta funcion se encarga de verificar si los archivos csv tienen las dimensiones correctas y en caso de
#  no tenerlas, inserta las filas faltantes con valores de cero

def check_and_fix_csv_dimensions(base_path):
    for folder_name in os.listdir(base_path):
        folder_path = os.path.join(base_path, folder_name,'camera_1','xyz')

        if os.path.exists(folder_path):
            for file_name in os.listdir(folder_path):
                if file_name.endswith('.csv'):
                    file_path = os.path.join(folder_path, file_name)
                    df = pd.read_csv(file_path, header=None)
                    if df.shape != (33, 4):
                        print(f"File: {file_name} in Folder: {folder_name} has dimensions {df.shape}")
                        # Check for missing indices and insert rows with zero values
                        for i in range(0,33):
                            if i not in df.iloc[:, 0].values:
                                missing_row = pd.DataFrame([[i, 0, 0, 0]], columns=df.columns)
                                df = pd.concat([df, missing_row], ignore_index=True)
                        df = df.sort_values(by=df.columns[0]).reset_index(drop=True) # Sort by index
                        df.to_csv(file_path, index=False, header=False)

## Esta funcion se encarga de mover los archivos raw_data a una carpeta con el nombre de la carpeta original

def move_raw_data(base_path):
    for folder_name in os.listdir(base_path):
        folder_path = os.path.join(base_path, folder_name)
        raw_data_path = os.path.join(folder_path, 'raw_data')
        if os.path.exists(raw_data_path):
            new_raw_data_path = os.path.join(base_path, 'raw_data', f"{folder_name}_raw_data")
            os.rename(raw_data_path, new_raw_data_path)
            print(f"Moved {raw_data_path} to {new_raw_data_path}")

## Esta funcion se encarga de buscar valores de cero en los archivos csv

def find_zero_values(base_path):
    for folder_name in os.listdir(base_path):
        folder_path = os.path.join(base_path, folder_name)
        if os.path.isdir(folder_path):
            for file_name in os.listdir(folder_path):
                if file_name.endswith('.csv'):
                    file_path = os.path.join(folder_path, file_name)
                    df = pd.read_csv(file_path)
                    # zero_indices hace referencia a los indices de las filas que tienen valores de cero
                    zero_indices = []
                    for i in range(1, 100, 3):
                        zero_indices.extend(df[(df.iloc[:, i] == 0) & (df.iloc[:, i+1] == 0) & (df.iloc[:, i+2] == 0)].index.tolist())
                        if zero_indices:
                            print(f"Category: {folder_name}, File: {file_name}, Indices with zero values: {zero_indices}")
                        zero_indices = []

## Esta funcion se encarga de interpolar los valores faltantes en los archivos csv  

def interpolate_missing_values(base_path):
    for folder_name in os.listdir(base_path):
        folder_path = os.path.join(base_path, folder_name)
        if os.path.isdir(folder_path):
            for file_name in os.listdir(folder_path):
                if file_name.endswith('.csv'):
                    file_path = os.path.join(folder_path, file_name)
                    df = pd.read_csv(file_path)
                    for col in df.columns:  # Skip the first column if it's an index
                        df[col] = df[col].replace(0, np.nan) 
                        df[col] = df[col].interpolate(method='linear', limit_direction='both')
                    new_folder_path = os.path.join(base_path, 'filtered_data', folder_name)
                    os.makedirs(new_folder_path, exist_ok=True)
                    new_file_path = os.path.join(new_folder_path, file_name)
                    df.to_csv(new_file_path, index=False)

## Esta funcion se encarga de combinar los archivos csv en una sola carpeta

def combine_csv_files(base_path):
    for folder_name in os.listdir(base_path):
        folder_path = os.path.join(base_path, folder_name)
        if os.path.isdir(folder_path):
            combined_df = pd.DataFrame()
            for file_name in os.listdir(folder_path):
                if file_name.endswith('.csv'):
                    file_path = os.path.join(folder_path, file_name)
                    df = pd.read_csv(file_path)
                    combined_df = pd.concat([combined_df, df], ignore_index=True)
            combined_folder_path = os.path.join(base_path, 'combined_data')
            os.makedirs(combined_folder_path, exist_ok=True)
            combined_file_path = os.path.join(combined_folder_path, f"{folder_name}_combined.csv")
            combined_df.to_csv(combined_file_path, index=False)

# Example usage
base_path = r"C:\Personal Local\Recuperacion\Escuela\5to Semestre\Machine Learning\depht cameras\MultipleCameras\filtered_data"
combine_csv_files(base_path)

# Example usage
# base_path = r"C:\Personal Local\Recuperacion\Escuela\5to Semestre\Machine Learning\depht cameras\MultipleCameras\captured_data"
# find_zero_values(base_path)

##########################################################################

# Example usage
# base_path = r"C:\Personal Local\Recuperacion\Escuela\5to Semestre\Machine Learning\depht cameras\MultipleCameras\captured_data"
# interpolate_missing_values(base_path)

##########################################################################

# Example usage
# base_path = r"C:\Personal Local\Recuperacion\Escuela\5to Semestre\Machine Learning\depht cameras\MultipleCameras\captured_data"
# move_raw_data(base_path)

##########################################################################

# Example usage
# base_path = r"C:\Personal Local\Recuperacion\Escuela\5to Semestre\Machine Learning\depht cameras\MultipleCameras\captured_data"
# check_csv_dimensions(base_path)

##########################################################################

# Example usage
# base_path = r"C:\Personal Local\Recuperacion\Escuela\5to Semestre\Machine Learning\depht cameras\MultipleCameras\captured_data\Saludo\raw_data"
# check_and_fix_csv_dimensions(base_path)