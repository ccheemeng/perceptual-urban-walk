# Generate Env  

Two shell scripts are provided here:  
1. [generate_env.sh](./generate_env.sh) to procedurally generate an urban environment in terms of regions, and the urban attributes and buildings included in those regions, through a query site, and  
2. [generate_env_pc.sh](./generate_env_pc.sh) to generate the point cloud for the generated environment by referencing the described regions from the query site  

Generation is done via [perceptual-env-gen](https://github.com/ccheemeng/perceptual-env-gen/).  

### Generate Env  

#### Input  

* A query site:  
    * Point samples in the query site as a GeoDataFrame in a ```.geojson``` file,  
    * Sample regions for each sample as a GeoDataFrame in a ```.geojson``` file,  
    * The cluster each sample belongs to described in a ```.csv``` file, and  
    * Building footprints with urban attributes in a ```.geojson``` file  
* A test site:  
    * Point samples in the test site as a GeoDataFrame in a ```.geojson``` file,  
    * Sample regions for each sample as a GeoDataFrame in a ```.geojson``` file,  
    * The cluster each sample belongs to described in a ```.csv``` file,  
    * Polygon\(s\) describing the site as a ```.geojson``` file, and  
    * Urban attribute targets for the generation described in a ```.csv``` file  

#### Output  

* A directory for each site polygon, each containing:  
    * The samples taken from the query site as a ```.csv``` file, ```perceptions.csv```,  
    * The multipolygon that corresponds to each sample as a ```.geojson``` file, ```polygons.geojson```,  
    * The building footprints that correspond to each sample as a ```.geojson``` file, ```buildings.geojson```,  
    * The urban attributes of each sample as a ```.csv``` file, ```attributes.csv```, and  
    * The additional samples that were brought in under each main sample but not used in generation, ```.samples.csv```  

### Generate Env PC  

#### Input  

* The directory containing the generation output for each test site polygon, and  
* The directory containing point clouds corresponding to each sample from the query site<sup>[how to get](#query-pc)</sup>  

#### Output  

* A point cloud describing the generation for each test site polygon  

## Installation  

For both scripts, create the environment from the ```generate-env.yml``` environment file and activate it.  
```shell
conda env create -f generate-env.yml
conda activate generate-env
```

For [generate_env_pc.sh](./generate_env_pc.sh), obtain query site point clouds from <a name="query-pc">[perceptual-env-gen's releases](https://github.com/ccheemeng/perceptual-env-gen/releases/tag/v0.1.1)</a>. Unzip all files and save all ```.csv``` files in a directory ```./beautyworld-sample-pc/```.  

## Running 

Run generate_env.sh then generate_env_pc.sh.  
The shell scripts are intended to work with the provided test [GeylangBahru](../GeylangBahru/) input. To run it:  
```shell
./generate_env.sh
./generate_env_pc.sh
```

## Arguments  

generate_env.sh and generate_env_pc.sh calls [Main.py](./perceptual-env-gen/Main.py) and [Generate.py](./perceptual-env-gen/Generate.py) within [perceptual-env-gen](./perceptual-env-gen/).  

### Main.py  

| Name            | Flags    | Type        | Description                                                                                 | Required   | Default |
|-----------------|----------|-------------|---------------------------------------------------------------------------------------------|------------|---------|
| ```query```     | ```-q``` | ```3 str``` | (1) Query site point samples, (2) query site sample regions, (3) query site sample clusters | ```True``` | -       |
| ```site```      | ```-s``` | ```3 str``` | (1) Test site point samples, (2) test site sample regions, (3) test site sample clusters    | ```True``` | -       |
| ```polygons```  | ```-p``` | ```str```   | Test site polygons                                                                          | ```True``` | -       |
| ```target```    | ```-t``` | ```str```   | Test site target attributes                                                                 | ```True``` | -       |
| ```buildings``` | ```-a``` | ```str```   | Query site building footprints                                                              | ```True``` | -       |
| ```out```       | ```-o``` | ```str```   | Directory to create output directories in                                                   | ```True``` | -       |

### Generate.py  

| Name          | Flags | Type      | Description                                                                            | Required   | Default |
|---------------|-------|-----------|----------------------------------------------------------------------------------------|------------|---------|
| ```gen-dir``` | -     | ```str``` | Directory containing the generation output for each test site polygon                  | ```True``` | -       |
| ```pc-dir```  | -     | ```str``` | Directory containing the point clouds corresponding to each sample from the query site | ```True``` | -       |
