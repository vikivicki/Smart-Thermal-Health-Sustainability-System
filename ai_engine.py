def get_ai_recommendation( q, lmtd, U, effectiveness, fouling):

    reasons = []
    recommendation = []
    confidence = 0



    # Heat Transfer
    if q < 100:
        reasons.append("• Heat transfer rate is lower than expected.")
        recommendation.append("Increase flow rate or inspect fouling.")
        confidence += 15

    # U Value
    if U < 300:
        reasons.append("• Overall Heat Transfer Coefficient (U) is low.")
        recommendation.append("Heat transfer surface may have fouling or scaling.")
        confidence += 35

    # LMTD
    if lmtd < 15:
        reasons.append("• LMTD is very low.")
        recommendation.append("Temperature driving force is insufficient.")
        confidence += 20

    # Effectiveness
    if effectiveness < 0.70:
        reasons.append("• Heat exchanger effectiveness is poor.")
        recommendation.append("Inspect exchanger performance.")
        confidence += 20

    # Fouling
    if fouling > 0.0005:
        reasons.append("• Fouling factor is high.")
        recommendation.append("Cleaning is recommended.")
        confidence += 25

 

    if confidence > 100:
        confidence = 100

    # Final Diagnosis
    if confidence < 30:
        diagnosis = "🟢 Heat Exchanger Healthy"

    elif confidence < 60:
        diagnosis = "🟡 Moderate Fouling"

    else:
        diagnosis = "🔴 Severe Fouling"

    return {
        
        "diagnosis": diagnosis,
        "confidence": confidence,
        "reasons": reasons,
        "recommendation": recommendation,
        
    }



