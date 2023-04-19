import json
import math
import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt


def calculate():
    global R
    R = float(R_entry.get())
    # Load the JSON files
    print(R)
    with open('value.json') as json_file:
        data = json.load(json_file)
    with open('ppow.json') as json_file:
        data2 = json.load(json_file)
    with open('pack.json') as json_file:
        data3 = json.load(json_file)

    # et the variables for a specific contaminant
    contaminant = contaminant_entry.get()
    delta_H = data[contaminant]['delta_H']
    K = data[contaminant]['K']
    T = float(temp_entry.get()) + 273  # temperature in Kelvin
    gas_constant = 1.987  # gas constant
    # Calculate H using the equation
    H = math.exp((-delta_H / (gas_constant * T)) + K)
    # Take the logarithm of H
    log_H = math.log(H)
    Henrry = 10 ** log_H
    P_t = 1  # total pressure in atm
    R = float(R_entry.get())
    # G/L
    G_over_L = R / (P_t * Henrry)
    # L/G
    L_over_G = 1 / G_over_L
    GMW_H2O = 18.01528
    LGMW_AIR = 28.97
    # L*/G*
    Ls_over_Gs = (GMW_H2O / LGMW_AIR) * L_over_G
    # Get the variables for a specific temperature
    temp = f"Tempreture{temp_entry.get()}"
    PG = data2[temp]['Density_gas']
    pl = data2[temp]['Density_Water']
    UL = data2[temp]['Dynamic_Viscosity']
    x = np.array([0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.15, 0.2,
                  0.25, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5])
    y = np.array(
        [0.03, 0.028, 0.0275, 0.0263, 0.0254, 0.0249, 0.0241, 0.0238, 0.0235, 0.022, 0.02, 0.018, 0.016, 0.0156,
         0.0138, 0.0128, 0.01, 0.0091, 0.0085, 0.0075, 0.007, 0.005, 0.0038, 0.0031, 0.00254, 0.0023, 0.0018, 0.00161,
         0.0015])
    # create log scale plots
    fig, ax = plt.subplots()
    ax.set_xscale('log')
    ax.set_yscale('log')
    # plot the data
    ax.plot(x, y)
    # add labels and title
    ax.set_xlabel('X Values (log scale)')
    ax.set_ylabel('Y Values (log scale)')
    ax.set_title('Eckert Curve')
    # set the x-value you want to find the corresponding y-value for
    X_axisi = Ls_over_Gs * (PG / (pl - PG)) ** 0.5
    x_target = X_axisi
    # find the index of the closest x-value
    index = np.abs(x - x_target).argmin()
    # get the corresponding y-value
    Y_axis = y[index]
    # print the result
    print(f"The corresponding y-value for x={x_target} is y={Y_axis}")
    LN = math.log10(X_axisi) * 2.302585092994046
    # Y_axis = ((-0.005*LN)+0.0086)
    # G*
    GS = (Y_axis * PG * (pl - PG) / (95 * (UL * (10 ** -3)) ** .1)) ** 0.5
    # L*
    LS = GS * Ls_over_Gs
    # Calculate area
    Q = float(Q_entry.get())
    A = (((Q / 86400) * pl) / LS)
    # Calculate diameter
    D = (A * 4 / math.pi) ** 0.5
    # Calculate NTU
    C0 = float(C0_entry.get())
    Ce = float(Ce_entry.get())
    NTU = (R / (R - 1)) * 2.302585092994046 * math.log10((1 + (C0 / Ce) * (R - 1)) / R)

    # Liquid-phase diffusion coefficient
    VB = data[contaminant]["Aatomic Volume"]
    Dl = (13.26 * 10 ** (-5)) / ((1.139 ** 1.14) * (VB) ** 0.589)

    # Gas-Phase Diffusion Coefficients
    VD = data[contaminant]["Diffusion volume"]
    DG = ((0.2025 * (T ** 1.75)) * 10 ** (-3)) / ((20.1 ** (1 / 3)) + (VD ** (1 / 3))) ** 2
    # Determine the KLa from the Onda correlation:
    # AT= data3["surface_area"]
    Dynamic = data2[temp]["Dynamic_Viscosity"]
    Tension = data2[temp]["Surface_Tension"]
    QC = -1.244
    REL = (LS / (125 * (Dynamic * (10 ** -3)))) ** 0.1

    FRL = (((LS ** 2) * 125) / ((pl ** 2) * 9.81)) ** -0.05
    WEL = (((LS ** 2)) / (pl * 125 * Tension)) ** 0.2
    AW = 125 * (1 - (2.71828 ** (QC * REL * FRL * WEL)))
    KUL = (pl / ((Dynamic * (10 ** -3)) * 9.81)) ** (1 / 3)
    KLS = 0.0051 * ((LS / (AW * (Dynamic * (10 ** -3)))) ** (2 / 3))
    print(KLS)
    KDL = ((Dynamic * (10 ** -3)) / pl / (Dl * 10 ** -4)) ** -0.5
    KL = (KLS * KDL * 1.866) / KUL
    UG = data2[temp]['Dynamic_Viscosity_gas']
    # gas-phase mass transfer coefficient:
    KDG = 5.23 * (125 * (DG * (10 ** -4)))
    KGS = (GS / (125 * (UG * (10 ** -5)))) ** (0.7)
    KUG = ((UG * (10 ** -5)) / PG / (DG * 10 ** -4)) ** (1 / 3)
    KG = (KGS * KDG * KUG) * 0.044
    # dimensionless henry’s constant:
    HD = Henrry / (0.0821 * T * 55.4)
    Kflip = (1 / KL) + (1 / (HD * KG))
    KLA = 1 / Kflip
    # Compute HTU:
    HTU = LS / (pl * KLA * AW)
    # Total tower depth:
    Total_Hight = HTU * NTU
    # Volume of tower:
    V = A * Total_Hight

    # Update result labels
    Henrry_label.config(
        text=f"Henry's constant for {contaminant} is {Henrry:.5f} atm")
    G_over_L_label.config(text=f"G/L for {contaminant} is {G_over_L:.5f}")
    L_over_G_label.config(text=f"L/G for {contaminant} is {L_over_G:.5f}")
    Ls_over_Gs_label.config(
        text=f"L*/G* for {contaminant} is {Ls_over_Gs:.5f}")
    X_axisi_label.config(text=f"X-axisi for {contaminant} is {X_axisi:.5f}")
    Y_axis_label.config(text=f"Y-axis for {contaminant} is {Y_axis:.5f}")
    GS_label.config(text=f"G* for {contaminant} is {GS:.5f}")
    LS_label.config(text=f"L* for {contaminant} is {LS:.5f}")
    A_label.config(text=f"A for {contaminant} is {A:.5f}")
    D_label.config(text=f"D for {contaminant} is {D:.5f}")
    NTU_label.config(text=f"NTU for {contaminant} is {NTU:.5f}")
    Dl_label.config(text=f"Dl for {contaminant} is {Dl:.5f}")
    DG_label.config(text=f"DG for {contaminant} is {DG:.5f}")
    REL_label.config(text=f"REL for {contaminant} is {REL:.5f}")
    FRL_label.config(text=f"FRL for {contaminant} is {FRL:.5f}")
    WEL_label.config(text=f"WEL for {contaminant} is {WEL:.5f}")
    AW_label.config(text=f"AW for {contaminant} is {AW:.5f}")

    KL_label.config(text=f"KL for {contaminant} is {KL:.5f}")
    KG_label.config(text=f"KG for {contaminant} is {KG:.5f}")
    HD_label.config(text=f"HD for {contaminant} is {HD:.5f}")
    KLA_label.config(text=f"KLA for {contaminant} is {KLA:.5f}")
    HTU_label.config(text=f"HTU for {contaminant} is {HTU:.5f}")
    Total_Hight_label.config(
        text=f"Total Hight for {contaminant} is {Total_Hight:.5f}")
    V_label.config(text=f"Volume for {contaminant} is {V:.5f}")
    ax.plot(x_target, Y_axis, 'ro', label=f'x={x_target:.3f}, y={Y_axis:.3f}')
    # save results to json file
    results = {
        "contaminant": contaminant,
        "temperature": temp,
        "R": R,
        "LS": LS,
        "GS": GS,
        "NTU": NTU,
        "HTU": HTU,
        "D": D,
        "A": A,
        "total_hight": Total_Hight,
        "Volume": V,
    }

    with open("results.json", "a") as f:
        json.dump(results, f, indent=4)
    print("Results saved to results.json")
    print(results)
    plt.show()


