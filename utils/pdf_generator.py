from fpdf import FPDF

def generate_pdf_report(data, detailed=False):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.set_text_color(255, 255, 255)
    pdf.set_fill_color(33, 33, 33)
    pdf.cell(200, 10, txt="CNC Tool Parameter Report", ln=True, align="C", fill=True)
    pdf.set_text_color(0, 0, 0)
    pdf.ln(10)

    for key, value in data.items():
        if not detailed and key.lower().startswith("estimated"):
            continue
        line = f"{key}: {value}"
        pdf.cell(200, 10, txt=line, ln=True, align="L")

    return pdf.output(dest='S').encode('latin1')
