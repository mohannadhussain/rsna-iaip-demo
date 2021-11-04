import random
import sys, argparse, os.path, time, datetime
from os import path

STORESCU_PATH = '~/Apps/dcm4che-5.23.2/bin/storescu'
STOWRS_PATH = '~/Apps/dcm4che-5.23.2/bin/stowrs'
DICOM_DEST = {'curie': [{'host':'localhost','port':4242,'aet':'ORTHANC','headerOnly':False}],
              'hounsfield':[{'host':'localhost','port':4242,'aet':'ORTHANC','headerOnly':False}],
              'rontgen':[{'host':'localhost','port':4242,'aet':'ORTHANC','headerOnly':False}],
              'prequel':[{'host':'localhost','port':4242,'aet':'ORTHANC','headerOnly':True}]}
STOW_DEST = {'curie': [{'name':'localhost','url':'http://localhost:8042/dicom-web/studies'}],
             'hounsfield': [{'name':'localhost','url':'http://localhost:8042/dicom-web/studies'}],
             'rontgen': [{'name':'localhost','url':'http://localhost:8042/dicom-web/studies'}],
             'prequel': []}

LAST_NAMES = ['Andriole','Magudia','Shih','Heilbrun','Wiggins','Kahn','Flanders','Cook','Kohli','OConnor','Juluru','Houshmand','Tejani','Duvvuri','Weintraub','Triana','Dhanaliwala','Schmidt','Hussain','Carr','Khan','Knox']

def killCtp():
    os.system("kill -9 `ps fax | grep -v 'grep' | grep CTP | head -n1 | cut -f2,3 -d' '`")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Manipulate CTP (Clinical Trials Processor) to generate a new copy of a given study')
    parser.add_argument('-d','--dicom', type=str, nargs='?', required=True, help="Path to directory containing input DICOM files")
    parser.add_argument('-c', '--ctp', type=str, nargs='?', required=True, help="Path to directory containing CTP")
    parser.add_argument('-t', '--team', type=str, nargs='?', required=True, help="Team name (controls which destinations to send to)")
    parser.add_argument('-l', '--logdir', type=str, nargs='?', required=True, default=".", help="Directory path used for log output")
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
    team = args.team
    log_directory = args.logdir
    dicomDestinations = DICOM_DEST[team]
    stowDestinations = STOW_DEST[team]

    # Step 1: Kill CTP in case it is running and clean up its directories
    killCtp()
    time.sleep(5)
    print('Killed CTP', flush=True)
    os.system(f"rm -rf {ctpPath}/roots/*")
    os.system(f"rm -rf {ctpPath}/quarantines/*")

    # Step 2: Replace CTP's anonymization script
    os.system(f"cp {os.getcwd()}/anonymizer.xml {ctpPath}/scripts/DicomAnonymizer.script")
    scriptFile = open(f"{ctpPath}/scripts/DicomAnonymizer.script", mode='r+')
    now = datetime.datetime.now().strftime("%d%H%M%S")
    last_name = random.choice(LAST_NAMES)
    anonScript = scriptFile.read()
    anonScript = anonScript.replace("{UID_POSTFIX}", now)
    anonScript = anonScript.replace("{STUDY_ACCESSION}", f"acn{now}")
    anonScript = anonScript.replace("{PATIENT_MRN}", f"mrn{now}")
    anonScript = anonScript.replace("{PATIENT_NAME}", f"{last_name}^Frank")
    anonScript = anonScript.replace("{TEAM_NAME}", team)
    scriptFile.seek(0)
    scriptFile.write(anonScript)
    scriptFile.truncate()
    scriptFile.close()

    # Step 3: Start CTP
    os.system(f"cd {ctpPath}; java -jar Runner.jar &")
    time.sleep(5)
    print('Started CTP', flush=True)

    # Step 4: Copy DICOM to CTP's input directory, then wait for processing to happen
    os.system(f"cp -r {dicomIn}/* {ctpPath}/roots/DirectoryImportService/import/")
    print('Copied DICOM to CTP', flush=True)
    time.sleep(60) #TODO This might be need to be bumped up on slower machines

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
        cmd = f"{STOWRS_PATH} --url '{dest['url']}' {ctpPath}/roots/FileStorageService/__default/ >> {log_directory}/stowrs-{dest['name']}-{now}.log 2>&1 &"
        print(cmd, flush=True)
        os.system(cmd)
    print('Done with STOWs', flush=True)

    # Kill CTP as a just-in-case
    killCtp()


