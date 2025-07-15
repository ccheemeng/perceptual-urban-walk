# Encode PC  

[encode_pc.py](./encode_pc.py) is a utility to encode labelled point clouds via [labelled-pointnet-autoencoder](https://github.com/ccheemeng/labelled-pointnet-autoencoder/).  

#### Input  

* A directory containing labelled point clouds as ```.csv``` files  

#### Output  

* A directory containing encodings of the point clouds as ```.json``` files  

## Installation  

Ensure the following requirements are installed:  
1. Python 3.11.13
2. [PyTorch 2.5.1](https://pytorch.org/get-started/previous-versions/)
3. Pandas 2.3.1

Other software version combinations may work but are untested.  

I have provided my preferred method of installing the above requirements for my system (CUDA 12.2) with conda and pip:  
```shell
conda create -n encode-pc anaconda::python=3.11.13 conda-forge::pandas=2.3.1 pytorch==2.5.1 torchvision==0.20.1 torchaudio==2.5.1 pytorch-cuda=12.1 -c pytorch -c nvidia -y
conda activate encode-pc
```

Obtain a model weights state dictionary by training according to [labelled-pointnet-autoencoder](https://github.com/ccheemeng/labelled-pointnet-autoencoder/) or find pretrained weights from the repository's [releases](https://github.com/ccheemeng/labelled-pointnet-autoencoder/releases):  
```shell
wget https://github.com/ccheemeng/labelled-pointnet-autoencoder/releases/download/v0.1.1/best-model-state-dict.pt
```

## Running  

[encode_pc.sh](./encode_pc.sh) has been provided to work with the provided test [GeylangBahru](../GeylangBahru/) input. To run it:  
```shell
./encode_pc.sh
```

## Arguments  

| Name              | Flags    | Type      | Description                                                    | Required    | Default                                         |
|-------------------|----------|-----------|----------------------------------------------------------------|-------------|-------------------------------------------------|
| ```dataset```     | ```-d``` | ```str``` | Directory containing labelled point clouds as ```.csv``` files | ```True```  | -                                               |
| ```weights```     | ```-w``` | ```str``` | Model weights state dictionary                                 | ```True```  | -                                               |
| ```out```         | ```-o``` | ```str``` | Directory to create output files in                            | ```True```  | -                                               |
| ```device```      | -        | ```str``` | Device to run inference on                                     | ```False``` | ```cuda``` if CUDA is available, else ```cpu``` |
| ```max-points```  | ```-n``` | ```int``` | The number of points in each point cloud                       | ```False``` | 16384                                           |
| ```num-classes``` | ```-c``` | ```int``` | Number of point labels                                         | ```False``` | 19                                              |