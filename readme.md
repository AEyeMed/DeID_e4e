### Env

```
conda create -n e4e_env python=3.8
conda activate e4e_env

pip install torch==1.8.0+cu111 torchvision==0.9.0+cu111 torchaudio==0.8.0 -f https://download.pytorch.org/whl/torch_stable.html

pip install -r requirement.txt
```

### StyleGAN Training:

```
cd stylegan2-ada-pytorch

Datasets Preparation:
python dataset_tool.py --source=/your_data_folder --dest=./datasets/dataname.zip --width=512 --height=512 --resize-filter=box

Training:
python train.py --outdir=./training-runs --data=./datasets/fundus512.zip --gpus=1 --cfg=stylegan2 --batch=8

Convert weight to stylegan2 format:
python export_weights.py training-runs/00004-fundus512-stylegan2/network-snapshot-000000.pkl ./checkpoint.pt
```

### e4e Training:

pretrained_models:

1. Download [model_ir_se50.pth](https://drive.google.com/file/d/1KW7bjndL3QG3sxBbZxreGHigcCCpsDgn/view) to encoder4editing/pretrained_models
2. Change the stylegan_weights path in train.sh to the path of checkpoint.pt

```
cd encoder4editing
prepare data:
modify data path code in configs/paths_config.py

1. sh scripts/train.sh
2. sh scripts/inference.sh
```


### VesselEdit

```
change the path of stylegan with xxx.pkl
download the segmentation model and change the segmentation model path

run the jupyternotebook in scripts
```
