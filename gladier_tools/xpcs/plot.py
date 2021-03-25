

def make_corr_plots(event):
    import os
    from XPCS.tools import xpcs_plots
    os.chdir(os.path.join(event['proc_dir'], os.path.dirname(event['hdf_file'])))
    xpcs_plots.make_plots(os.path.join(event['proc_dir'], event['hdf_file']))
    return [img for img in os.listdir('.') if img.endswith('.png')]
