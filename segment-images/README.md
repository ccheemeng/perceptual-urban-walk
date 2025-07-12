# Segment Images  

[segment_images.py](./segment_images.py) is a utility to semantically segment images via [MMSegmentation](https://mmsegmentation.readthedocs.io/).  

By default, the models provided here segment images according to [Cityscapes](https://www.cityscapes-dataset.com/) labels. [classes.json](./classes.json) is provided as a reference for class labels.  

#### Input  

* A directory of panoramas (images)  

#### Output  

* A directory of semantically segmented panoramas as ```.json``` files, and
* [Optional] A directory of the segmentations visualised.  

## Installation  

Ensure the following requirements are installed:  
1. Python 3.11.13
2. [PyTorch 2.1.2](https://pytorch.org/get-started/previous-versions/)
3. [MMCV 2.1.0](https://mmcv.readthedocs.io/) for MMSegmentation  
4. MMSegmentation 1.2.2  
5. NumPy < 2

Other software version combinations may work but are untested.  

I have provided my preferred method of installing the above requirements for my system (CUDA 12.2) with conda and pip:  
```shell
conda create -n segment-images python=3.11.13 -y
conda activate segment-images
pip install torch==2.1.2 torchvision==0.16.2 torchaudio==2.1.2 --index-url https://download.pytorch.org/whl/cu121
pip install ftfy==6.3.1 mmcv==2.1.0 -f https://download.openmmlab.com/mmcv/dist/cu121/torch2.1/index.html mmsegmentation==1.2.2 numpy==1.26.0 opencv-python-headless==4.11.0.86 regex==2024.11.6
```

The [config file](./configs/fcn/fcn-d6_r101-d16_4xb2-80k_cityscapes-512x1024.py) and checkpoint link for an FCN baseline trained on the Cityscapes dataset are provided here, but a full list of models may be accessed via MMSegmentation's [model zoo](https://github.com/open-mmlab/mmsegmentation/blob/main/docs/en/model_zoo.md).  

## Running  

```segment_images.sh``` has been provided to work with the provided test [GeylangBahru](../GeylangBahru/) input. To run it:  
```shell
./segment_images.sh
```
If desired, replace the checkpoint link in the file, and ensure that the necessary config and base files are also downloaded.  

## Arguments  

| Name                 | Flags    | Type      | Description                                                                                         | Required    | Default                                         |
|----------------------|----------|-----------|-----------------------------------------------------------------------------------------------------|-------------|-------------------------------------------------|
| ```config```         | -        | ```str``` | Config file path                                                                                    | ```True```  | -                                               |
| ```checkpoint```     | -        | ```str``` | Checkpoint file path, required if ```checkpoint-url``` not provided                                 | ```False``` | -                                               |
| ```checkpoint-url``` | -        | ```str``` | Checkpoint file URL, required if ```checkpoint``` not provided                                      | ```False``` | -                                               |
| ```input```          | ```-i``` | ```str``` | Directory containing input panoramas (images)                                                       | ```True```  | -                                               |
| ```out```            | ```-o``` | ```str``` | Directory to create output directories in                                                           | ```True```  | -                                               |
| ```name```           | ```-n``` | ```str``` | Name of segmentation and visualisation directories, derived from ```out``` basename if not provided | ```False``` | -                                               |
| ```no-viz```         | -        | -         | If used, visualisations will not be generated                                                       | ```False``` | -                                               |
| ```device```         | ```-d``` | ```str``` | Device to run inference on                                                                          | ```False``` | ```cuda``` if CUDA is available, else ```cpu``` |