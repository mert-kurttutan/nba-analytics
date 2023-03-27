from .base_mlp import BaseMLP
from torch import nn


def get_classifier_head(in_dim, out_dim):
    return nn.Sequential(
        nn.BatchNorm1d(in_dim),
        nn.Linear(in_features=in_dim, out_features=512, bias=False),
        nn.ReLU(inplace=True),
        nn.BatchNorm1d(512),
        nn.Dropout(0.4),
        nn.Linear(in_features=512, out_features=out_dim, bias=False)
    )


def get_model(config):

    if config["model_name"] == "base_mlp":
        return BaseMLP(config)
    else:
        raise NotImplementedError
