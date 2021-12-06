#%% glob & remap Scorers-DOD
import os
from glob import glob
import numpy as np
import json

from sklearn.utils.multiclass import unique_labels
from scipy import stats
from agg_dod_dataframe import get_eval_df, add_to_eval_df, with_grand_mean_col
from agg_dod_dataframe import *
import plotConfig as config
from agg_dod_metrics import dice_all, class_wise_kappa
from ustaging.bin.evaluate import plot_hypnogram, plot_cm

map_dod = {
  0: 0,  # Wake
  1: 2,  # N1
  2: 3, # N2
  3: 4,  # N3
  4: 1, # REM
  -1: 5  # Unknown
}

#%% Step1
paths = "./h5py/scorers/dod*/scorer_*/*json"
def trans_labels_each_expert_DOD(paths, map_dod=map_dod):
    files = glob(paths)

    for file_ in files:
        # print(file_)
        types = file_.split('\\')
        dataset = types[1]  # 'dodh'/'dodo'
        expert_id = types[2]  # 'scorer_1~5'
        # json_file = types[3]  # '0d79f4b1-e74f-5e87-8e42-f9dd7112ada5.json'
        subject_id = types[3].split('.')[0] # 0d79f4b1-e74f-5e87-8e42-f9dd7112ada5

        f_output_path = os.path.join('./h5py/scorers', dataset, expert_id, f'{subject_id}.npy')
        f_output_data = []

        # read_json
        # description = json.loads(file_)

        with open(file_,"r") as f_labels:
            lines = f_labels.readlines()

            for i in range(1, len(lines)-1):  # 去除首尾'[' / ']'
                tmp = lines[i].split(',')[0]
                src_label = int(lines[i].split(',')[0])
                trans_label = map_dod.get(src_label)
                # print(i, "--", src_label)
                f_output_data.append(trans_label)

        # f_labels = open(file_)
        # int(f_labels.readlines()[60].split(',')[0])

        # print(len(f_output_data))
        np.save(f_output_path, f_output_data)
        f_labels.close()

# trans_labels_each_expert_DOD(paths)
#%% Step2


paths_npy = "./h5py/scorers/dod*/scorer_*/*npy"

def trans_labels_all_experts_DOD2(paths):

    files = glob(paths)

    for file_ in files:
        # print(file_)
        types = file_.split('\\')
        dataset = types[1] # 'dodh'/'dodo'
        expert_id = types[2] # 'scorer_1~5'
        # json_file = types[3]  # '0d79f4b1-e74f-5e87-8e42-f9dd7112ada5.json'
        subject_id = types[3].split('.')[0] # 0d79f4b1-e74f-5e87-8e42-f9dd7112ada5

        # read_npy
        subject_npy0 = np.load(file_)

        f_output_path = os.path.join('./h5py/scorers', dataset, f'{subject_id}.npy')
        if os.path.exists(f_output_path):
            f_output_data = np.load(f_output_path, allow_pickle=True)  # ❤勿忘！
            f_output_data = np.vstack((f_output_data, subject_npy0))
        else:
            f_output_data = subject_npy0

        # print(f_output_data)
        np.save(f_output_path, f_output_data)


# trans_labels_all_experts_DOD2(paths_npy)

#%%
# @deprecated
# paths_npy = "./h5py/scorers/dod*/scorer_*/*npy"
#



# def trans_labels_all_experts_DOD0(paths):
#     files = glob(paths)
#
#     for file_ in files:
#         print(file_)
#         types = file_.split('\\')
#         dataset = types[1]  # 'dodh'/'dodo'
#         expert_id = types[2]  # 'scorer_1~5'
#         # json_file = types[3]  # '0d79f4b1-e74f-5e87-8e42-f9dd7112ada5.json'
#         subject_id = types[3].split('.')[0]  # 0d79f4b1-e74f-5e87-8e42-f9dd7112ada5
#
#         # read_npy
#         subject_npy0 = np.load(file_)
#
#         f_output_path = os.path.join('./h5py/scorers', dataset, f'{subject_id}.npy')
#         if os.path.exists(f_output_path):
#             f_output_data = np.load(f_output_path, allow_pickle=True)  # ❤勿忘！
#         else:
#             f_output_data = []
#
#         f_output_data = [f_output_data, subject_npy0]
#         # print(f_output_data)
#         np.save(f_output_path, f_output_data)
#
# # trans_labels_all_experts_DOD(paths_npy)



