# salt_aries

Data reduction scripts for RSS alignment testing

## Installation Instructions

The following scripts require these packages to be installed in order to run.  These can all be installed via pip or conda:

+ numpy
+ scipy
+ matplotlib
+ astropy
+ ccdproc
+ astroscrappy
+ pyspectrorgaph
+ pyqt


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

### Run the basic image reductions on the data.   

Pass the names of the files to the `aprep` script to reduce each file.   There are in addition several optional flags that can be passed to remove a bias frame, dark frame, etc. Output files have a 'p' prefix.

    aprep [files to be reduced] [--d dark_file] [--b bias file]

### Create wave maps for each of the arc frames
    python aries_measure_arc.py [arc file]

### Produce difference spectra
    adiff [ref_file] [test_file] 

### Reduce all data in folder
    arundiff [list of files]

arundiff calls `aries_diff_all.py` that contains the test setup of files in the folder as well as the linear wavelength calibration data.
