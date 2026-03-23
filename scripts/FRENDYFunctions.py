"Set of functions related to the workflow that make use of FRENDY"

def GenerateUnperturbedNeutronACEFile(frendy_Path, endf_Path, temperature, upgrade_Flag, energy_Grid):
    """ 

    Generates unperturbed neutron cross section ACE files for use in the workflow.

    Parameters:
        frendy_Path (str): Full path to the directory created by FRENDY during the installation process
            End of path should be '.../frendy_YYYYMMDD' where 'YYYYMMDD' corresponds to the date related to the version of FRENDY installed

        endf_Path (str): Full path to the ENDF evaluation for the nuclide of interest
            End of path should be '.../n-ZZZ_Y_AAA.endf' where ZZZ represents the three-digit Z number of the nuclide, Y the alphabetical name of the nuclide's element, and AAA the mass number of the nuclide

        temperature (int): Temperature at which to generate ACE file at

        upgrade_Flag (Boolean): Flag used to determine whether the ACE file will have additional energy grid points added to increase chances of successful data perturbations

        energy_Grid (list or nd_array): Values of the energy grid used to determine perturbation bounds.
            Should be the same as those corresponding to the retrieval of covariance data
        
    Results:

    unperturbed_ace_filename (str): Path to where the unperturbed ACE file is saved

    """



        

