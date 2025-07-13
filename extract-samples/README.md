# Extract Samples  

Two Python scripts are provided here:  
1. [generate_roads.py](./generate_roads.py) to generate a road network graph with vertices tied to each panorama and its coordinates, and  
2. [extract_samples.py](./extract_samples.py) to extract sample points and regions from the generated road network  

### Generate Roads  

#### Input  

* A ```.csv``` file describing the coordinates of each panorama  

#### Output  

* An adjacency list as a ```.json``` file,  
* A ```.csv``` file describing the vertices of the graph, and  
* A ```.csv``` file describing the edges of the graph  

### Extract Samples  

#### Input  

* An adjacency list as a ```.json``` file,  
* A ```.csv``` file describing the vertices of the graph, and  
* A boundary polygon described via a ```.geojson``` in a coordinate system matching that of the vertices  

#### Output  

* A directory containing ```.csv``` files per sample describing the panoramas required to build that sample, and  
* A directory containing ```.geojson``` files per sample describing the sample region  

## Installation  

Reproduced from
 [Conda's user guide](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-from-an-environment-yml-file).  

1. Create the environment from the ```environment.yml``` file:  
    ```shell
    conda env create -f extract-samples.yml
    ```
2. Activate the new environment:  
    ```shell
    conda activate extract-samples
    ```
3. Verify that the new environment was installed correctly:  
    ```shell
    conda env list
    ```
    You can also use ```conda info --envs```.  

## Running  

Run generate_roads.py then extract_samples.py.  
Shell scripts have been provided to work with the provided test [GeylangBahru](../GeylangBahru/) input. To run it:  
```shell
./generate_roads.sh
./extract_samples.sh
```

## Arguments  

### Generate Roads  

| Name               | Flags    | Type        | Description                                                                 | Required    | Default |
|--------------------|----------|-------------|-----------------------------------------------------------------------------|-------------|---------|
| ```coords```       | ```-c``` | ```str```   | ```.csv``` to read panorama coordinates from                                | ```True```  | -       |
| ```has-header```   | -        | -           | Use if ```coords``` file has a header row                                   | ```False``` | -       |
| ```use-id```       | -        | -           | If used, panorama IDs will used as vertex IDs                               | ```False``` | -       |
| ```use-z```        | -        | -           | If used, z coordinate will be taken into account when creating road network | ```False``` | -       |
| ```out```          | ```-o``` | ```str```   | Directory to create output files in                                         | ```True```  | -       |
| ```name```         | ```-n``` | ```str```   | Name of output files, derived from ```out``` basename if not provided       | ```False``` | -       |
| ```id-idx```       | ```-i``` | ```int```   | Index of column in ```coords``` file containing panorama IDs                | ```False``` | 0       |
| ```x-idx```        | ```-x``` | ```int```   | Index of column in ```coords``` file containing x coordinates               | ```False``` | 1       |
| ```y-idx```        | ```-y``` | ```int```   | Index of column in ```coords``` file containing y coordinates               | ```False``` | 2       |
| ```z-idx```        | ```-z``` | ```int```   | Index of column in ```coords``` file containing z coordinates               | ```False``` | 3       |
| ```max-edge-len``` | ```-l``` | ```float``` | Maximum possible euclidean length for an edge to connect two vertices       | ```False``` | 15.0    |

### Extract Samples  

| Name              | Flags    | Type      | Description                                                                                                                  | Required    | Default |
|-------------------|----------|-----------|------------------------------------------------------------------------------------------------------------------------------|-------------|---------|
| ```adjacencies``` | ```-a``` | ```str``` | ```.json``` file to read adjacency list from                                                                                 | ```True```  | -       |
| ```points```      | ```-p``` | ```str``` | ```.csv``` file to read vertex coordinates from                                                                              | ```True```  | -       |
| ```boundary```    | ```-b``` | ```str``` | ```.geojson``` file to read boundary polygon from                                                                            | ```True```  | -       |
| ```out```         | ```-o``` | ```str``` | Directory to create output files in                                                                                          | ```True```  | -       |
| ```name```        | ```-n``` | ```str``` | Name of output files, derived from ```out``` basename if not provided                                                        | ```False``` | -       |
| ```num-queries``` | ```-n``` | ```int``` | The minimum number of samples that will be generated is guaranteed to be min(```num-queries```, number of vertices in graph) | ```False``` | 1024    |