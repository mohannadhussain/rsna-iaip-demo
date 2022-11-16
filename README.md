# RSNA Imaging AI in Practice Demo Data Generator
This repository contains scripts to generate new studies throughout the day for the demos. There is a branch corresponding to the configuration used in every year of the demo.

## Dependencies
* Python 3
* [RSNA's MIRC Clinical Trial Processor (CTP)](https://mircwiki.rsna.org/index.php?title=MIRC_CTP)
* [dcm4che v5](https://sourceforge.net/projects/dcm4che/files/dcm4che3/)

## Usage
```python main.py -d [PATH TO DICOM FILES] -c [PATH TO CTP] -t [TEAM NAME: dotter, fleischner or mansfield]```

## Example commands for the RSNA IAIP 2022 Demo
```buildoutcfg
python3 main.py -c ~/Apps/ctp -t dotter -l "./logs -d ~/path-to-one-or-more-studies/

python3 main.py -c ~/Apps/ctp -t fleischner -l "./logs -d ~/path-to-one-or-more-studies/

python3 main.py -c ~/Apps/ctp -t mansfield -l "./logs -d ~/path-to-one-or-more-studies/
```
