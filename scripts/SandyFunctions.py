"Set of functions involving Sandy related to the uncertainty quantification workflow"

def CovarianceRetrieval(energy_grid, nuclide, mt_Number, data_library, temperature, rel_Flag):
    "" ""

    import numpy as np
    import sys
    import pandas as pd


    if type(energy_grid) != 'nd_array':
        energy_grid = np.array(energy_grid)

    ek_error = energy_grid

    #Need to set up a library to retrieve 

    errorr = sandy.get_endf6_file(data_library, 
                                "xs", 
                                nuclide_number).get_errorr(err = 0.1, 
                                                           nubar = True,
                                                           mubar = True,
                                                           chi = True,
                                                           xs = True,
                                                           relative = rel_Flag)

    
    if mt_Number in [452, 455, 456]:
        cov = errorr['errorr31'].get_cov(mts = mtNumber)
    else:
        cov = errorr['errorr33'].get_cov(mts = mtNumber)

    covariance_data = cov.data_library

    print('The shape of the retrieved covariance data is: ' + str(covariance_data.shape[0]) + ' by ' +str(convariance_data.shape[1]))

    covariance_data.to_csv('intermediate_dataframe.csv', index = False)

    df = pd.read_csv('intermediate_dataframe.csv', skiprows = 2)

    filename = 'covarianceMatrix_' + str(len(energy_grid)) + 'Groups_' + str(nuclide) + 'MT' + str(mt_Number[0]) + '.csv'

    df.to_csv(filename, index= False, header = False)

