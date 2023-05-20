# -*- coding: utf-8 -*-


import math
import helics as h
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

elec_price = np.array([.088, .087, .088, .088, .089, .092, .114, .127, .133, .123, .119, .104, .099, .088, .092, .096, .105, .125, .129, .127, .112, .102, .101, .092])

def add_rule(rule_para):
    if rule_para == 0:
        return 'poor'
    else:
        if rule_para == 1:
            return 'average'
        else:
            return 'good'

def cal_energy(array_energy):
    sum_energy = 0
    temp_arr = np.random.randint(1, 10, 24)
    temp_arr[-1] = 0
    for i in range(24):
        temp_arr[i] = array_energy[2 * i + 1]
        real_arr = temp_arr[i] - temp_arr[i-1]
        sum_energy += real_arr * elec_price[i]
    return sum_energy

def fed_init():
    
    fuz_power = ctrl.Antecedent(np.arange(-1000, 7000, 50), 'fuz_power')
    fuz_soc = ctrl.Antecedent(np.arange(0, 1.1, 0.1), 'fuz_soc')
    fuz_price = ctrl.Antecedent(np.arange(0, 0.8, 0.01), 'fuz_price')
    fuz_batt = ctrl.Consequent(np.arange(-3000, 3000, 50), 'fuz_batt')

    fuz_power.automf(3)
    fuz_soc.automf(3)
    fuz_price.automf(3)
    fuz_batt.automf(3)
    
    para0 = np.load('para0', allow_pickle=True)
    
    rule0 = ctrl.Rule(fuz_power['poor'] & fuz_soc['poor'] & fuz_price['poor'], fuz_batt[add_rule(para0[0])])
    rule1 = ctrl.Rule(fuz_power['poor'] & fuz_soc['poor'] & fuz_price['average'], fuz_batt[add_rule(para0[1])])
    rule2 = ctrl.Rule(fuz_power['poor'] & fuz_soc['poor'] & fuz_price['good'], fuz_batt[add_rule(para0[2])])
    rule3= ctrl.Rule(fuz_power['poor'] & fuz_soc['average'] & fuz_price['poor'], fuz_batt[add_rule(para0[3])])
    rule4= ctrl.Rule(fuz_power['poor'] & fuz_soc['average'] & fuz_price['average'], fuz_batt[add_rule(para0[4])])
    rule5 = ctrl.Rule(fuz_power['poor'] & fuz_soc['average'] & fuz_price['good'], fuz_batt[add_rule(para0[5])])
    rule6 = ctrl.Rule(fuz_power['poor'] & fuz_soc['good'] & fuz_price['poor'], fuz_batt[add_rule(para0[6])])
    rule7 = ctrl.Rule(fuz_power['poor'] & fuz_soc['good'] & fuz_price['average'], fuz_batt[add_rule(para0[7])])
    rule8= ctrl.Rule(fuz_power['poor'] & fuz_soc['good'] & fuz_price['good'], fuz_batt[add_rule(para0[8])])
    
    rule9 = ctrl.Rule(fuz_power['average'] & fuz_soc['poor'] & fuz_price['poor'], fuz_batt[add_rule(para0[9])])
    rule10 = ctrl.Rule(fuz_power['average'] & fuz_soc['poor'] & fuz_price['average'], fuz_batt[add_rule(para0[10])])
    rule11 = ctrl.Rule(fuz_power['average'] & fuz_soc['poor'] & fuz_price['good'], fuz_batt[add_rule(para0[11])])
    rule12 = ctrl.Rule(fuz_power['average'] & fuz_soc['average'] & fuz_price['poor'], fuz_batt[add_rule(para0[12])])
    rule13 = ctrl.Rule(fuz_power['average'] & fuz_soc['average'] & fuz_price['average'], fuz_batt[add_rule(para0[13])])
    rule14 = ctrl.Rule(fuz_power['average'] & fuz_soc['average'] & fuz_price['good'], fuz_batt[add_rule(para0[14])])
    rule15 = ctrl.Rule(fuz_power['average'] & fuz_soc['good'] & fuz_price['poor'], fuz_batt[add_rule(para0[15])])
    rule16 = ctrl.Rule(fuz_power['average'] & fuz_soc['good'] & fuz_price['average'], fuz_batt[add_rule(para0[16])])
    rule17 = ctrl.Rule(fuz_power['average'] & fuz_soc['good'] & fuz_price['good'], fuz_batt[add_rule(para0[17])])
    
    rule18 = ctrl.Rule(fuz_power['good'] & fuz_soc['poor'] & fuz_price['poor'], fuz_batt[add_rule(para0[18])])
    rule19 = ctrl.Rule(fuz_power['good'] & fuz_soc['poor'] & fuz_price['average'], fuz_batt[add_rule(para0[19])])
    rule20 = ctrl.Rule(fuz_power['good'] & fuz_soc['poor'] & fuz_price['good'], fuz_batt[add_rule(para0[20])])
    rule21 = ctrl.Rule(fuz_power['good'] & fuz_soc['average'] & fuz_price['poor'], fuz_batt[add_rule(para0[21])])
    rule22 = ctrl.Rule(fuz_power['good'] & fuz_soc['average'] & fuz_price['average'], fuz_batt[add_rule(para0[22])])
    rule23 = ctrl.Rule(fuz_power['good'] & fuz_soc['average'] & fuz_price['good'], fuz_batt[add_rule(para0[23])])
    rule24 = ctrl.Rule(fuz_power['good'] & fuz_soc['good'] & fuz_price['poor'], fuz_batt[add_rule(para0[24])])
    rule25 = ctrl.Rule(fuz_power['good'] & fuz_soc['good'] & fuz_price['average'], fuz_batt[add_rule(para0[25])])
    rule26 = ctrl.Rule(fuz_power['good'] & fuz_soc['good'] & fuz_price['good'], fuz_batt[add_rule(para0[26])])
    
    batt_ctrl = ctrl.ControlSystem([rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10, rule11, rule12, rule13, rule14, rule15, rule16, rule17, rule18, rule19, rule20, rule21, rule22, rule23, rule24, rule25, rule26])
    batt_sim = ctrl.ControlSystemSimulation(batt_ctrl)



    fed = h.helicsCreateValueFederateFromConfig("control_0.json")
    pub = h.helicsFederateGetPublicationByIndex(fed, 0)
    pub_price = h.helicsFederateGetPublicationByIndex(fed, 1)
    sub_power = h.helicsFederateGetInputByIndex(fed, 0)
    sub_soc = h.helicsFederateGetInputByIndex(fed, 1)
    sub_energy = h.helicsFederateGetInputByIndex(fed, 2)
    
    hours = 24
    total_interval = int(60 * 60 * hours)
    update_interval = int(h.helicsFederateGetTimeProperty(fed, h.HELICS_PROPERTY_TIME_PERIOD))
    grantedtime = 0
    rec_energy = np.array([])

    h.helicsFederateEnterExecutingMode(fed)
    
    while grantedtime < total_interval:
        requested_time = grantedtime + update_interval
        grantedtime = h.helicsFederateRequestTime(fed, requested_time)
        power = h.helicsInputGetDouble(sub_power)
        soc = h.helicsInputGetDouble(sub_soc)
        energy = h.helicsInputGetDouble(sub_energy)
        rec_energy = np.append(rec_energy, energy)

        sim_time = math.ceil(grantedtime/3600) - 1
        batt_sim.input['fuz_power'] = power
        batt_sim.input['fuz_soc'] = soc
        batt_sim.input['fuz_price'] = elec_price[sim_time]
        batt_sim.compute()
        batt_out = batt_sim.output['fuz_batt']
        h.helicsPublicationPublishDouble(pub, batt_out)


        print('batt_out at %d is %f' %(grantedtime, batt_out))
        print('power at %d is %f' %(grantedtime, power))
        print('soc at %d is %f' %(grantedtime, soc))
        print('energy at %d is %f' %(grantedtime, energy))
        print('rec_energy at %d is %s' %(grantedtime, rec_energy))
        print('sim_time at %d is %f' %(grantedtime, sim_time))
    total_energy = cal_energy(rec_energy) / 1000.0
    print("the daily price is %f EUR" % total_energy)
    h.helicsPublicationPublishDouble(pub_price, total_energy)

    h.helicsFederateFinalize(fed)
    h.helicsFederateFree(fed)
    h.helicsCloseLibrary()
    
def main():
    fed_init()

if __name__ == "__main__":
    main()  
    
    
    
    
	
    
    

