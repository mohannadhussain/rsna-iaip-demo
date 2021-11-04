# 2021 RSNA Imaging AI in Practice Demo
This repository contains scripts to generate new studies throughout the day for the demos

## Dependencies
* Python 3
* [RSNA's MIRC Clinical Trial Processor (CTP)](https://mircwiki.rsna.org/index.php?title=MIRC_CTP)
* [dcm4che v5](https://sourceforge.net/projects/dcm4che/files/dcm4che3/)

## Usage
```python main.py -d [PATH TO DICOM FILES] -c [PATH TO CTP] -t [TEAM NAME: curie, hounsfield or rontgen]```

## Example commands for the RSNA IAIP 2021 Demo
```buildoutcfg
python3 main.py -c ~/Apps/ctp -t curie -d ~/Downloads/IAIP/Originals/Curie-ChestXR/ -l "./logs"
python3 main.py -c ~/Apps/ctp -t curie -d ~/Downloads/IAIP/Originals/Curie-BrainMR/ -l "./logs"
python3 main.py -c ~/Apps/ctp -t curie -d ~/Downloads/IAIP/Originals/Curie-LungCT/ -l "./logs"

python3 main.py -c ~/Apps/ctp -t hounsfield -d ~/Downloads/IAIP/Originals/Hounsfield-ChestCT/ -l "./logs"
python3 main.py -c ~/Apps/ctp -t hounsfield -d ~/Downloads/IAIP/Originals/Hounsfield-ChestXR/ -l "./logs"
python3 main.py -c ~/Apps/ctp -t hounsfield -d ~/Downloads/IAIP/Originals/Hounsfield-US/ -l "./logs"

python3 main.py -c ~/Apps/ctp -t rontgen -d ~/Downloads/IAIP/Originals/Rontgen-BrainCT/ -l "./logs"
python3 main.py -c ~/Apps/ctp -t rontgen -d ~/Downloads/IAIP/Originals/Rontgen-ChestCT/ -l "./logs"
python3 main.py -c ~/Apps/ctp -t rontgen -d ~/Downloads/IAIP/Originals/Rontgen-ChestXR/ -l "./logs"
```