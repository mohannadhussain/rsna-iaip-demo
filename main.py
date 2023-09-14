import random
import sys, argparse, os.path, time, datetime
from os import path

STORESCU_PATH = '~/Apps/dcm4che-5.23.2/bin/storescu'
STOWRS_PATH = '~/Apps/dcm4che-5.23.2/bin/stowrs'

DICOM_DEST = {'bucky': [{'host':'localhost','port':4242,'aet':'ORTHANC','headerOnly':False}],
              'mallard':[{'host':'localhost','port':4242,'aet':'ORTHANC','headerOnly':False}],
              'jensen':[{'host':'localhost','port':4242,'aet':'ORTHANC','headerOnly':False}]}
STOW_DEST = {'bucky': [{'name':'localhost','url':'http://localhost:8042/dicom-web/studies'}],
             'mallard': [{'name':'localhost','url':'http://localhost:8042/dicom-web/studies'}],
             'jensen': [{'name':'localhost','url':'http://localhost:8042/dicom-web/studies'}]}


LAST_NAMES = ['Harrold','Green','Brown','James','Steel','Bond','Jones','Connor','Williams','Hortons','Park','Frederik','Singh','Patel','Hawk','Smith','Stephenson','Lewis','Nicholls','Howard','Grant','Liu','Victor','McDonald','Lamb','Young','Ali','Chan','Thompson','Morgan','Campbell','Noble','Bell']

def killCtp():
    os.system("kill -9 `ps fax | grep -v 'grep' | grep CTP | head -n1 | sed 's/^ *//g' | cut -f 1 -d ' '")


def countFiles(dir_path):
    count = 0
    for root_dir, cur_dir, files in os.walk(dir_path):
        count += len(files)
    return count


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Manipulate CTP (Clinical Trials Processor) to generate a new copy of a given study')
    parser.add_argument('-d','--dicom', type=str, nargs='?', required=True, help="Path to directory containing input DICOM files")
    parser.add_argument('-c', '--ctp', type=str, nargs='?', required=True, help="Path to directory containing CTP")
    parser.add_argument('-t', '--team', type=str, nargs='?', required=True, help="Team name (controls which destinations to send to)")
    parser.add_argument('-l', '--logdir', type=str, nargs='?', required=True, default=".", help="Directory path used for log output")
    parser.add_argument('-g', '--generateonly', type=bool, nargs='?', required=False, default=False, help="Only generate DICOM files and do NOT send them (no C-STORE, no STOW)")
    args = parser.parse_args()

    # Perform some basic error checking
    if( not path.exists(args.dicom) ):
        print(f"DICOM path not found or not sufficient permissions: {args.dicom}", file=sys.stderr, flush=True)
        exit()
    if (not path.exists(args.ctp)):
        print(f"CTP path not found or not sufficient permissions: {args.ctp}", file=sys.stderr, flush=True)
        exit()
    if (not path.exists(args.logdir)):
        print(f"Log directory path not found or not sufficient permissions: {args.logdir}", file=sys.stderr, flush=True)
        exit()
    if(args.team not in DICOM_DEST):
        print(f"Unknown team: {args.team}", file=sys.stderr, flush=True)
        exit()

    ctpPath = args.ctp
    dicomIn = args.dicom
    team = str(args.team).lower()
    institution = team
    log_directory = args.logdir
    dicomDestinations = DICOM_DEST[team]
    stowDestinations = STOW_DEST[team]
    patient_sex = "M"

    first_name = "Frank"
    if team == "jensen":
        first_name = "Francine"
        patient_sex = "F"
    if team == "bucky-hyperfine":
        first_name = "Joan"
        patient_sex = "F"
        institution = 'bucky'

    # Step 1: Kill CTP in case it is running and clean up its directories
    killCtp()
    time.sleep(5)
    print('Killed CTP', flush=True)
    os.system(f"rm -rf {ctpPath}/roots/*")
    os.system(f"rm -rf {ctpPath}/quarantines/*")

    # Step 2: Replace CTP's anonymization script
    os.system(f"cp {os.getcwd()}/anonymizer.xml {ctpPath}/scripts/DicomAnonymizer.script")
    scriptFile = open(f"{ctpPath}/scripts/DicomAnonymizer.script", mode='r+')
    now = datetime.datetime.now().strftime("%d%H%M%S").strip('0') # Remove the leading zero (makes for illegal UIDs)
    last_name = random.choice(LAST_NAMES)
    patient_name = f"{last_name}^{first_name}"
    anonScript = scriptFile.read()
    anonScript = anonScript.replace("{UID_POSTFIX}", now)
    anonScript = anonScript.replace("{ACCESSION_PREFIX}", f"{now}")
    anonScript = anonScript.replace("{PATIENT_MRN}", f"mrn{now}")
    anonScript = anonScript.replace("{PATIENT_SEX}", patient_sex)
    anonScript = anonScript.replace("{PATIENT_NAME}", patient_name)
    anonScript = anonScript.replace("{TEAM_NAME}", institution)
    scriptFile.seek(0)
    scriptFile.write(anonScript)
    scriptFile.truncate()
    scriptFile.close()

    print(f"======= Patient name is {patient_name}")

    # Step 3: Start CTP
    os.system(f"cd {ctpPath}; java -jar Runner.jar &")
    time.sleep(5)
    print('Started CTP', flush=True)

    # Step 4: Copy DICOM to CTP's input directory, then wait for processing to happen
    os.system(f"cp -r {dicomIn}/* {ctpPath}/roots/DirectoryImportService/import/")
    print('Copied DICOM to CTP', flush=True)
    last_count = -1
    while( True ):
        time.sleep(10)
        current_count = countFiles(f'{ctpPath}/roots/FileStorageService/__default/')
        if current_count == last_count: # CTP is no longer generating new files, i.e. it is finished
            break
        elif current_count > 0: # CTP is still working, sleep again and try in a bit
            last_count = current_count

    if args.generateonly is not True:
        # Step 5: C-STORE anonymized copy to the given destinations for this configuration
        print('About to start C-STORing anonymized DICOM', flush=True)
        for dest in dicomDestinations:
            params = ""
            if( 'headerOnly' in dest and dest['headerOnly'] == True ):
                params = "-s 7fe00010="
            cmd = f"{STORESCU_PATH} -b DEMOTOOL -c {dest['aet']}@{dest['host']}:{dest['port']} {ctpPath}/roots/FileStorageService/__default/* {params} >> {log_directory}/storescu-{dest['aet']}-{now}.log 2>&1 &"
            print(cmd, flush=True)
            os.system(cmd)

        print('Done with C-STOREs', flush=True)

        # Step 6: STOW anonymized copy to destinations that do not support C-STORE
        print('About to start STOWing anonymized DICOM', flush=True)
        for dest in stowDestinations:
            extra_stuff = "\\{\\} \\;"
            cmd = f"find {ctpPath}/roots/FileStorageService/__default/ -name '*.dcm' -exec {STOWRS_PATH} --url '{dest['url']}' -a json -t json {extra_stuff} >> {log_directory}/stowrs-{dest['name']}-{now}.log 2>&1 &"
            print(cmd, flush=True)
            os.system(cmd)
        print('Done with STOWs', flush=True)

    # Kill CTP as a just-in-case
    killCtp()


