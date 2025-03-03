import argparse
import os
import random


def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


class ModelOptions:
    def __init__(self):
        parser = argparse.ArgumentParser(description='image-colorization')

        parser.add_argument('--seed', type=int, default=0, metavar='S', help='random seed (default: 0)')
        parser.add_argument('--task', type=str, default='colorizer',
                            help='The task to execute [colorizer, classifier, eval-gen, eval-si]')
        parser.add_argument('--experiment-name', type=str, default='experiment_001',
                            help='Experiment name (default: experiment_001)')
        parser.add_argument('--model-name', type=str, default='resnet',
                            help='Colorization model architecture (default: resnet)')
        parser.add_argument('--model-suffix', type=str, help='Colorization model name suffix')
        parser.add_argument('--model-path', type=str, default='./models', help='Path for pretrained models')
        parser.add_argument('--dataset-name', type=str, default='placeholder',
                            help='the dataset to use [placeholder, cifar10, places100, places205, places365] (default: placeholder)')
        parser.add_argument('--dataset-root-path', type=str, default='./data',
                            help='dataset root path (default: ./data)')
        parser.add_argument('--use-dataset-archive', type=str2bool, default=False,
                            help='Load dataset from TAR archive (default: False)')
        parser.add_argument('--output-root-path', type=str, default='./output',
                            help='models, stats etc. are saved here (default: ./output)')
        parser.add_argument('--max-epochs', type=int, default='5', help='max number of epoch to train for')
        parser.add_argument('--train-batch-size', type=int, default='100', help='training batch size')
        parser.add_argument('--val-batch-size', type=int, default='100', help='validation batch size')
        parser.add_argument('--batch-output-frequency', type=int, default=1,
                            help='frequency with which to output batch stats')
        parser.add_argument('--max-images', type=int, default=10,
                            help='maximum number of images from the validation set to be saved')
        parser.add_argument('--eval-root-path', type=str, default='./eval',
                            help='the root path for evaluation images')
        parser.add_argument('--eval-type', type=str, default='original',
                            help='the type of eval task to perform [original, grayscale, colorized]')

        self._parser = parser

    def parse(self):
        opt = self._parser.parse_args()

        if opt.seed == 0:
            opt.seed = random.randint(0, 2 ** 31 - 1)

        opt.dataset_path = os.path.join(opt.dataset_root_path, opt.dataset_name)
        opt.experiment_output_path = os.path.join(opt.output_root_path, opt.experiment_name)

        if opt.model_suffix is None:
            opt.full_model_name = opt.model_name
        else:
            opt.full_model_name = '{}-{}'.format(opt.model_name, opt.model_suffix)

        return opt
