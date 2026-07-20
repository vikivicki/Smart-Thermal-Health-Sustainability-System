from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet


def generate_pdf(
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
):

    filename = "ThermalGuardian_Report.pdf"

    doc = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    story = []

    story.append(Paragraph("<b>ThermalGuardian AI Report</b>", styles["Title"]))

    story.append(Paragraph(f"Hot Side Heat Transfer : {q_hot:.2f} kW", styles["Normal"]))

    story.append(Paragraph(f"Cold Side Heat Transfer : {q_cold:.2f} kW", styles["Normal"]))


    story.append(Paragraph(f"Heat Balance Error : {heat_error:.2f} %", styles["Normal"]))

    story.append(Paragraph(f"LMTD : {lmtd:.2f} °C", styles["Normal"]))

    story.append(Paragraph(f"Overall U : {U:.2f} W/m²K", styles["Normal"]))

    story.append(Paragraph(f"Effectiveness : {effectiveness:.2f}", styles["Normal"]))

    story.append(Paragraph(f"Fouling Factor : {fouling:.6f}", styles["Normal"]))

    story.append(Paragraph("<br/><b>Clean & Green Metrics</b>", styles["Heading2"]))

    story.append(
    Paragraph(
        f"Estimated Energy Loss : {energy_loss:.2f} kW",
        styles["Normal"]
    )
)

    story.append(
    Paragraph(
        f"Estimated CO₂ Reduction : {co2_saved:.2f} kg/day",
        styles["Normal"]
    )
)

    story.append(
    Paragraph(
        f"Sustainability Score : {green_score}/100",
        styles["Normal"]
    )
)



   

    doc.build(story)

    return filename