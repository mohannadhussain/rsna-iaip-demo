# 2021 RSNA Imaging AI in Practice Demo
This repository contains scripts to generate new studies throughout the day for the demos

## Dependencies
* Python 3
* [RSNA's MIRC Clinical Trial Processor (CTP)](https://mircwiki.rsna.org/index.php?title=MIRC_CTP)
* [dcm4che v2](https://sourceforge.net/projects/dcm4che/files/dcm4che2/)
* [dcm4che v5](https://sourceforge.net/projects/dcm4che/files/dcm4che3/)

## Usage
```python main.py -d [PATH TO DICOM FILES] -c [PATH TO CTP] -t [TEAM NAME: curie, hounsfield or rontgen]```