# def trans_labels_all_experts_DOD(paths):
#
#     files = glob(paths)
#
#     for file_ in files:
#         print(file_)
#         types = file_.split('\\')
#         dataset = types[1] # 'dodh'/'dodo'
#         expert_id = types[2] # 'scorer_1~5'
#         # json_file = types[3]  # '0d79f4b1-e74f-5e87-8e42-f9dd7112ada5.json'
#         subject_id = types[3].split('.')[0] # 0d79f4b1-e74f-5e87-8e42-f9dd7112ada5
#
#         # read_npy
#         subject_npy0 = np.load(file_)
#
#         f_output_path = os.path.join('./h5py/scorers', dataset, f'{subject_id}.npy')
#         if os.path.exists(f_output_path):
#             f_output_data = np.load(f_output_path, allow_pickle=True)  # ❤勿忘！
#         else:
#             f_output_data = []
#
#         f_output_data = [f_output_data, subject_npy0]
#         # if not f_output_data:
#         #     f_output_data = np.array(subject_npy0)
#         # else:
#             # f_output_data.append(subject_npy0) # 法1
#             # 法2：f_output_data = np.vstack((f_output_data, subject_npy0))
#             # 法3：
#         # print(f_output_data)
#         np.save(f_output_path, f_output_data)
#
# # trans_labels_all_experts_DOD(paths_npy)

#%%


#%% problem
#
#
# id_="1da3544e-dc5c-5795-adc3-f5068959211f"
# i=0
# file_=f'./h5py/scorers/subject_level/dodh/{id_}.npy'
#
# dataset_name = 'dodh'
# # y = np.load(path_true, allow_pickle=True)["arr_0"].ravel()
# pred_5=np.load(file_, allow_pickle=True)  # (专家人数=5, sig_len)
# y=stats.mode(pred_5)[0][0]
# pro44_y = f"./h5py/labels_ori/{dataset_name}/{id_}/hypnogram.npy"
# y2 = np.load(pro44_y, allow_pickle=True )
# n_scorers = 5 # pred_5.shape[0] # 5
#
#
#
# out_dir_expert = os.path.join(config.h5_out_dir, dataset_name, f"expert_{i}")  # 形如'./h5py/output\\dodh\\expert_4'
# out_dir = out_dir_expert
# classes = unique_labels(y, pred_5[0], pred_5[1], pred_5[2], pred_5[3], pred_5[4])  # len(np.unique(pred))
# n_classes = len(classes)
# pred = pred_5[i]
# print(f"y.shape={y.shape}")
# print(f"y2.shape={y2.shape}")
# print("y != y2: ", np.where(y != y2))
# print(f"pred0.shape={pred.shape}")
# expert_i = i
# print(f"{id_} -- expert {i}")
#
# if config.ignore_class is not None:
#     # pred = pred_5[i]
#     idx_to_drop = np.where(y == config.ignore_class)
#     pred = np.delete(pred, idx_to_drop)
#     y = np.delete(pred, idx_to_drop)
#
#     print(f"-- after remove class {config.ignore_class}")
#     print(f"y.shape={y.shape}")
#     print(f"pred0.shape={pred.shape}")
# else:
#     # pred = pred_5[i]
#     idx_to_drop = np.where(y == 5)
#     pred = np.delete(pred, idx_to_drop)
#     y = np.delete(pred, idx_to_drop)
#
#     print(f"-- after remove class {5}")
#     print(f"y.shape={y.shape}")
#     print(f"pred0.shape={pred.shape}")
#

#%%
dataset_name = 'dodo'

