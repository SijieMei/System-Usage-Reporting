

def compute_aggregates(atl_path, file_name):
    '''
    Use the ATLSDK to consume the input and output the merged files to working_
    directory folder. Return None.
    '''
    import subprocess
    subprocess.call(atl_path + "\\" + file_name)

    return None
