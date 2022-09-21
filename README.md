
# TinyUStaging

### TinyUStaging: An Efficient Model for Sleep Staging with Single-Channel EEG and EOG

![image-20220921113347382](https://s2.loli.net/2022/09/21/s4P8HuF7lTgWO5p.png)

- See HD figure in `supplementary_materials\Figures\FigS1.tif`

#### Codes

- The source code will be made public after the paper is accepted. 
  - The model framework has been open sourced, see `bin/defaults`

- Welcome to submit issues to promote my work!

#### Workflow

- Schematic illustration of our TinyUStaging workflow

  ![](https://s2.loli.net/2022/09/21/uUevaWczIrKCVBm.png)

  - **Data.** We selected any combination of 'EEG+EOG'. 
  - **Cross-validation**. we applied *5-fold subject-wise cross-validation* on seven datasets totaling above 750G, in each fold, *75%, 10%, and 15%* of the data were utilized to train, validate and evaluate the model. 
  - **Pre-Processing.** We conducted data scaling and data enhancement methods to make the model more robust. 
  - **Model.** We trained a 4-layer U-Net including Encoder, Decoder and Random Window Classifier (RWC) with SE and CSJA module. 
  - **Predict.** We output the confidence scores of each class in the entire RWC. 
  - **Evaluate.** TinyUStaging use metrics including per-class metrics and overall metrics (*accuracy, precision, recall, F1-Score, Cohen’s kappa*). 

#### Model Architecture

##### Overall 

![](https://s2.loli.net/2022/09/21/KXW5T138QnYMOaB.png)

###### CSJA block

<img src="https://s2.loli.net/2022/09/21/KGH7fSiJPvr5YeU.png" style="zoom: 50%;" />

###### SE block

<img src="https://s2.loli.net/2022/09/21/PjIeqL2WwsOGo39.png" alt="image-20220921114210287" style="zoom: 30%;" />

#### Results

##### Subject-wise

- See `supplementary_materials\paper_plot`
- *e.g.* Case **tpf435cf71_2574_49b2_bad0_5feceaa69d23** in **DCSM**
  - See `supplementary_materials\paper_plot\pro44\test_data\dcsm\plots`
  - <img src="https://s2.loli.net/2022/09/21/RMmwQOv5P9WH1Uq.png" alt="image-20220921160250353" style="zoom: 50%;" />
  - <img src="https://s2.loli.net/2022/09/21/WSfdznRmpFaQNJY.png" alt="image-20220921160213160" style="zoom: 33%;" />

- *e.g.* Case **SC4191E0** in **Sleep-EDF**
  - <img src="https://s2.loli.net/2022/09/21/j2bSOfcekYM8uG1.png" alt="image-20220921114512898" style="zoom: 50%;" />
  - <img src="https://s2.loli.net/2022/09/21/oTEmFOuGrpwxCfc.png" alt="image-20220921114529993" style="zoom: 33%;" />

##### Dataset-wise

- This will be made public after the paper is accepted. 

##### All Test Sets

- Results with seven **highly heterogeneous**

  - <img src="https://s2.loli.net/2022/09/21/H7g5kEuTrsFqaLw.png" alt="image-20220921114922524" style="zoom: 33%;" />

  - For more visualization results, see our paper and project folders `supplementary_materials`