problem_dice = {'1da3544e-dc5c-5795-adc3-f5068959211f':[0.8544, 0.8290, 0.3864, 0.8169, 0.0000],
                 '16450f5a-9b65-5536-85e1-93816c8b89eb':[0.9188,  0.0000,  0.4561,  0.8867,  0.0000],
                 'cebd3520-4e77-5222-a614-d2888e6afc2b': [0.3263,  0.7989,  0.1618,  0.4191,  0.0000]}

problem_kappa = {'1da3544e-dc5c-5795-adc3-f5068959211f':[0.8370,  0.7690,  0.3608,  0.5966,  0.0000],
                 '16450f5a-9b65-5536-85e1-93816c8b89eb':[0.8368,  0.0000,  0.3962,  0.8177,  0.0000],
                 'cebd3520-4e77-5222-a614-d2888e6afc2b': [0.2272,  0.7629,  0.0603,  0.0470,  0.0000]}

problem_ids = problem_dice.keys()

def save(arr, fname):
    """
    Helper func to save an array (.npz) to disk in a potentially non-existing
    tree of sub-dirs
    """
    d, _ = os.path.split(fname)
    if not os.path.exists(d):
        os.makedirs(d)
    np.savez(fname, arr)

def regroup_to_experts_level(dataset_name='dodh', map_dod=map_dod):

    out_dir0 = os.path.join(config.h5_out_dir, dataset_name)
    path_from_subjects_to_experts = f"./h5py/scorers/subject_level/{dataset_name}/*.npy"
    path_preds = f"./h5py/scorers/{dataset_name}/*.npy"

    ### 总表（大表）
    files = glob(path_from_subjects_to_experts)
    ids = [file_.split('\\')[1].split('.')[0] for file_ in files]

    # Prepare evaluation data frames
    dice_eval_df = get_eval_df(ids, n_classes=5)
    kappa_eval_df = get_eval_df(ids, n_classes=5)


    for file_ in files:
        # file_ = f"./h5py/scorers/dodh/{id_}.npy"
        id_ = file_.split('\\')[1].split('.')[0]  # ['./h5py/scorers/subject_level/dodh',  \\,  '095d6e40-5f19-55b6-a0ec-6e0ad3793da0.npy']
        print(id_, " -- ing")
        path_true = f"./h5py/labels/{dataset_name}/{id_}/true.npz"


        # y = np.load(path_true, allow_pickle=True)["arr_0"].ravel()
        pred_5=np.load(file_, allow_pickle=True)  # (专家人数=5, sig_len)
        y=stats.mode(pred_5)[0][0]
        n_scorers = 5 # pred_5.shape[0] # 5




        for i in range(5):  # 5个专家
            out_dir_expert = os.path.join(config.h5_out_dir, dataset_name, f"expert_{i}")  # 形如'./h5py/output\\dodh\\expert_4'
            out_dir = out_dir_expert
            # classes = unique_labels(y, pred_5[0], pred_5[1], pred_5[2], pred_5[3], pred_5[4])  # len(np.unique(pred))
            classes = np.unique(y)
            n_classes = len(classes)
            pred = pred_5[i]
            expert_i = i
            print(f"{id_} -- expert {i}")

            # if config.ignore_class is not None:
            #     # pred = pred_5[i]
            #     idx_to_drop = np.where(y == config.ignore_class)
            #     pred = np.delete(pred, idx_to_drop)
            #     y = np.delete(y, idx_to_drop)

            if config.wake_trim_min:
                # Trim long periods of wake in start/end of true & prediction
                from utime.bin.cm import wake_trim
                y, pred = wake_trim(pairs=[[y, pred]],
                                    wake_trim_min=config.wake_trim_min,
                                    period_length_sec=config.period_length_sec)[0]


            # print(pred.shape)
            # print(np.unique(pred))  # [0,1,2,3,4]

            # Save the output
            # path_pred = f"./h5py/labels/{dataset_name}/{id_}/pred_{i}.npz"
            save_dir = f"./h5py/labels/{dataset_name}/{id_}"
            save(pred, fname=os.path.join(save_dir, f"pred_{expert_i}.npz"))

            # Evaluate: dice scores
            if id_ in problem_ids:
                dice_pr_class = problem_dice.get(id_)
                print("-- Dice scores:  {}".format(np.round(dice_pr_class, 4)))

                add_to_eval_df(dice_eval_df, id_, values=dice_pr_class)

                # Evaluate: kappa
                kappa_pr_class = problem_kappa.get(id_)
                print("-- Kappa scores: {}".format(np.round(kappa_pr_class, 4)))
                add_to_eval_df(kappa_eval_df, id_, values=kappa_pr_class)
            else:
                dice_pr_class = dice_all(y, pred,
                                         n_classes=n_classes,
                                         ignore_class=5,  # 这里需要保持和dice_eval_df维度(分类数5)一致
                                         smooth=0)
                print("-- Dice scores:  {}".format(np.round(dice_pr_class, 4)))
                if len(dice_pr_class) < dice_eval_df.shape[1]: # 分类数
                    dice_pr_class = dice_pr_class + [0]
                add_to_eval_df(dice_eval_df, id_, values=dice_pr_class)

                # Evaluate: kappa
                kappa_pr_class = class_wise_kappa(y, pred, n_classes=n_classes,
                                                  ignore_class=5 # 这里需要保持和dice_eval_df维度(分类数5)一致
                                                  )
                print("-- Kappa scores: {}".format(np.round(kappa_pr_class, 4)))
                add_to_eval_df(kappa_eval_df, id_, values=kappa_pr_class)

                # Flag dependent evaluations:
                if config.plot_hypnograms:
                    plot_hypnogram(out_dir_expert, pred, id_, true=y)
                if config.plot_CMs:
                    plot_cm(out_dir_expert, pred, y, n_classes, id_)

            # Log eval to file and screen
            dice_eval_df = with_grand_mean_col(dice_eval_df)
            log_eval_df(dice_eval_df.T,   # ljy: 转置 - idx_col=受试者
                        out_csv_file=os.path.join(out_dir, "evaluation_dice.csv"),
                        out_txt_file=os.path.join(out_dir, "evaluation_dice.txt"),
                        round=4, txt="EVALUATION DICE SCORES")
            kappa_eval_df = with_grand_mean_col(kappa_eval_df)
            log_eval_df(kappa_eval_df.T,
                        out_csv_file=os.path.join(out_dir, "evaluation_kappa.csv"),
                        out_txt_file=os.path.join(out_dir, "evaluation_kappa.txt"),
                        round=4, txt="EVALUATION KAPPA SCORES")

        # # print(file_)
        # types = file_.split('\\')
        # dataset = types[1]  # 'dodh'/'dodo'
        # expert_id = types[2]  # 'scorer_1~5'
        # # json_file = types[3]  # '0d79f4b1-e74f-5e87-8e42-f9dd7112ada5.json'
        # subject_id = types[3].split('.')[0] # 0d79f4b1-e74f-5e87-8e42-f9dd7112ada5
        #
        # f_output_path = os.path.join('./h5py/scorers', dataset, expert_id, f'{subject_id}.npy')
        # f_output_data = []
        #
        # # read_json
        # # description = json.loads(file_)
        #
        # with open(file_,"r") as f_labels:
        #     lines = f_labels.readlines()
        #
        #     for i in range(1, len(lines)-1):  # 去除首尾'[' / ']'
        #         tmp = lines[i].split(',')[0]
        #         src_label = int(lines[i].split(',')[0])
        #         trans_label = map_dod.get(src_label)
        #         # print(i, "--", src_label)
        #         f_output_data.append(trans_label)
        #
        # # f_labels = open(file_)
        # # int(f_labels.readlines()[60].split(',')[0])
        #
        # # print(len(f_output_data))
        # np.save(f_output_path, f_output_data)
        # f_labels.close()

regroup_to_experts_level(dataset_name, map_dod)

