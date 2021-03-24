eigen_corr_data = {
        'proc_dir':'',
        'imm_file':'',
        'hdf_file':'',
        'flags':'',
        'flat_file':'',
        'corr_loc':'corr',
    }
    
def eigen_corr(event):
    import os
    import subprocess
    from subprocess import PIPE

    ##minimal data inputs payload
#    data_dir = event.get('data_dir','') #location of the IMM
    imm_file = event['imm_file'] # raw data
    ##
    proc_dir = event['proc_dir'] # location of the HDF/QMAP process file / result
    hdf_file = event['hdf_file'] # name of the file to run EIGEN CORR
#    qmap_file = event.get('qmap_file', '')
    ##optional
    flags = event.get('flags', '') # flags for eigen corr
    corr_loc = event.get('corr_loc', 'corr')

    if not os.path.exists(proc_dir):
        raise NameError('proc dir does not exist')

    # if qmap_file:
    #     apply_qmap(event)

    os.chdir(proc_dir)

    cmd = f"{corr_loc} {hdf_file} -imm {imm_file} {flags}"
  
    res = subprocess.run(cmd, stdout=PIPE, stderr=PIPE,
                             shell=True, executable='/bin/bash')
    
    with open(os.path.join(proc_dir,'corr_output.log'), 'w+') as f:
                f.write(res.stdout.decode('utf-8'))

    with open(os.path.join(proc_dir,'corr_errors.log'), 'w+') as f:
                f.write(res.stderr.decode('utf-8'))
    
    return str(res.stdout)
