# Download Panoramas  

[download_panoramas.py](./download_panoramas.py) is a script to download street
 imagery via the [streetlevel](https://streetlevel.readthedocs.io/) API.  

#### Input  

* Two corner coordinates defining a query rectangle in EPSG:3414, or  
* A query polygon described via a ```.geojson``` in any coordinate system  

#### Output  

* A directory containing panoramas found within the query area, and  
* A ```<name>-coords.csv``` with xyz coordinates for each panorama  

Outputs are always written in EPSG:3414.  

## Installation  

Reproduced from
 [Conda's user guide](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-from-an-environment-yml-file).  

1. Create the environment from the ```environment.yml``` file:  
    ```shell
    conda env create -f environment.yml
    ```
2. Activate the new environment:  
    ```shell
    conda activate download-panoramas
    ```
3. Verify that the new environment was installed correctly:  
    ```shell
    conda env list
    ```
    You can also use ```conda info --envs```.  

## Running  

[download_panoramas.sh](./download_panoramas.sh) has been provided to work with
 the provided test [GeylangBahru](../GeylangBahru/) input. To run it:  
```shell
./download_panoramas.sh
```

## Arguments  

| Name           | Flags    | Type        | Description                                                                                                                                                | Required    | Default |
|----------------|----------|-------------|------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------|---------|
| ```p1```       | -        | ```float``` | x and y coordinates of p1                                                                                                                                  | ```False``` | -       |
| ```p2```       | -        | ```float``` | x and y coordinates of p2                                                                                                                                  | ```False``` | -       |
| ```out```      | ```-o``` | ```str```   | Directory to create panorama directory in                                                                                                                  | ```True```  | -       |
| ```boundary``` | ```-b``` | ```str```   | ```.geojson``` file to read query polygon                                                                                                                  | ```False``` | -       |
| ```name```     | ```-n``` | ```str```   | Name of panorama directory and coordinate ```.csv```, derived from ```out``` basename if not provided                                                      | ```False``` | -       |
| ```res```      | ```-r``` | ```float``` | Maximum orthogonal distance between sample points in metres                                                                                                | ```False``` | 10.0    |
| ```zoom```     | ```-z``` | ```int```   | 0 to 5 inclusive, refer to [streetlevel](https://streetlevel.readthedocs.io/en/master/streetlevel.streetview.html#streetlevel.streetview.get_panorama) API | ```False``` | 1       |