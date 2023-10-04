# RSNA Imaging AI in Practice Demo Data Generator
This repository contains scripts to generate new studies throughout the day for the demos. There is a branch corresponding to the configuration used in every year of the demo.

## Dependencies
* Python 3
* [RSNA's MIRC Clinical Trial Processor (CTP)](https://mircwiki.rsna.org/index.php?title=MIRC_CTP)
* [dcm4che v5](https://sourceforge.net/projects/dcm4che/files/dcm4che3/)

## Usage
```python main.py -d [PATH TO DICOM FILES] -c [PATH TO CTP] -t [TEAM NAME: bucky, mallard or jensen]```

### Optional Flags
  * `-nd` If specified, generate new study demographics (vs load existing ones from a JSON file)
  * `-g` If specified, only generate DICOM files and do NOT send them (no C-STORE, no STOW)

## Example commands for the RSNA IAIP 2023 Demo

```buildoutcfg
python main.py -c ~/Apps/ctp -t bucky -l "./logs -d ~/path-to-one-or-more-studies/

python main.py -c ~/Apps/ctp -t mallard -l "./logs -d ~/path-to-one-or-more-studies/

python main.py -c ~/Apps/ctp -t jensen -l "./logs -d ~/path-to-one-or-more-studies/

# Clean up SRs
python delete-srs.py -d ~/path-to-one-or-more-studies/
```
## Change Log
### 2023
  * Added the ability to choose whether to generate new demographics or re-use existing ones. Allows for simulating of sending prior studies for the same patient (i.e. comparisons)
  * Added script to clean up SR files vs. outright filtering them out at the CTP level (was being done to ensure AI results samples were not sent with the generated study but rather by the AI model). The change allows to clean up the datasets selectively, because for certian modalities like Ultrasound, we need the SR measurements.   
