# salt_aries

Data reduction scripts for RSS alignment testing

## Installation Instructions

The following scripts require these packages to be installed in order to run.  These can all be installed via pip or conda:

+ numpy
+ scipy
+ matplotlib
+ astropy
+ ccdproc
+ pyqt (wavecal only)
+ pyspectrograph (wavecal only)

At this time, the development versions of this package needs to be installed (required for the wavelength calibration tool only)

+ [specreduce](https://github.com/crawfordsm/specreduce.git)

The specreduce package does depend on [PyQt4](https://riverbankcomputing.com/software/pyqt/intro) package. 

Suggested method for installing most of the necessary packages via anaconda

    conda create --name aries -y python=2.7 astropy pyqt matplotlib 
    source activate aries
    conda install -c astropy ccdproc specutils
    pip install pyspectrograph 
    git clone https://github.com/crawfordsm/specreduce
    cd specreduce
    python setup.py develop
    cd 
    git clone https://github.com/janusbrink/salt_aries


## Instructions

To perform basic data reductions, follow these steps:

### Configuration
The Region of Interest (ROI) for the spectrum and background is defined in aries_roi.py:

    # region on interest definition
    roi = {
            'yc': 107,      # Centre row of spectrum
            'dy': 30,       # Half-width of spectrum in rows
            'bg1': 200,     # Background region start row
            'bg2': 315,     # Background region end row
        }

The wavelength calibration is defined in aries_wcal.py:

    # wavelength cal table
    #  wavelength [A], wl at x=0 [A], disp [A/pixel]
    wcaldict = {
        3500: (3786.82740000956, -0.7160),
        4000: (4283.04591640358, -0.7140),
        4500: (4781.16982674218, -0.7112),
        5000: (5278.33868815227, -0.7085),
        5500: (5776.06936014866, -0.7053),
        6000: (6274.35744728712, -0.7015),
        6500: (6772.32951675212, -0.6992),
        7000: (7271.75813080403, -0.6958),
        7500: (7771.30906597260, -0.6931),
        8000: (8268.25741607708, -0.6884),
        8500: (8766.04451394839, -0.6840),
        9000: (9263.24690748274, -0.6796)
        }



### Run the basic image reductions on the data.   

Pass the names of the files to the `aprep` script to reduce each file.   There are in addition several optional flags that can be passed to remove a bias frame, dark frame, etc. Output files have a 'p' prefix.

    aprep [files to be reduced] [--d dark_file] [--b bias file]
    
Typically background subtraction from a region above the spectrum is sufficient.

Example:

    aprep image*
    
The output files are prefixed with `p`

### Produce difference spectra
To plot the difference spectra of a single data set (a pair of images):

    adiff [ref_file] [test_file] 

Example:

    adiff pimage001.fit pimage002.fit --wref 3500
    
The optional `wref` flag indicates the wavelength calibration configuration entry to use when plotting the data.

### Reduce all data in folder
    arundiff [list of files]

arundiff calls `aries_diff_all.py` that contains the test setup of files in the folder.

Example:

    arundiff pimage*
    
Output for each image pair is saved as `throughput_xxxx.txt` and the combined output is available in `combined.txt`.
