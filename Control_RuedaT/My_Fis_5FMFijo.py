import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt

# Generate universe variables
#   * inputs : error teta y error
#   obtener omega
def fis_opt(e_teta, error, params=[], grafica=False):
    #a, b, c, d, e, f, g, h = list(map(abs,params))
    print(params,e_teta, error)
    #factor_apertura = 1.3

    x_e_teta = np.arange(-5, 5, 0.5)
    x_error  = np.arange(-5, 5, 0.5)
    x_omega  = np.arange(-5, 5, 0.5)

# estas son las 5 funciones de membresia con parametros fijos
    # ver en variables !2

    # Generate fuzzy membership functions trapezoidal y triangular
    e_teta_hi_neg = fuzz.trapmf(x_e_teta, [-5, -5,-2, -1])
    e_teta_med_neg = fuzz.trimf(x_e_teta, [-2,-1, 0])
    e_teta_lo      = fuzz.trimf(x_e_teta, [-1, 0, 1])
    e_teta_med_pos = fuzz.trimf(x_e_teta, [0, 1, 2])
    e_teta_hi_pos = fuzz.trapmf(x_e_teta, [ 1, 2, 5, 8])

    error_hi_neg  = fuzz.trapmf(x_error, [-5,-5, -2,  -1])
    error_med_neg = fuzz.trimf(x_e_teta, [-2,-1, 0])
    error_lo      = fuzz.trimf(x_error,  [-1, 0, 1])
    error_med_pos = fuzz.trimf(x_e_teta, [0, 1, 2])
    error_hi_pos  = fuzz.trapmf(x_error, [ 1, 2, 5, 8])

    omega_hi_neg  = fuzz.trapmf(x_omega,  [-5,-5,-2,-1])
    omega_med_neg = fuzz.trimf(x_omega,   [-2, -1, -0])
    omega_lo      = fuzz.trimf(x_omega,   [-1, 0, 1])
    omega_med_pos = fuzz.trimf(x_omega,   [0, 1, 2])
    omega_hi_pos  = fuzz.trapmf(x_omega,  [ 1, 2, 5, 8])

    # We need the activation of our fuzzy membership functions at these values.
    # This is what fuzz.interp_membership exists for!
    e_teta_level_hi_neg = fuzz.interp_membership(x_e_teta, e_teta_hi_neg, e_teta)
    e_teta_level_med_neg = fuzz.interp_membership(x_e_teta, e_teta_med_neg, e_teta)
    e_teta_level_lo = fuzz.interp_membership(x_e_teta, e_teta_lo, e_teta)
    e_teta_level_med_pos = fuzz.interp_membership(x_e_teta, e_teta_med_pos, e_teta)
    e_teta_level_hi_pos = fuzz.interp_membership(x_e_teta, e_teta_hi_pos, e_teta)

    error_level_hi_neg = fuzz.interp_membership(x_error, error_hi_neg, error)
    error_level_med_neg = fuzz.interp_membership(x_error, error_med_neg, error)
    error_level_lo = fuzz.interp_membership(x_error, error_lo, error)
    error_level_med_pos = fuzz.interp_membership(x_error, error_med_pos, error)
    error_level_hi_pos = fuzz.interp_membership(x_error, error_hi_pos, error)

    if grafica:
        # Visualize these universes and membership functions
        fig, (ax0, ax1, ax2) = plt.subplots(nrows=3, figsize=(8, 9))

        ax0.plot(x_e_teta, e_teta_hi_neg, 'b', linewidth=1.5, label='Alto negativo')
        ax0.plot(x_e_teta, e_teta_med_neg, 'm', linewidth=1.5, label='Medio negativo')
        ax0.plot(x_e_teta, e_teta_lo, 'g', linewidth=1.5, label='Bajo')
        ax0.plot(x_e_teta, e_teta_med_pos, 'k', linewidth=1.5, label='Medio positivo')
        ax0.plot(x_e_teta, e_teta_hi_pos, 'r', linewidth=1.5, label='Alto positivo')
        ax0.set_title('Error Theta')
        ax0.legend()

        ax1.plot(x_error, error_hi_neg, 'b', linewidth=1.5, label='Alto negativo')
        ax1.plot(x_error, error_med_neg, 'm', linewidth=1.5, label='Medio negativo')
        ax1.plot(x_error, error_lo, 'g', linewidth=1.5, label='Bajo')
        ax1.plot(x_error, error_med_pos, 'k', linewidth=1.5, label='Medio positivo')
        ax1.plot(x_error, error_hi_pos, 'r', linewidth=1.5, label='Alto positivo')
        ax1.set_title('Error')
        ax1.legend()

        ax2.plot(x_omega, omega_hi_neg, 'b', linewidth=1.5, label='Alto negativo')
        ax2.plot(x_omega, omega_med_neg, 'm', linewidth=1.5, label='Medio negativo')
        ax2.plot(x_omega, omega_lo, 'g', linewidth=1.5, label='Bajo')
        ax2.plot(x_omega, omega_med_pos, 'k', linewidth=1.5, label='Medio positivo')
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
    # fmin regresa el minimo de los dos arreglos o valores
    # fmax regresa el maximo de los dos arreglos o valores
    # The OR operator means we take the maximum of these two.
    # The AND operator means we take el minimun of these two

    # # Rule 1 si e_teta es hi_neg y error es low entonces omega es hi pos
    active_rule1 = np.fmin(e_teta_level_hi_neg, error_level_lo)
    # tip_activation_1 = np.fmin(active_rule1, omega_hi_pos)
    #
    # # Rule 2 si e_teta es hi_pos y error es low entonces omega es hi neg
    active_rule2 = np.fmin(e_teta_level_hi_pos, error_level_lo)
    # tip_activation_2 = np.fmin(active_rule2, omega_hi_neg)
    #
    # # Rule 3 si e_teta es low y error es low entonces omega es low
    active_rule3 = np.fmin(e_teta_level_lo, error_level_lo)
    # tip_activation_3 = np.fmin(active_rule3, omega_lo)
    #
    # # Rule 4 si e_teta es hi_neg y error es hi_neg entonces omega es hi pos
    active_rule4 = np.fmin(e_teta_level_hi_neg, error_level_hi_neg)
    # tip_activation_4 = np.fmin(active_rule4, omega_hi_pos)
    #
    # # Rule 5 si e_teta es hi_pos y error es hi_pos entonces omega es hi neg
    active_rule5 = np.fmin(e_teta_level_hi_pos, error_level_hi_pos)
    # tip_activation_5 = np.fmin(active_rule5, omega_hi_neg)
    #
    # # Rule 6 si e_teta es hi_pos y error es hi_neg entonces omega es bajo
    active_rule6 = np.fmin(e_teta_level_hi_pos, error_level_hi_neg)
    # tip_activation_6 = np.fmin(active_rule6, omega_lo)
    #
    # # Rule 7 si e_teta es hi_neg y error es hi_pos entonces omega es bajo
    active_rule7 = np.fmin(e_teta_level_hi_neg, error_level_hi_pos)
    # tip_activation_7 = np.fmin(active_rule7, omega_lo)
    #
    # # Rule 8 si e_teta es low y error es hi_pos entonces omega es hi_neg
    active_rule8 = np.fmin(e_teta_level_lo, error_level_hi_pos)
    # tip_activation_8 = np.fmin(active_rule8, omega_hi_neg)
    #
    # # Rule 9 si e_teta es low y error es hi_neg entonces omega es hi_pos
    active_rule9 = np.fmin(e_teta_level_lo, error_level_hi_neg)
    # tip_activation_9 = np.fmin(active_rule9, omega_hi_pos)
    #
    # # Rule 10 si e_teta es med_neg y error es med_neg entonces omega es med_neg
    active_rule10 = np.fmin(e_teta_level_med_neg, error_level_med_neg)
    # tip_activation_10 = np.fmin(active_rule10, omega_med_neg)
    #
    # # Rule 11 si e_teta es med_pos y error es med_pos entonces omega es med_neg
    active_rule11 = np.fmin(e_teta_level_med_pos, error_level_med_pos)
    # tip_activation_11 = np.fmin(active_rule11, omega_med_neg)
    #
    # # Rule 12 si e_teta es med_neg y error es med_pos entonces omega es med_neg
    active_rule12 = np.fmin(e_teta_level_med_neg, error_level_med_pos)
    # tip_activation_12 = np.fmin(active_rule12, omega_med_neg)
    #
    # # Rule 13 si e_teta es med_pos y error es med_neg entonces omega es med_pos
    active_rule13 = np.fmin(e_teta_level_med_pos, error_level_med_neg)
    # tip_activation_13 = np.fmin(active_rule13, omega_med_pos)
    #
    # # Rule 14 si e_teta es med_neg y error es hi_neg entonces omega es med_pos
    active_rule14 = np.fmin(e_teta_level_med_neg, error_level_hi_neg)
    # tip_activation_14 = np.fmin(active_rule14, omega_med_pos)
    #
    # # Rule 15 si e_teta es hi_neg y error es med_neg entonces omega es hi_pos
    active_rule15 = np.fmin(e_teta_level_hi_neg, error_level_med_neg)
    # tip_activation_15 = np.fmin(active_rule14, omega_hi_pos)
    #
    # # Rule 16 si e_teta es hi_neg y error es med_pos entonces omega es hi_neg
    active_rule16 = np.fmin(e_teta_level_hi_neg, error_level_med_pos)
    # tip_activation_16 = np.fmin(active_rule14, omega_hi_neg)
    #
    # # Rule 17 si e_teta es hi_pos y error es med_neg entonces omega es low
    active_rule17 = np.fmin(e_teta_level_hi_pos, error_level_med_neg)
    # tip_activation_17 = np.fmin(active_rule14, omega_lo)
    #
    # # Rule 18 si e_teta es hi_pos y error es med_pos entonces omega es lo
    active_rule18 = np.fmin(e_teta_level_hi_pos, error_level_med_pos)
    # tip_activation_18 = np.fmin(active_rule14, omega_lo)
    #
    # # Rule 19 si e_teta es med_neg y error es hi_pos entonces omega es med_pos
    active_rule19 = np.fmin(e_teta_level_med_neg, error_level_hi_pos)
    # tip_activation_19 = np.fmin(active_rule14, omega_med_pos)
    #
    # # Rule 20 si e_teta es med_pos y error es low entonces omega es med_neg
    active_rule20 = np.fmin(e_teta_level_med_pos, error_level_lo)
    # tip_activation_20 = np.fmin(active_rule14, omega_med_neg)
    #
    # # Rule 21 si e_teta es med_neg y error es low entonces omega es med_pos
    active_rule21 = np.fmin(e_teta_level_med_neg, error_level_lo)
    # tip_activation_21 = np.fmin(active_rule14, omega_med_pos)
    #
    # # Rule 22 si e_teta es low y error es med_neg entonces omega es med_pos
    active_rule22 = np.fmin(e_teta_level_lo, error_level_med_neg)
    # tip_activation_22 = np.fmin(active_rule14, omega_med_pos)
    #
    # # Rule 23 si e_teta es low y error es med_pos entonces omega es med_neg
    active_rule23 = np.fmin(e_teta_level_lo, error_level_med_pos)
    # tip_activation_23 = np.fmin(active_rule14, omega_med_neg)

    # # Rule 24 si e_teta es med_pos y error es hi_pos entonces omega es med_neg
    active_rule24 = np.fmin(e_teta_level_med_pos, error_level_hi_pos)
    # tip_activation_24 = np.fmin(active_rule24, omega_med_neg)

    # # Rule 25 si e_teta es med_pos y error es hi_neg entonces omega es med_pos
    active_rule25 = np.fmin(e_teta_level_med_pos, error_level_hi_neg)
    # tip_activation_25 = np.fmin(active_rule25, omega_med_neg)



    active_rule_Hi_neg = np.fmin(active_rule2, np.fmin(active_rule5, np.fmin(active_rule8, active_rule16)))
    tip_activation_Hi_neg  = np.fmax(active_rule_Hi_neg, omega_hi_neg)

    active_rule_Hi_pos = np.fmin(active_rule1, np.fmin(active_rule4, np.fmin(active_rule9,active_rule15)))
    tip_activation_Hi_pos = np.fmax(active_rule_Hi_pos, omega_hi_pos)

    active_rule_med_neg = np.fmin(active_rule10 ,np.fmin(active_rule11, np.fmin(active_rule12, np.fmin(active_rule20, np.fmin(active_rule23, active_rule24)))))
    tip_activation_med_neg = np.fmax(active_rule_med_neg, omega_med_neg)

    active_rule_med_pos =  np.fmin(active_rule13, np.fmin(active_rule14, np.fmin(active_rule19, np.fmin(active_rule21, np.fmin(active_rule22, active_rule25)))))
    tip_activation_med_pos = np.fmax(active_rule_med_pos, omega_med_pos)

    active_rule_low = np.fmin(active_rule3, np.fmin(active_rule6, np.fmin(active_rule7, np.fmin(active_rule17, active_rule18))))
    tip_activation_low = np.fmax(active_rule_low, omega_lo)

    #aggregated = np.fmax(tip_activation_23, np.fmax(tip_activation_22,np.fmax(tip_activation_21, np.fmax(tip_activation_20,np.fmax(tip_activation_19, np.fmax(tip_activation_18,np.fmax(tip_activation_17, np.fmax(tip_activation_16, np.fmax(tip_activation_15, np.fmax(tip_activation_14,np.fmax(tip_activation_13, np.fmax(tip_activation_12,np.fmax(tip_activation_11, np.fmax(tip_activation_10,np.fmax(tip_activation_9, np.fmax(tip_activation_8,np.fmax(tip_activation_7, np.fmax(tip_activation_6, np.fmax(tip_activation_5, np.fmax(tip_activation_4, np.fmax(tip_activation_1, np.fmax(tip_activation_2, tip_activation_3))))))))))))))))))))))
    aggregated = np.fmax(tip_activation_Hi_neg, np.fmax(tip_activation_Hi_pos,np.fmax(tip_activation_med_neg, np.fmax(tip_activation_med_pos, tip_activation_low))))
    # Calculate defuzzified result
    omega = fuzz.defuzz(x_omega, aggregated, 'centroid')
    #tip_activation = fuzz.interp_membership(x_omega, aggregated, omega)  # for plot

 # Visualize this
 #    if grafica:
 #        fig, ax0 = plt.subplots(figsize=(8, 3))
 #
 #        ax0.fill_between(x_omega,  tip_activation_1, facecolor='b', alpha=0.7)
 #        ax0.plot(x_omega, omega_hi_neg, 'b', linewidth=0.5, linestyle='--', )
 #        ax0.fill_between(x_omega, tip_activation_2, facecolor='g', alpha=0.7)
 #        ax0.plot(x_omega, omega_lo, 'g', linewidth=0.5, linestyle='--')
 #        ax0.fill_between(x_omega,  tip_activation_3, facecolor='r', alpha=0.7)
 #        ax0.plot(x_omega, omega_hi_pos, 'r', linewidth=0.5, linestyle='--')
 #        ax0.set_title('Output membership activity')
 #
 #
 #    # Visualize this
 #    if grafica:
 #        fig, ax0 = plt.subplots(figsize=(8, 3))
 #
 #        ax0.plot(x_omega, omega_hi_neg, 'b', linewidth=0.5, linestyle='--', )
 #        ax0.plot(x_omega, omega_lo, 'g', linewidth=0.5, linestyle='--')
 #        ax0.plot(x_omega, omega_hi_pos, 'r', linewidth=0.5, linestyle='--')
 #        ax0.fill_between(x_omega,  aggregated, facecolor='Orange', alpha=0.7)
 #        ax0.plot([omega, omega], [0, tip_activation], 'k', linewidth=1.5, alpha=0.9)
 #        ax0.set_title('Aggregated membership and result (line)')

        # plt.tight_layout()
        # plt.show()
    return omega

