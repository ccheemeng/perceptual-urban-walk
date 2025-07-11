# Download Panoramas  

[DownloadPanoramas.py](./DownloadPanoramas.py) is a utility to download street
 imagery via the [streetlevel](https://streetlevel.readthedocs.io/) API.  

#### Input  

* Two corner coordinates defining a query rectangle in EPSG:3414, or  
* A query polygon described via a ```.geojson``` in any coordinate system  

#### Output  

* A directory containing panoramas found within the query area, and  
* A ```<name>.csv``` with xyz coordinates for each panorama  

Outputs are always written in EPSG:3414.    

## Installation  

Reproduced from
 [Conda's user guide](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-from-an-environment-yml-file).  

1. Create the environment from the ```environment.yml``` file:  
    ```
    conda env create -f environment.yml
    ```
2. Activate the new environment:  
    ```
    conda activate download-panoramas
    ```
3. Verify that the new environment was installed correctly:  
    ```
    conda env list
    ```
    You can also use ```conda info --envs```.  

## Running  

[downloadPanoramas.sh](./downloadPanoramas.sh) has been provided to work with
 the provided test [GeylangBahru](../GeylangBahru/) input. To run it:  
```
./downloadPanoramas.sh
```

Refer to the arguments list below to modify the behaviour of the utility.  

## Arguments  

| Name           | Flags    | Type        | Description                                                                                                                                                | Required    | Default |
|----------------|----------|-------------|------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------|---------|
| ```p1```       | -        | ```float``` | x and y coordinates of p1                                                                                                                                  | ```False``` | -       |
| ```p2```       | -        | ```float``` | x and y coordinates of p2                                                                                                                                  | ```False``` | -       |
| ```out```      | ```-o``` | ```str```   | Directory to create panorama directory in                                                                                                                  | ```True```  | -       |
| ```boundary``` | ```-b``` | ```str```   | ```.geojson``` to read query polygon from                                                                                                                  | ```False``` | -       |
| ```name```     | ```-n``` | ```str```   | Name of panorama directory and coordinate ```.csv```, derived from ```out``` basename if not provided                                                      | ```False``` | -       |
| ```res```      | ```-r``` | ```float``` | Maximum orthogonal distance between sample points in metres                                                                                                | ```False``` | 10.0    |
| ```zoom```     | ```-z``` | ```int```   | 0 to 5 inclusive, refer to [streetlevel](https://streetlevel.readthedocs.io/en/master/streetlevel.streetview.html#streetlevel.streetview.get_panorama) API | ```False``` | 1       |