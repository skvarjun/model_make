
# Author: Arjun S Kulathuvayal. Intellectual property. Copyright strictly restricted
import numpy as np
import matplotlib.pyplot as plt
font = {'family': 'serif',
        'weight': 'normal',
        'size': 12}
plt.rc('font', **font)
import re
plt.rcParams["figure.figsize"] = [8, 6]



def con_kcal_mol(hatree):
    return hatree*627.5095

def get_value(file_path, key_word):
    numbers = []
    with open(file_path, 'r') as file:
        for line in file:
            if key_word in line:
                part = line.split(key_word)[1]
                numbers.append(float(re.search(r"[-+]?\d*\.\d+|\d+", part).group()))
    return numbers[0]


def fetch_data(f_path):
    #Fetching values
    E_DFT = -get_value(f_path, "HF=-")
    E_ZPE = get_value(f_path, "Zero-point correction=")
    E_Tot = get_value(f_path, "Thermal correction to Energy=")
    H_Cor = get_value(f_path, "Thermal correction to Enthalpy=")
    G_Cor = get_value(f_path, "Thermal correction to Gibbs Free Energy=")

    #Executing Corrections
    Corrected_E0 = E_DFT + E_ZPE
    Corrected_E_tot = E_DFT + E_Tot
    Corrected_H = E_DFT + H_Cor #Use for enthalpy step plot
    Corrected_G = E_DFT + G_Cor #Use for Gibbs free energy step plot



    E_DFT_Plus_E_ZPE = E_DFT + E_ZPE 
    E_DFT_Plus_E_Tot = E_DFT + E_Tot
    E_DFT_Plus_H_Cor = E_DFT + H_Cor + E_ZPE
    E_DFT_Plus_G_Cor = G_Cor

    return E_DFT_Plus_H_Cor, E_DFT_Plus_G_Cor



def main():
    pfoa_H, pfoa_G = fetch_data("PFOA_GO_Freq_SMD_Water/log.out")
    ts1_H, ts1_G = fetch_data("TS1_GO_Freq/log.out")
    ts1_pdt_H, ts1_pdt_G = fetch_data("TS1_GO_product/log.out")  
    ts2_H, ts2_G = fetch_data("TS2_GO_Freq/log.out")
    ts2_pdt_H, ts2_pdt_G = fetch_data("TS2_GO_product/log.out")

    print(pfoa_H, pfoa_G)
    print(ts1_H, ts1_G)

    print(ts1_pdt_H, ts1_pdt_G)
    print(ts2_H, ts2_G)

    ts1_dH = con_kcal_mol(ts1_H - pfoa_H)
    ts1_dG = con_kcal_mol(ts1_G - pfoa_G)
    ts1_fin_dH = con_kcal_mol(ts1_pdt_H - ts1_H)
    ts1_fin_dG = con_kcal_mol(ts1_pdt_G - ts1_G)

    ts2_dH = con_kcal_mol(ts2_H - pfoa_H)
    ts2_dG = con_kcal_mol(ts2_G - pfoa_G)
    ts2_fin_dH = con_kcal_mol(ts2_pdt_H - ts2_H)
    ts2_fin_dG = con_kcal_mol(ts2_pdt_G - ts2_G)

    
    plt.plot([2, 3], [0, ts1_dH], c='r', linestyle=':')
    plt.plot([3, 4], [ts1_dH, ts1_dH], c='r', label='Chain shortening')
    plt.plot([4, 5], [ts1_dH, ts1_fin_dH], c='r', linestyle=':')
    plt.plot([5, 6], [ts1_fin_dH, ts1_fin_dH], c='r')
    #plt.text(3.25, ts1_dH+0.5,f'TS1') 
    plt.text(3.00, ts1_dH+1,f'dH = {ts1_dH:.2f}  \ndG = {ts1_dG:.2f}')
    plt.text(5.00, ts1_fin_dH+1,f'dH = {ts1_fin_dH:.2f} \ndG = {ts1_fin_dG:.2f}')

    plt.plot([2, 3], [0, ts2_dH], c='b', linestyle=':')
    plt.plot([3, 4], [ts2_dH, ts2_dH], c='b', label='H/F exchange')
    plt.plot([4, 5], [ts2_dH, ts2_fin_dH], c='b', linestyle=':')
    plt.plot([5, 6], [ts2_fin_dH, ts2_fin_dH], c='b')
    #plt.text(3.25, ts2_dH+0.5,f'TS2') 
    plt.text(3.00, -0.75,f'dH = {ts2_dH:.2f} \ndG = {ts2_dG:.2f}')
    plt.text(5.00, ts2_fin_dH+1,f'dH = {ts2_fin_dH:.2f} \ndG = {ts2_fin_dG:.2f}')

    plt.plot([1, 2], [0, 0], c='black')
    plt.text(1.25, 0.5, r'PFOA$^{.2-}$')
    plt.ylim(-30, 22.5)
    plt.xticks([])
    plt.legend(loc='best')
    plt.xlabel('Reaction path')
    plt.ylabel('Change in enthalpy (Kcal/mol)')
    plt.tight_layout()
    plt.savefig('graph.png', dpi=300)
    plt.close()

if __name__ == "__main__":
    main()
