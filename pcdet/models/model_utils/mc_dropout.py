import torch.nn as nn
import torch.nn.functional as F

class MonteCarloDropout(nn.Dropout):
    """Dropout that is active during evaluation for MC Dropout."""
    def forward(self, input):
        return F.dropout(input, self.p, training=True, inplace=self.inplace)

class MonteCarloDropout2d(nn.Dropout2d):
    """2D Dropout always active for MC Dropout."""
    def forward(self, input):
        return F.dropout2d(input, self.p, training=True, inplace=self.inplace)
