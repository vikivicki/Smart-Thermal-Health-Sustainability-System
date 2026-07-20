import math

# Heat Transfer (kW)
def calculate_heat_transfer(flow_hot, cp_hot, hot_in, hot_out,flow_cold, cp_cold, cold_in, cold_out):
    q_hot  = flow_hot * cp_hot * (hot_in - hot_out)
    q_cold = flow_cold* cp_cold * (cold_in - cold_out)
    q = (q_hot+q_cold)/2
    return q 



# LMTD
def calculate_lmtd(flow_type, hot_in, hot_out, cold_in, cold_out):

    if flow_type == "Counter Flow":
        delta_t1 = hot_in - cold_out
        delta_t2 = hot_out - cold_in

    elif flow_type == "Parallel Flow":
        delta_t1 = hot_in - cold_in
        delta_t2 = hot_out - cold_out

    else:  
        delta_t1 = hot_in - cold_out
        delta_t2 = hot_out - cold_in

    if delta_t1 <= 0 or delta_t2 <= 0:
        return 0

    if abs(delta_t1 - delta_t2) < 0.00001:
        return delta_t1

    return (delta_t1-delta_t2)/math.log(delta_t1/delta_t2)


# Overall Heat Transfer Coefficient
def calculate_U(q, area, lmtd):

    if area == 0 or lmtd == 0:
        return 0

    q_watt = q * 1000

    return q_watt/(area*lmtd)


# Heat Exchanger Effectiveness
def calculate_effectiveness(flow_hot,
                            cp_hot,
                            flow_cold,
                            cp_cold,
                            hot_in,
                            cold_in,
                            q):

    C_hot = flow_hot * cp_hot
    C_cold = flow_cold * cp_cold

    C_min = min(C_hot, C_cold)

    if C_min == 0:
        return 0

    q_max = C_min * (hot_in-cold_in)

    if q_max == 0:
        return 0

    return q/q_max

def calculate_fouling_factor(U_clean, U_actual):

    if U_actual == 0:
        return 0

    Rf = (1 / U_actual) - (1 / U_clean)

    return Rf

def fouling_status(Rf):

    if Rf < 0.0002:
        return "Excellent"

    elif Rf < 0.0005:
        return "Good"

    elif Rf < 0.001:
        return "Moderate"

    else:
        return "Heavy Fouling"
    
def health_score(effectiveness,U):

    score=100

    if effectiveness<0.7:
        score-=20

    if U<300:
        score-=20

    if U<200:
        score-=20

    return max(score,0)


# ==========================================
# Sustainability Calculations
# ==========================================

def calculate_energy_loss(U_clean, U_actual, q):
    """
    Estimate energy loss due to fouling (kW)
    """
    if U_clean <= 0:
        return 0

    efficiency_ratio = min(U_actual / U_clean, 1)

    energy_loss = q * (1 - efficiency_ratio)

    return max(0, energy_loss)


def calculate_co2_savings(energy_loss):
    """
    Estimate CO2 reduction if fouling is removed.
    Assumption:
    0.82 kg CO2 emitted per kWh saved.
    """
    return energy_loss * 24 * 0.82


def sustainability_score(effectiveness, fouling, U_actual, U_clean):

    score = 100

    if effectiveness < 0.80:
        score -= 20

    if fouling > 0.0005:
        score -= 30

    if U_actual < 0.80 * U_clean:
        score -= 25

    return max(0, score)
