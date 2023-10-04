import os, pydicom, traceback, argparse
from os import path


def is_dicom_sr(file_path):
    try:
        dicom_file = pydicom.dcmread(file_path)
        #TODO For now, I am keeping it simple with detecting modality=SR. In the future, perhaps it can be based on SOP Class UID
        #print(f"{file_path} = {dicom_file.Modality}")
        return 'SR' in dicom_file.Modality
        #print(f"{file_path} = {dicom_file.SOPClassUID}")
        #return 'Structured Report' in dicom_file.SOPClassUID
    except Exception as e:
        return False

def delete_sr_dicom_files(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if file.endswith(".dcm") and is_dicom_sr(file_path):
                os.remove(file_path)
                print(f"*** Deleted: {file_path}")

if __name__ == "__main__":
    # Read command line arguments
    parser = argparse.ArgumentParser(description='Recurse through directories to find all DICOM SRs and delete them')
    parser.add_argument('-d', '--directory', type=str, nargs='?', required=True, help="Path to directory containing input DICOM files")
    args = parser.parse_args()

    if (not path.exists(args.directory)):
        print(f"Directory path not found or not sufficient permissions: {args.directory}", file=sys.stderr, flush=True)
        exit()
    delete_sr_dicom_files(args.directory)