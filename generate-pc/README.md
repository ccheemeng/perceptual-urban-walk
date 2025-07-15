# Generate PC  

Two Python scripts are provided here:  
1. [project_segmentations.py](./project_segmentations.py) to project panorama segmentations onto a extrusions of building footprints, and  
2. [generate_sample_pc.py](./generate_sample_pc.py) to generate point clouds using polygon regions to clip the projected segmentations  

### Project Segmentations  

#### Input  

* A ```.csv``` file describing the coordinates of each panorama,  
* A directory of semantically segmented panoramas as ```.json``` files, and  
* Building footprints described via a ```.geojson``` file in EPSG:3414  

#### Output  

* A directory containing labelled point clouds as ```.csv``` files by projecting the panorama segmentations on extrusions of the building footprints  

### Generate Sample PC  

#### Input  

* A directory containing ```.csv``` files per sample describing the panoramas required to build that sample,  
* A directory containing ```.geojson``` files per sample describing the sample region  
* A directory containing labelled point clouds as ```.csv``` files by projecting the panorama segmentations on extrusions of the building footprints  

#### Output  

* A directory containing labelled point clouds as ```.csv``` files by clipping the projected segmentations with the sample regions  

## Installation  

For both scripts, create the environment from the respective ```.yml``` environment file and activate it.  

### Project Segmentations  

```shell
conda env create -f project-segmentations.yml
conda activate project-segmentations
```

### Generate Sample PC  

```shell
conda env create -f generate-sample-pc.yml
conda activate generate-sample-yml
```

## Running  

Run project_segmentations.py then generate_sample_pc.py.  

Shell scripts have been provided to work with the provided test [GeylangBahru](../GeylangBahru/) input. To run it:  
```shell
./project_segmentations.sh
./generate_sample_pc.sh
```

## Arguments  

### Project Segmentations  

| Name                 | Flags    | Type        | Description                                           | Required    | Default  |
|----------------------|----------|-------------|-------------------------------------------------------|-------------|----------|
| ```points```         | ```-p``` | ```str```   | ```.csv``` file to read panorama coordinates from     | ```True```  | -        |
| ```segmentations```  | ```-s``` | ```str```   | Directory containing semantically segmented panoramas | ```True```  | -        |
| ```buildings```      | ```-b``` | ```str```   | ```.geojson``` file describing building footprints    | ```True```  | -        |
| ```out```            | ```-o``` | ```str```   | Directory to create output files in                   | ```True```  | -        |
| ```exclude-labels``` | ```-e``` | ```* int``` | Semantic labels to exclude                            | ```False``` | ```[]``` |

### Generate Sample PC  

| Name                | Flags    | Type      | Description                                                                                                                                                  | Required    | Default |
|---------------------|----------|-----------|--------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------|---------|
| ```points```        | ```-p``` | ```str``` | Directory containing ```.csv``` files describing the panoramas required to build each sample                                                                 | ```True```  | -       |
| ```regions```       | ```-r``` | ```str``` | Directory containing ```.geojson``` files describing the sample regions for each sample                                                                      | ```True```  | -       |
| ```segmentations``` | ```-s``` | ```str``` | Directory containing point clouds of projected semantically segmented panoramas                                                                              | ```True```  | -       |
| ```out```           | ```-o``` | ```str``` | Directory to create output files in                                                                                                                          | ```True```  | -       |
| ```batch-size```    | ```-b``` | ```int``` | How many samples are created in each iteration<sup>[*](#batch-size)</sup>                                                                                    | ```False``` | 500     |
| ```sample-size```   | -        | ```int``` | The number of points in each sample                                                                                                                          | ```False``` | 65536   |
| ```write-small```   | -        | -         | If used, will write samples with less points than ```sample-size```                                                                                          | ```False``` | -       |
| ```no-sample```     | -        | -         | If used, supersedes ```sample-size``` and ```write-small``` and writes [ALL](#no-sample-warning) points from segmented panoramas contributing to each sample | ```False``` | -       |

Note:  
* <a name="batch-size">Unless training on a HPC system or a system with a lot of RAM, use a ```batch-size``` much more conservative than the default.<br>As a guide, a batch size of <b>10</b> safely works on a system with <b>32GiB of RAM</b>, but a size up to 20 is possible.<br>The script may be resumed in the event that the program runs out of memory.</a>  
* <a name="no-sample-warning">I do not recommend using ```no-sample```.</a>