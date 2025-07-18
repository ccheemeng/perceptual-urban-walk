# Download Panoramas  

[download_panoramas.py](./download_panoramas.py) is a script to download street
 imagery via the [streetlevel](https://streetlevel.readthedocs.io/) API.  

#### Input  

* Two corner coordinates defining a query rectangle in EPSG:3414, or  
* A query polygon described via a ```.geojson``` in any coordinate system  

#### Output  

* A directory containing panoramas found within the query area, and  
* A ```.csv``` file with xyz coordinates for each panorama  

Outputs are always written in EPSG:3414.  

## Installation  

Create the environment from the ```download-panoramas.yml``` environment file and activate it.  
```shell
conda env create -f download-panoramas.yml
conda activate download-panoramas
```

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
| ```boundary``` | ```-b``` | ```str```   | ```.geojson``` file to read query polygon from                                                                                                             | ```False``` | -       |
| ```name```     | ```-n``` | ```str```   | Name of panorama directory and coordinate ```.csv``` file, derived from ```out``` basename if not provided                                                 | ```False``` | -       |
| ```res```      | ```-r``` | ```float``` | Maximum orthogonal distance between sample points in metres                                                                                                | ```False``` | 10.0    |
| ```zoom```     | ```-z``` | ```int```   | 0 to 5 inclusive, refer to [streetlevel](https://streetlevel.readthedocs.io/en/master/streetlevel.streetview.html#streetlevel.streetview.get_panorama) API | ```False``` | 1       |