# Create the window
window = tk.Tk()
window.title("Calculate")
window.geometry("900x700")
window.configure(background="pink")
#window.resizable(width=False, height=False)
window.grid_columnconfigure(0, weight=1)
window.grid_columnconfigure(1, weight=1)
window.grid_columnconfigure(2, weight=1)

# Create the labels
contaminant_label = tk.Label(text="Contaminant")
contaminant_label.grid(row=0, column=0)
temp_label = tk.Label(text="Temperature (C)")
temp_label.grid(row=1, column=0)
R_label = tk.Label(text="R")
R_label.grid(row=2, column=0)
Q_label = tk.Label(text="Q (m3/day)")
Q_label.grid(row=3, column=0)
C0_label = tk.Label(text="C0 (mg/L)")
C0_label.grid(row=4, column=0)
Ce_label = tk.Label(text="Ce (mg/L)")
Ce_label.grid(row=5, column=0)

# Create the entries
contaminant_entry = tk.Entry()
contaminant_entry.grid(row=0, column=1)
temp_entry = tk.Entry()
temp_entry.grid(row=1, column=1)
R_entry = tk.Entry()
R_entry.grid(row=2, column=1)
Q_entry = tk.Entry()
Q_entry.grid(row=3, column=1)
C0_entry = tk.Entry()
C0_entry.grid(row=4, column=1)
Ce_entry = tk.Entry()
Ce_entry.grid(row=5, column=1)

