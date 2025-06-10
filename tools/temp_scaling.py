from pcdet.datasets.kitti.kitti_dataset import KittiDataset
from pcdet.config import cfg, cfg_from_yaml_file
from tools.eval_utils.ece import ece
import torch

import numpy as np


"""
Note that in order to use temperature scaling, the scores for all classes needs to be
outputed. This can be done by modifying the post_processing function in 
pcdet/models/detectors/detector3d_template.py.
"""

def calibrate(config_path, result_path):
    preds = np.load(result_path, allow_pickle=True)
    config = cfg_from_yaml_file(config_path, cfg)
    gts = get_kitti_gt_infos(config)

    index_to_class = ['Car', 'Pedestrian', 'Truck']

    results = []
    best, best_T = 1, None
    for _ in range(20):
        T = np.random.uniform(low=0.01, high=10)
        for i in range(len(preds)):
            score_all = preds[i]['score_all']
            label_idx, score = temp_scale(score_all, T)
            labels = [index_to_class[int(j)] for j in label_idx]

            preds[i]['score'] = np.array(score)
            preds[i]['label'] = np.array(labels)

        acc, ECE = ece(gts, preds, iou_thres=0.6)
        results.append((T, ECE))
        if ECE < best:
            best, best_T = ECE, T

    print('(Temperature, ECE) pairs:')
    print(results)
    print('Best T is {}, corresponding ECE is {}'.format(best_T, best))

def temp_scale(raw_scores, T, act_func='sigmoid'):
    raw_scores = torch.Tensor(raw_scores)
    if act_func == 'softmax':
        softmax = torch.softmax(raw_scores / T, dim=-1)
        score, label_idx = torch.max(softmax, dim=-1)
    elif act_func == 'sigmoid':
        sigmoid = torch.sigmoid(raw_scores / T)
        score, label_idx = torch.max(sigmoid, dim=-1)
    else:
        raise NameError("Activation function should be 'sigmoid' or 'softmax', you entered {}.".format(act_func))
    return label_idx.cpu().numpy(), score.cpu().numpy()


def get_kitti_gt_infos(cfg):
    dataset_cfg = cfg.DATA_CONFIG
    class_names = cfg.CLASS_NAMES
    kitti = KittiDataset(
        dataset_cfg=dataset_cfg,
        class_names=class_names,
        training=False
    )
    gt_infos = []
    for info in kitti.kitti_infos:
        box3d_lidar = np.array(info['annos']['gt_boxes_lidar'])
        labels = np.array(info['annos']['name'])

        relevant_objs = [i for i in range(len(labels)) if labels[i] in cfg.CLASS_NAMES]
        relevant_objs = np.array(relevant_objs)

        gt_info = {
            'box': box3d_lidar[relevant_objs],
            'label': info['annos']['name'][relevant_objs],
        }
        gt_infos.append(gt_info)
    return gt_infos

def main():
    config_path = "tools/cfgs/kitti_models/pv_rcnn_car.yaml"
    result_path = "output/pv_rcnn_car/default/eval/epoch_80/val/default/result.pkl"
    calibrate(config_path, result_path)

if __name__ == "__main__":
    main()
