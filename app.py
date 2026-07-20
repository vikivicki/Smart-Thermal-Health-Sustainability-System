import streamlit as st
import math
from pdf_report import generate_pdf



from calculator import (
    calculate_heat_transfer,
    calculate_lmtd,
    calculate_U,
    calculate_effectiveness,
    calculate_fouling_factor,
    fouling_status,
    health_score,
    calculate_energy_loss,
    calculate_co2_savings,
    sustainability_score
)

from ai_engine import get_ai_recommendation

st.set_page_config(
    page_title="ThermalGuardian AI",
    layout="wide"
)

st.title("🔥Smart Thermal Health & Sustainability System")
st.write("AI Powered Heat Exchanger Health Monitor for Sustainable Energy Efficiency")

# Heat Exchanger


hx_type = st.selectbox(
    "Heat Exchanger Type",
    [
        "Shell and Tube",
        "Double Pipe",
        "Plate Heat Exchanger",
        "Air Cooled"
    ]
)

flow_type = st.selectbox(
    "Flow Type",
    [
        "Counter Flow",
        "Parallel Flow",
        "Cross Flow"
    ]
)

st.header("Operating Data")

flow_hot = st.number_input(
    "Hot Flow Rate (kg/s)",
    min_value=0.0
)

flow_cold = st.number_input(
    "Cold Flow Rate (kg/s)",
    min_value=0.0
)

cp_hot = st.number_input(
    "Hot Fluid Cp (kJ/kg°C)",
    min_value=0.0
)

cp_cold = st.number_input(
    "Cold Fluid Cp (kJ/kg°C)",
    min_value=0.0
)

hot_in = st.number_input("Hot Inlet Temperature (°C)")
hot_out = st.number_input("Hot Outlet Temperature (°C)")
cold_in = st.number_input("Cold Inlet Temperature (°C)")
cold_out = st.number_input("Cold Outlet Temperature (°C)")


q_hot = 0.0
q_cold = 0.0
q = 0.0
heat_error = 0.0
lmtd=0.0
U_clean=0.0
U=0.0
effectiveness=0.0
fouling=0.0 
score=0.0
status=0.0



area = st.number_input(
    "Heat Transfer Area (m²)",
    min_value=0.0
)
q_hot  = flow_hot * cp_hot * (hot_in - hot_out)
q_cold = flow_cold* cp_cold * (cold_in - cold_out)
q = (q_hot+q_cold)/2



if st.button("Analyze"):

    # Heat Transfer
    q = calculate_heat_transfer(
        flow_hot,
        cp_hot,
        hot_in,
        hot_out,
         flow_cold,
        cp_cold,
        cold_in,
        cold_out

    )
    heat_error = calculate_heat_transfer(
        flow_hot,
        cp_hot,
        hot_in,
        hot_out,
         flow_cold,
        cp_cold,
        cold_in,
        cold_out

    )

    # LMTD
    lmtd = calculate_lmtd(
        flow_type,
        hot_in,
        hot_out,
        cold_in,
        cold_out
    )

    # U
    U = calculate_U(
        q,
        area,
        lmtd
    )

    # Effectiveness
    effectiveness = calculate_effectiveness(
        flow_hot,
        cp_hot,
        flow_cold,
        cp_cold,
        hot_in,
        cold_in,
        q
    )



    st.subheader("Results")

    
    st.success(f"Heat Transfer : {q:.2f} kW")
    st.success(f"LMTD : {lmtd:.2f} °C")
    st.success(f"Overall U : {U:.2f} W/m²°C")
    st.success(f"Effectiveness : {effectiveness:.2f}")

   

  # 5. Fouling Factor
    U_clean = 850
    fouling = calculate_fouling_factor(U_clean, U)
    st.info(fouling)

    # 6. Fouling Status
    status = fouling_status(fouling)
    st.info(status)
    score = health_score(effectiveness, U)
    st.info(score)


ai = get_ai_recommendation(
    q,
    lmtd,
    U,
    effectiveness,
    fouling
)
st.header("🤖 Explainable AI Diagnosis")