# Create the buttons
calculate_button = tk.Button(text="Calculate", command=calculate)
calculate_button.grid(row=6, column=0)

# Create the result labels
Henrry_label = tk.Label(text="Henrry's constant")
Henrry_label.grid(row=7, column=0)
G_over_L_label = tk.Label(text="G/L")
G_over_L_label.grid(row=8, column=0)
L_over_G_label = tk.Label(text="L/G")
L_over_G_label.grid(row=9, column=0)
Ls_over_Gs_label = tk.Label(text="L*/G*")
Ls_over_Gs_label.grid(row=10, column=0)
X_axisi_label = tk.Label(text="X-axisi")
X_axisi_label.grid(row=11, column=0)
Y_axis_label = tk.Label(text="Y-axis")
Y_axis_label.grid(row=12, column=0)
GS_label = tk.Label(text="G* (kg/m^2.sec)")
GS_label.grid(row=13, column=0)
LS_label = tk.Label(text="L*(kg/m^2.sec)")
LS_label.grid(row=14, column=0)
A_label = tk.Label(text="Area (m2)")
A_label.grid(row=15, column=0)
D_label = tk.Label(text="Diameter (m)")
D_label.grid(row=16, column=0)
NTU_label = tk.Label(text="NTU")
NTU_label.grid(row=17, column=0)
Dl_label = tk.Label(text="Dl(cm^2/sec)")
Dl_label.grid(row=18, column=0)
DG_label = tk.Label(text="DG (Cm^2.sec")
DG_label.grid(row=19, column=0)
REL_label = tk.Label(text="REL")
REL_label.grid(row=20, column=0)
FRL_label = tk.Label(text="FRL")
FRL_label.grid(row=21, column=0)
WEL_label = tk.Label(text="WEL")
WEL_label.grid(row=22, column=0)
AW_label = tk.Label(text="AW")
AW_label.grid(row=23, column=0)
KL_label = tk.Label(text="KL (m/s)")
KL_label.grid(row=24, column=0)
KG_label = tk.Label(text="KG (m/s)")
KG_label.grid(row=25, column=0)
HD_label = tk.Label(text="dimensionless henry’s constant")
HD_label.grid(row=26, column=0)
KLA_label = tk.Label(text="KLA (s−1)")
KLA_label.grid(row=27, column=0)
HTU_label = tk.Label(text="HTU (m)")
HTU_label.grid(row=28, column=0)
Total_Hight_label = tk.Label(text="Total Hight (m) ")
Total_Hight_label.grid(row=29, column=0)
V_label = tk.Label(text="Volume (m3)")
V_label.grid(row=30, column=0)

# Start the program
window.mainloop()
plt.show()
