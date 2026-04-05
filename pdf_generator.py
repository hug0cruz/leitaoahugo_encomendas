from fpdf import FPDF

def gerar_pdf(encomendas, filename="encomendas.pdf"):
    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", size=10)

    for e in encomendas:
        _, produto, nome, telefone, data = e
        linha = f"{data} | {nome} | {produto}"
        pdf.cell(200, 8, txt=linha, ln=True)

    pdf.output(filename)
    return filename