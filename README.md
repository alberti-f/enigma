
# ENIGMA Consortium - Joint-Variation Graph Analysis

This project was developed to analyze structural MRI data of the ENIGMA consortium. This script uses previously extracted morphological data to compute individualized joint-variantion graphs of cortical thickness, extracts a set of topological properties of such graphs, and computes descriptive statistics for meta-analysis. 
Specifically, this script was created to investigate alterations in patterns of cortical thickness in individuals with anorexia nervosa.
To participate to the study, please follow the following instructions to install Docker desktop, run the analyses, and share the results with our team for cross-center meta-analysis.



## 1. Docker download & setup

The project uses a preconfigdoured environment setup in a Docker container, so the first step is downloading, installing and setting up Docker Desktop to work correctly with your subsystem.  
To do this, download the software installer from the Docker Desktop [download page](https://www.docker.com/products/docker-desktop/) and follow the installation instructions for your system:
  * [**Windows**](https://docs.docker.com/desktop/install/windows-install/)
  * [**Linux**](https://docs.docker.com/desktop/install/linux-install/)
  * [**Mac**](https://docs.docker.com/desktop/install/mac-install/)  

Additional information can be found on the official [Docker Desktop documentation](https://docs.docker.com/desktop/).



## 2. Download the repository to your machine

###  Visual interface  
  1. Open the **Code** dropdown menu
  2. Click on the **Download Zip** option
  3. **Extract** the .zip folder to a directory of your choice

### Command line
  1. If you do not have it altready installed, download and install [git](https://git-scm.com/downloads) on your system
  2. Type the following command into the terminal:
```bash
  git clone https://github.com/alberti-f/enigma.git
```



## 3. Set up script and data

  1. Open the `docker-compose.yaml` file and change the `user` entry to your username
```yaml
.
.
  panel:
    build:
      args:
        user: "YOUR-USER-NAME"
.
.
```

  2. Copy the following files to the `data` directory:
     - `CorticalMeasuresENIGMA_ThickAvg.csv`
     - `SubcorticalMeasuresENIGMA_VolAvg.csv`
     - `Covariates.csv`

     These files are part of the outputs generated by the scripts of the original ENIGMA study on AN

  3. Give read, write, and execute permissions for everyone to the `data` and `output` directories and to the `log.txt` file 

```bash
  cd /full/path/to/enigma   # change directory to the enigma folder
  chmod 777 data/           # Give full permissions to data folder
  chmod 777 output/         # Give full permissions to output folder
  chmod 777 output/log.txt  # Give full permissions to the log file
```



## 4. Launch the analyses

Now you are ready to build the Docker image and run the analyses:
```bash
  cd /full/path/to/enigma   # change directory to the enigma folder
  docker compose up         # build docker image and launch analysis scripts
```

## 5. Share the compressed output folder with the Authors for meta-analysis
At the end of the image build process, the analisis script will run and generate several output files in the `output` directory. Among them, you will find also a compressed copy of output `output.tar.gz`.
Please share this folder with our team sending it to:
**enrico.collantoni@unipd.it**



## Support
For support, please contact us at:
  * **enrico.collantoni@unipd.it**
  * **francesco.alberti@etu.u-paris.fr**


## License

[MIT](https://choosealicense.com/licenses/mit/)
