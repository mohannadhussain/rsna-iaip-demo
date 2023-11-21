import os, pydicom, traceback, argparse
from os import path


def is_modality_match(file_path, modality):
    try:
        dicom_file = pydicom.dcmread(file_path)
        return modality in dicom_file.Modality
    except Exception as e:
        return False

def delete_dicom_files(directory, modality):
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if file.endswith(".dcm") and is_modality_match(file_path, modality):
                os.remove(file_path)
                print(f"*** Deleted: {file_path}")

if __name__ == "__main__":
    # Read command line arguments
    parser = argparse.ArgumentParser(description='Recurse through directories to find all DICOM files matching a specific modality (e.g. SR) and delete them')
    parser.add_argument('-d', '--directory', type=str, nargs='?', required=True, help="Path to directory containing input DICOM files")
    parser.add_argument('-m', '--modality', type=str, nargs='?', required=True, help="Modality code to filter by, case-sensitive (e.g. SR)")
    args = parser.parse_args()

    if (not path.exists(args.directory)):
        print(f"Directory path not found or not sufficient permissions: {args.directory}", file=sys.stderr, flush=True)
        exit()

    if args.modality is None or args.modality == '':
        print(f"Your must specify a modality code, e.g. SR", file=sys.stderr, flush=True)
        exit()

    delete_dicom_files(args.directory, args.modality)