#Functions adding data post-processing capabilities
#within WINDIGO.

def generate_relative_sensitivity_plot(
        energy_grid_MeV,
        sens_calculation_method,
        positive_perturbed_outputs=[],
        negative_perturbed_outputs=[],
        unperturbed_output=[],
        positive_perturbed_inputs=[],
        negative_perturbed_inputs=[],
        perturbation_coefficient=1,
        original_inputs=[],
):
    """
    Generates a relative sensitivity per unit lethargy 
    plot of the outputs with respect to incident neutron
    energy.

    Parameters
    ----------
    energy_grid_MeV: list or ndarray
       Grid defining the energy bounds used to perturb inputs
       in MeV

    sens_calculation_method: str
       Desired method used to calculate sensitivity coefficients.
       Options: Forward, Backward, Central
    
    positive_perturbed_inputs: list or ndarray, optional
       Outputs from simulations that utilized positively-perturbed 
       inputs. Required for Forward and Central sensitivity coefficient
       calculations.
       Default is blank list.
    
    


    Returns
    ---------
    str
       Path to the generated relative sensitivity per unit lethargy plot.    
    """ 