
def get_data(arg1, batch_path):
    '''
    Retrieve data for either battery or process from running the bat file that
    will be saved in the output, and return nothing.
    '''
    import subprocess
    import time

    batfile_path = batch_path + arg1

    subprocess.call(batfile_path)
    return None