if __name__ == '__main__':
    # = fis_opt(-1.0225139922075002, -1.5029882118831652,[0.9054750552355649, 1.313749939916838, 1.2115608804558582, 1.0984015671585659,0.9054750552355649, 1.313749939916838, 1.2115608804558582, 1.0984015671585659],True)
    #omega = fis_opt(-1.0225139922075002, -1.5029882118831652,
                    #[.5,1,1,1,.5,1,1,1]
     #               [0.904678677722167, 0.8175345617149045, 0.13224560900960503, 0.5469457556076623, 0.5325770579589316,
      #               0.9268987320027717, 0.9800203897134122, 0.24073473149479774]
       #              , True)
    #omega= fis_opt(1.0572916680894755 ,-0.92007166,[0.19590043465383156, 0.7167493393335032, 0.9350616308752682, 0.2737485279962393, 0.9197640201658847, 0.9344545773709528, 0.2746576593220633, 0.662691565472217],True)
    #omega = fis_opt( -0.8579203417523265, -2.02587306, [0.6158061060468809, 0.4832258519402056, 0.7864552296026883, 0.5862045721640615, 0.6798355710879616, 0.386040327866486, 0.6634239215587792, 0.38294084619747026], True)
    #print(omega) ## debe imprimir -1.5385706528567843e-17
    omega = fis_opt(-1.053091629254558,4.5266952810876880,[0.7129072353481256, 0.6950511269226142, 0.4050757896004107, 0.5196998000235793, 0.59708268324291787, 0.48749702495492913, 0.3155646574417933, 0.4239541979859553] ,True)