st.subheader("Overall Diagnosis")

st.success(ai["diagnosis"])

st.metric(
    "AI Confidence",
    f"{ai['confidence']}%"
)
st.subheader("Why did AI predict this?")

for reason in ai["reasons"]:
    st.write(reason)

st.subheader("Maintenance Recommendation")

for item in ai["recommendation"]:
    st.write("✔", item)
st.subheader("AI Confidence")

st.progress(ai["confidence"] / 100) 




    # ==========================
    # Dashboard
    # ==========================
st.header("📊 Performance Dashboard")

col1, col2, col3, col4 = st.columns(4)

col1.metric("🔥 Hot Heat", f"{q_hot:.2f} kW")

col2.metric("❄ Cold Heat", f"{q_cold:.2f} kW")

col3.metric("📈 Average Heat", f"{q:.2f} kW")

col4.metric("⚖ Heat Error", f"{heat_error:.2f}%")
col5, col6, col7, col8 = st.columns(4)

col5.metric("🌡 LMTD", f"{lmtd:.2f} °C")

col6.metric("🔥 U Value", f"{U:.2f} W/m²K")

col7.metric("✅ Effectiveness", f"{effectiveness:.2f}")

col8.metric("⚠ Fouling", f"{fouling:.6f}")

st.subheader("🏥 Equipment Health")

st.progress(score / 100)

st.metric("Health Score", f"{score}%")

if status == "Excellent":
        st.success(status)

elif status == "Good":
        st.info(status)

elif status == "Moderate":
        st.warning(status)

else:
        st.error(status)

    # ==========================
    # AI Recommendation
    # ==========================
ai = get_ai_recommendation(
        effectiveness,
        fouling,
        q,
        lmtd,
        U,
    
    
    )

st.success(ai["diagnosis"])

st.metric(
    "AI Confidence",
    f"{ai['confidence']}%"
)

for reason in ai["reasons"]:
    st.write(reason)

for rec in ai["recommendation"]:
    st.write(rec)



st.subheader("Why did AI predict this?")

for reason in ai["reasons"]:
        st.write("✔", reason)

st.subheader("Recommended Actions")

fouling = calculate_fouling_factor(U_clean, U)

# ============================
# Sustainability Metrics
# ============================

energy_loss = calculate_energy_loss(U_clean, U, q)

co2_saved = calculate_co2_savings(energy_loss)

green_score = sustainability_score(
    effectiveness,
    fouling,
    U,
    U_clean
)
st.header("🌱 Clean & Green Dashboard")

g1, g2, g3 = st.columns(3)

g1.metric(
    "⚡ Energy Loss",
    f"{energy_loss:.2f} kW"
)

g2.metric(
    "🌍 CO₂ Reduction",
    f"{co2_saved:.2f} kg/day"
)

g3.metric(
    "♻ Sustainability Score",
    f"{green_score}/100"
)

st.progress(green_score/100)

if green_score >= 90:
    st.success("🟢 Excellent Sustainability")

elif green_score >= 75:
    st.info("🟢 Good Sustainability")

elif green_score >= 50:
    st.warning("🟡 Moderate Sustainability")

else:
    st.error("🔴 Poor Sustainability")

st.subheader("🌍 Green Recommendation")

if green_score >= 90:
    st.success(
        "System is operating efficiently with minimal environmental impact."
    )

elif green_score >= 70:
    st.info(
        "Minor cleaning can improve efficiency and reduce energy consumption."
    )

else:
    st.warning(
        "Heavy fouling is increasing energy consumption and CO₂ emissions. Cleaning is recommended immediately."
    )



pdf_file = generate_pdf(
         q_hot,
    q_cold,
    heat_error,
    lmtd,
    U,
    effectiveness,
    fouling,
    energy_loss,
    co2_saved,
    green_score
    
    )

with open(pdf_file, "rb") as file:

        st.download_button(
            label="📄 Download PDF Report",
            data=file,
            file_name="ThermalGuardian_Report.pdf",
            mime="application/pdf"
     )



