from gladier import GladierBaseTool



__all__ = ['EigenCorr', 'ApplyQmap']

from .corr import *
from .apply_qmap import * 

EigenCorr = GladierBaseTool()
EigenCorr.flow_definition = []
EigenCorr.flow_input = eigen_corr_data
EigenCorr.funcx_functions = [
        eigen_corr
    ]

ApplyQmap = GladierBaseTool()
ApplyQmap.flow_definition = []
ApplyQmap.flow_input = apply_qmap_data
ApplyQmap.funcx_functions = [
        apply_qmap
    ]

