# Input data paths

data_dir = "/home/data"
covariates = f"{data_dir}/Covariates.csv"
thickness = f"{data_dir}/CorticalMeasuresENIGMA_ThickAvg.csv"
volume = f"{data_dir}/SubcorticalMeasuresENIGMA_VolAvg.csv"
output_dir = f"/home/output"
nj = -1

def log_config():
    import logging
    logging.basicConfig(filename=f"{output_dir}/log.txt",
        format='%(asctime)s %(message)s',
        level=logging.DEBUG,
        datefmt='%d-%m-%Y %H:%M:%S %Z')

def log_func(var_dict):
    new = {key:type(value) for key, value in var_dict.items()}
    return new