import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt

# Generate universe variables
#   * inputs : error teta y error
#   obtener omega
def fis_opt(e_teta, error, params=[], grafica=False):
    a, b, c, d = params

    a = a if a >= 0 else 0.001
    b = b if b >= 0 else 0.001
    c = c if c >= 0 else 0.001
    d = d if d >= 0 else 0.001


    x_e_teta = np.arange(-5, 5, .1)
    x_error  = np.arange(-5, 5, .1)
    x_omega  = np.arange(-8, 8, .1)

    # Generate fuzzy membership functions trapezoidal y triangular
    e_teta_hi_neg = fuzz.trapmf(x_e_teta, [-100,-100, -a,  0])
    e_teta_lo     = fuzz.trimf(x_e_teta, [-b, 0, b])
    e_teta_hi_pos = fuzz.trapmf(x_e_teta, [ 0, a, 600, 600])

    error_hi_neg  = fuzz.trapmf(x_error,  [-600,-600,-c, 0])
    error_lo      = fuzz.trimf(x_error,  [-d, 0, d])
    error_hi_pos  = fuzz.trapmf(x_error,  [ 0, c, 600,600])

    omega_hi_neg  = fuzz.trapmf(x_omega,  [-8,-8,-2,-.5])
    omega_lo      = fuzz.trimf(x_omega,  [-1, 0, 1])
    omega_hi_pos  = fuzz.trapmf(x_omega,  [ .5, 2, 8, 8])


      # We need the activation of our fuzzy membership functions at these values.
    # This is what fuzz.interp_membership exists for!
    e_teta_level_hi_neg = fuzz.interp_membership(x_e_teta, e_teta_hi_neg, e_teta)

    e_teta_level_lo = fuzz.interp_membership(x_e_teta, e_teta_lo, e_teta)

    e_teta_level_hi_pos = fuzz.interp_membership(x_e_teta, e_teta_hi_pos, e_teta)

    error_level_hi_neg = fuzz.interp_membership(x_error, error_hi_neg, error)

    error_level_lo = fuzz.interp_membership(x_error, error_lo, error)

    error_level_hi_pos = fuzz.interp_membership(x_error, error_hi_pos, error)

    if grafica:
        # Visualize these universes and membership functions
        fig, (ax0, ax1, ax2) = plt.subplots(nrows=3, figsize=(8, 9))

        ax0.plot(x_e_teta, e_teta_hi_neg, 'b', linewidth=1.5, label='Alto negativo')

        ax0.plot(x_e_teta, e_teta_lo, 'g', linewidth=1.5, label='Bajo')

        ax0.plot(x_e_teta, e_teta_hi_pos, 'r', linewidth=1.5, label='Alto positivo')
        ax0.set_title('Error Theta')
        ax0.legend()

        ax1.plot(x_error, error_hi_neg, 'b', linewidth=1.5, label='Alto negativo')

        ax1.plot(x_error, error_lo, 'g', linewidth=1.5, label='Bajo')

        ax1.plot(x_error, error_hi_pos, 'r', linewidth=1.5, label='Alto positivo')
        ax1.set_title('Error')
        ax1.legend()

        ax2.plot(x_omega, omega_hi_neg, 'b', linewidth=1.5, label='Alto negativo')
        ax2.plot(x_omega, omega_lo, 'g', linewidth=1.5, label='Bajo')
        ax2.plot(x_omega, omega_hi_pos, 'r', linewidth=1.5, label='Alto positivo')
        ax2.set_title('Omega')
        ax2.legend()

        # Turn off top/right axes
        for ax in (ax0, ax1, ax2):
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.get_xaxis().tick_bottom()
            ax.get_yaxis().tick_left()

        plt.tight_layout()
        plt.show()

    # Now we take our rules and apply them.
    # Rule 1 si e_teta es hi_neg y error es low entonces omega es hi pos
    # The OR operator means we take the maximum of these two.
    active_rule1 = np.fmin(e_teta_level_hi_neg, error_level_lo)
    tip_activation_1 = np.fmin(active_rule1, omega_hi_pos)


    # Rule 2 si e_teta es hi_pos y error es low entonces omega es hi neg
    active_rule2 = np.fmin(e_teta_level_hi_pos, error_level_lo)
    tip_activation_2 = np.fmin(active_rule2, omega_hi_neg)

    # Rule 3 si e_teta es low y error es low entonces omega es low
    active_rule3 = np.fmin(e_teta_level_lo, error_level_lo)
    tip_activation_3 = np.fmin(active_rule3, omega_lo)

    # Rule 4 si e_teta es hi_neg y error es hi_neg entonces omega es hi pos
    active_rule4 = np.fmin(e_teta_level_hi_neg, error_level_hi_neg)
    tip_activation_4 = np.fmin(active_rule4, omega_hi_pos)

    # Rule 5 si e_teta es hi_pos y error es hi_pos entonces omega es hi neg
    active_rule5 = np.fmin(e_teta_level_hi_pos, error_level_hi_pos)
    tip_activation_5 = np.fmin(active_rule5, omega_hi_neg)

    # Rule 6 si e_teta es hi_pos y error es hi_neg entonces omega es bajo
    active_rule6 = np.fmin(e_teta_level_hi_pos, error_level_hi_neg)
    tip_activation_6 = np.fmin(active_rule6, omega_lo)

    # Rule 7 si e_teta es hi_neg y error es hi_pos entonces omega es bajo
    active_rule7 = np.fmin(e_teta_level_hi_neg, error_level_hi_pos)
    tip_activation_7 = np.fmin(active_rule7, omega_lo)

    # Rule 8 si e_teta es low y error es hi_pos entonces omega es hi neg
    active_rule8 = np.fmin(e_teta_level_lo, error_level_hi_pos)
    tip_activation_8 = np.fmin(active_rule8, omega_hi_neg)

    # Rule 9 si e_teta es low y error es hi_neg entonces omega es hi pos
    active_rule9 = np.fmin(e_teta_level_lo, error_level_hi_neg)
    tip_activation_9 = np.fmin(active_rule9, omega_hi_pos)
    #print(tip_activation_9)

    aggregated = np.fmax(tip_activation_9, np.fmax(tip_activation_8,np.fmax(tip_activation_7, np.fmax(tip_activation_6, np.fmax(tip_activation_5, np.fmax(tip_activation_4, np.fmax(tip_activation_1, np.fmax(tip_activation_2, tip_activation_3))))))))

    # Calculate defuzzified result
    omega = fuzz.defuzz(x_omega, aggregated, 'centroid')
    tip_activation = fuzz.interp_membership(x_omega, aggregated, omega)  # for plot

 # Visualize this
    if grafica:
        fig, ax0 = plt.subplots(figsize=(8, 3))

        ax0.fill_between(x_omega,  tip_activation_1, facecolor='b', alpha=0.7)
        ax0.plot(x_omega, omega_hi_neg, 'b', linewidth=0.5, linestyle='--', )
        ax0.fill_between(x_omega, tip_activation_2, facecolor='g', alpha=0.7)
        ax0.plot(x_omega, omega_lo, 'g', linewidth=0.5, linestyle='--')
        ax0.fill_between(x_omega,  tip_activation_3, facecolor='r', alpha=0.7)
        ax0.plot(x_omega, omega_hi_pos, 'r', linewidth=0.5, linestyle='--')
        ax0.set_title('Output membership activity')


    # Visualize this
    if grafica:
        fig, ax0 = plt.subplots(figsize=(8, 3))

        ax0.plot(x_omega, omega_hi_neg, 'b', linewidth=0.5, linestyle='--', )
        ax0.plot(x_omega, omega_lo, 'g', linewidth=0.5, linestyle='--')
        ax0.plot(x_omega, omega_hi_pos, 'r', linewidth=0.5, linestyle='--')
        ax0.fill_between(x_omega,  aggregated, facecolor='Orange', alpha=0.7)
        ax0.plot([omega, omega], [0, tip_activation], 'k', linewidth=1.5, alpha=0.9)
        ax0.set_title('Aggregated membership and result (line)')

        plt.tight_layout()
        plt.show()
    return omega

if __name__ == '__main__':
    omega = fis_opt(-1.0225139922075002, -1.5029882118831652,[0.5352509072211054, 0.8290705366152646, 0.4913977583475415, 0.5530603377966343],True)
    print(omega) ## debe imprimir 3.743589743589744
