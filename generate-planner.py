from fpdf import FPDF

# https://pyfpdf.github.io/fpdf2/

pdf = FPDF(orientation="l")
pdf.add_page()

with pdf.new_path() as path:
    path.style.stroke_width = 1
    path.move_to(10, 10)
    path.line_to(100, 10)
    path.close()


with pdf.new_path() as path:
    path.style.stroke_width = 0.25
    path.move_to(10, 50)
    path.line_to(200, 50)
    path.close()

pdf.set_y(100)
pdf.set_font('helvetica', 'B', 16)
pdf.cell(txt='Week of this one!')

pdf.output("test.pdf")