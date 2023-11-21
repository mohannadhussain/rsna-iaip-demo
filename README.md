# RSNA Imaging AI in Practice Demo Data Generator
This repository contains scripts to generate new studies throughout the day for the demos. There is a branch corresponding to the configuration used in every year of the demo.

## Dependencies
* Python 3
* [RSNA's MIRC Clinical Trial Processor (CTP)](https://mircwiki.rsna.org/index.php?title=MIRC_CTP)
* [dcm4che v5](https://sourceforge.net/projects/dcm4che/files/dcm4che3/)

## Usage
```python main.py -d [PATH TO DICOM FILES] -c [PATH TO CTP] -t [TEAM NAME: bucky, mallard or jensen]```

### Optional Flags
  * `-nd=true` If specified, generate new study demographics (vs load existing ones from a JSON file)
  * `-g=true` If specified, only generate DICOM files and do NOT send them (no C-STORE, no STOW)
  * `-m=9` If specified generated DICOM files will have a date of 9 months ago, instead of today's today

## Example commands for the RSNA IAIP 2023 Demo

```buildoutcfg
python main.py -c ~/Apps/ctp -t bucky -l "./logs -d ~/path-to-one-or-more-studies/

python main.py -c ~/Apps/ctp -t mallard -l "./logs -d ~/path-to-one-or-more-studies/

python main.py -c ~/Apps/ctp -t jensen -l "./logs -d ~/path-to-one-or-more-studies/
```

### Clean up DICOM Files By Modality
Example of cleaning up SRs:
```
python delete-by-modality.py -m SR -d ~/path-to-one-or-more-studies/
```

### Examples for priors and currents
Step 1: Prior study
```commandline
python main.py -c ~/Apps/ctp -t bucky-john -l "./logs" -d /home/mhussain/projects/rsna/rsna-iaip-demo/W_Chest_PA_3172/ -nd True -m 9
```

Step 2: Current study
```commandline
python main.py -c ~/Apps/ctp -t bucky-john -l "./logs" -d /home/mhussain/projects/rsna/rsna-iaip-demo/W_Chest_PA_3172/
```

## Change Log
### 2023
  * Added the ability to choose whether to generate new demographics or re-use existing ones. Allows for simulating of sending prior studies for the same patient (i.e. comparisons)
  * Added the option for the months offset to generate priors for a patient
  * Added script to clean up SR files vs. outright filtering them out at the CTP level (was being done to ensure AI results samples were not sent with the generated study but rather by the AI model). The change allows to clean up the datasets selectively, because for certian modalities like Ultrasound, we need the SR measurements.   
  * Added a PHP webpage `index.php` that would allow a "self-serve" option to generate studies on demand... Warning: super hacky!!
