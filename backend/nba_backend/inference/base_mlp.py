import torch
import torch.nn as nn
import torch.nn.functional as F


def get_block(in_dim, out_dim):
    return nn.Sequential(nn.Linear(in_dim, out_dim), nn.BatchNorm1d(out_dim))


class BaseMLP(nn.Module):
    """
    Standard Baseline CNN.
    Basic unit is conv->BN->pool->activation
    """

    @staticmethod
    def get_activation(name: str):
        activation_map = {
            "relu": F.relu,
            "elu": F.elu,
            "gelu": F.gelu,
            "tanh": torch.tanh,
        }

        return activation_map[name]

    def __init__(self, config):
        """
        We define an convolutional network that predicts
        the sign from an image. The components required are:
        Args:
            params: (Params) contains n_channels
        """
        super(BaseMLP, self).__init__()
        self.n_dims = config["n_dims"]
        self.n_classes = config["n_classes"]

        self.activation = (
            F.relu
            if config["activation"] is None
            else self.get_activation(config["activation"])
        )

        self.layers = nn.ModuleList(
            [
                get_block(in_dim, out_dim)
                for in_dim, out_dim in zip(self.n_dims[:-1], self.n_dims[1:])
            ]
        )
        self.fc = nn.Linear(self.n_dims[-1], self.n_classes)
        self.dropout_rate = config["fc_pdrop"]

    def forward(self, x):
        """
        This function defines how we use the components of our
        network to operate on an input batch.
        Args:
            s: contains a batch of images, of dimension batch_size x 3 x 32 x 32 .
        Returns:
            out: dimension batch_size x class_num with the
                log prob for the image labels.
        Note: the dimensions after each step are provided
        """
        # we apply the conv layers, followed by batch normalisation, maxpool and activation x 3

        for _layer in self.layers:
            x = _layer(x)
            x = self.activation(x)

        out = self.fc(x)
        return out
