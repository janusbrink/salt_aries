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
    conda activate aries
    conda install -c astropy ccdproc specutils
    mkdir aries
    cd aries 
    git clone https://github.com/janusbrink/salt_aries

NOTE: If plots do not display on Mac - change:
    ~/.matplotlib/matplotlibrc and add:
    backend: MacOSX


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
    #  wavelength [nm], wl at x=0 [nm], disp [nm/pixel]
    wcaldict = {
         350: (293.2687, 0.075744),
         400: (343.3987, 0.075479),
         450: (393.5357, 0.075196),
         500: (443.6857, 0.074895),
         550: (493.8437, 0.074575),
         600: (544.0107, 0.074238),
         650: (593.4949, 0.075834),
         700: (644.3727, 0.073507),
         750: (694.5677, 0.073112),
         800: (744.7717, 0.072700),
         850: (794.9887, 0.072270),
         900: (845.2147, 0.071817),
         }

### Run the basic image reductions on the data.   

Pass the names of the files to the `aprep` script to reduce each file.   There are in addition several optional flags that can be passed to remove a bias frame, dark frame, etc. Output files have a 'p' prefix.

    aprep [files to be reduced] [--d dark_file] [--b bias file]
    
Typically background subtraction from a region next to the spectrum is sufficient.

Example:

    aprep image*
    
The output files are prefixed with `p`

### Produce difference spectra
To plot the difference spectra of a single data set (a pair of images):

    adiff [ref_file] [test_file] 

Example:

    adiff pimage001.fit pimage002.fit --wref 350
    
The optional `wref` flag indicates the wavelength calibration configuration entry to use when plotting the data.

### Reduce all data in folder
    arundiff [list of files]

arundiff calls `aries_diff_all.py` that contains the test setup of files in the folder:
 cfglist = (
     ('out', 'in', 350),
     ('out', 'in', 400),
     ('out', 'in', 450),
     ('out', 'in', 500),
     ('out', 'in', 550),
     ('out', 'in', 600),
     ('out', 'in', 650),
     ('out', 'in', 700),
     ('out', 'in', 750),
     ('out', 'in', 800),
     ('out', 'in', 850),
     ('out', 'in', 900)
     )

Example:

    arundiff pimage*
    
Output for each image pair is saved as `throughputnn_xxxx.txt` and the combined output is available in `combined.txt`.
