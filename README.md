# RSNA Imaging AI in Practice Demo
This repository contains scripts to generate new studies throughout the day for the demos. There is a branch corresponding to the configuration used in every year of the demo.

## Dependencies
* Python 3
* [RSNA's MIRC Clinical Trial Processor (CTP)](https://mircwiki.rsna.org/index.php?title=MIRC_CTP)
* [dcm4che v5](https://sourceforge.net/projects/dcm4che/files/dcm4che3/)

## Usage
```python main.py -d [PATH TO DICOM FILES] -c [PATH TO CTP] -t [TEAM NAME: curie, hounsfield or rontgen]```

## Example commands for the RSNA IAIP 2022 Demo
```buildoutcfg
python3 main.py -c ~/Apps/ctp -t dotter -d ~/Downloads/IAIP/Originals/Dotter-BrainMR-Hyperfine/ -l "./logs"
python3 main.py -c ~/Apps/ctp -t dotter -d ~/Downloads/IAIP/Originals/Dotter-BrainMR-Siemens/ -l "./logs"
python3 main.py -c ~/Apps/ctp -t dotter -d ~/Downloads/IAIP/Originals/Dotter-ChestXR/ -l "./logs"
python3 main.py -c ~/Apps/ctp -t dotter -d ~/Downloads/IAIP/Originals/Dotter-LungCT/ -l "./logs"

python3 main.py -c ~/Apps/ctp -t fleischner -d ~/Downloads/IAIP/Originals/Fleischner-ChestXR/ -l "./logs"
python3 main.py -c ~/Apps/ctp -t fleischner -d ~/Downloads/IAIP/Originals/Fleischner-ChestCT/ -l "./logs"
python3 main.py -c ~/Apps/ctp -t fleischner -d ~/Downloads/IAIP/Originals/Fleischner-ProstateMR/ -l "./logs"

python3 main.py -c ~/Apps/ctp -t mansfield -d ~/Downloads/IAIP/Originals/Mansfield-BrainCT/ -l "./logs"
python3 main.py -c ~/Apps/ctp -t mansfield -d ~/Downloads/IAIP/Originals/Mansfield-ChestXR/ -l "./logs"
python3 main.py -c ~/Apps/ctp -t mansfield -d ~/Downloads/IAIP/Originals/Mansfield-Mammo/ -l "./logs"
```
