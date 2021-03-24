from gladier import GladierBaseTool



__all__ = ['EigenCorr', 'ApplyQmap']

from .corr import *
from .apply_qmap import * 

class EigenCorr(GladierBaseTool):

    flow_definition = []

    input = eigen_corr_data

    funcx_functions = [
        eigen_corr
    ]

class ApplyQmap(GladierBaseTool):
    
    flow_definition = []

    input = apply_qmap_data

    funcx_functions = [
        apply_qmap
    ]

