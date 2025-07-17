# Cluster Samples  

[cluster_samples.py](./cluster_samples.py) is a script to cluster sample point cloud encodings based on a pretrained k-means model.  

#### Input  

* A scikit-learn [StandardScaler](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html) as a joblib ```.pkl``` file with the following attributes:  
    * ```n_features_in_```: 1024  
* A scikit-learn [PCA](https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html#sklearn.decomposition.PCA) as a joblib ```.pkl``` file with the following attributes:  
    * ```n_features_in_```: 1024  
    * ```n_components_```: 8  
* A scikit-learn [KMeans](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html) as a joblib ```.pkl``` file with the following attributes:  
    * ```n_features_in_```: 8  
* A directory containing encodings of the point clouds as ```.json``` files  

The attributes may be different if they follow the dimensionality of the data.   

#### Output  

* A ```.csv``` file describing the cluster each sample is predicted to belong to  

## Installation  

Create the environment from the ```cluster-samples.yml``` environment file and activate it.  
```shell
conda env create -f cluster-samples.yml
conda activate cluster-samples
```

## Running  

[cluster_samples.sh](./cluster_samples.sh) has been provided to work with
 the provided test [GeylangBahru](../GeylangBahru/) input. To run it:  
```shell
./cluster_samples.sh
```

## Arguments  

| Name            | Flags    | Type      | Description                                                             | Required   | Default |
|-----------------|----------|-----------|-------------------------------------------------------------------------|------------|---------|
| ```scaler```    | ```-s``` | ```str``` | StandardScaler as a joblib ```.pkl``` file                              | ```True``` | -       |
| ```pca```       | ```-r``` | ```str``` | PCA as a joblib ```.pkl``` file                                         | ```True``` | -       |
| ```kmeans```    | ```-k``` | ```str``` | KMeans as a joblib ```.pkl``` file                                      | ```True``` | -       |
| ```encodings``` | ```-e``` | ```str``` | Directory containing encodings of the point clouds as ```.json``` files | ```True``` | -       |
| ```out```       | ```-o``` | ```str``` | Directory to create output ```.csv``` file in                           | ```True``` | -       |