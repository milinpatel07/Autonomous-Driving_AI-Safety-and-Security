import argparse
import pickle
from pathlib import Path

import torch
from ensemble_boxes import weighted_boxes_fusion

from pcdet.config import cfg, cfg_from_yaml_file
from pcdet.datasets import build_dataloader
from pcdet.models import build_network
from tools.eval_utils import eval_utils
from pcdet.utils import common_utils


def parse_args():
    parser = argparse.ArgumentParser(description="Ensemble several checkpoints")
    parser.add_argument('--cfg_file', type=str, required=True, help='config file')
    parser.add_argument('--ckpts', type=str, nargs='+', required=True, help='list of checkpoints')
    parser.add_argument('--batch_size', type=int, default=1)
    parser.add_argument('--workers', type=int, default=4)
    parser.add_argument('--output_dir', type=str, default='ensemble_output')
    return parser.parse_args()


def run_inference(cfg, ckpt, test_loader, result_dir):
    model = build_network(model_cfg=cfg.MODEL, num_class=len(cfg.CLASS_NAMES), dataset=test_loader.dataset)
    model.load_params_from_file(ckpt, to_cpu=False, logger=None)
    model.cuda()
    model.eval()
    eval_utils.eval_one_epoch(cfg, model, test_loader, 0, common_utils.create_logger(None),
                              dist_test=False, result_dir=result_dir, save_to_file=False)
    with open(result_dir / 'result.pkl', 'rb') as f:
        preds = pickle.load(f)
    return preds


def fuse_samples(sample_preds):
    fused = []
    num_samples = len(sample_preds[0])
    for idx in range(num_samples):
        boxes = []
        scores = []
        labels = []
        for pred in sample_preds:
            boxes.append(pred[idx]['bbox'])
            scores.append(pred[idx]['score'])
            labels.append([1]*len(pred[idx]['score']))
        if boxes and len(boxes[0])>0:
            fused_boxes, fused_scores, fused_labels = weighted_boxes_fusion(boxes, scores, labels, iou_thr=0.55)
            fused_pred = sample_preds[0][idx].copy()
            fused_pred['bbox'] = fused_boxes
            fused_pred['score'] = fused_scores
            fused_pred['name'] = ['Car']*len(fused_scores)
            fused.append(fused_pred)
        else:
            fused.append(sample_preds[0][idx])
    return fused


def main():
    args = parse_args()
    cfg_from_yaml_file(args.cfg_file, cfg)
    logger = common_utils.create_logger('')

    test_set, test_loader, _ = build_dataloader(dataset_cfg=cfg.DATA_CONFIG,
                                                class_names=cfg.CLASS_NAMES,
                                                batch_size=args.batch_size,
                                                dist=False, workers=args.workers,
                                                logger=logger, training=False)

    all_preds = []
    output_root = Path(args.output_dir)
    for idx, ckpt in enumerate(args.ckpts):
        result_dir = output_root / f'model_{idx}'
        result_dir.mkdir(parents=True, exist_ok=True)
        preds = run_inference(cfg, ckpt, test_loader, result_dir)
        all_preds.append(preds)

    fused_preds = fuse_samples(all_preds)
    with open(output_root / 'ensemble_result.pkl', 'wb') as f:
        pickle.dump(fused_preds, f)
    print(f'Saved fused predictions to {output_root / "ensemble_result.pkl"}')


if __name__ == '__main__':
    main()
