# Python Planner

After searching for a PDF weekly planner for my iPad I decided to try and create one with python.

## Libraries
###Considered

- pyPdf
  - Doesn't seem to have recent documentation http://pybrary.net/pyPdf/pythondoc-pyPdf.pdf.html
- PyPDF2
  - Contains a class labeled [`PdfFileWriter`](https://pythonhosted.org/PyPDF2/PdfFileWriter.html)
- PyPDF4
  - Doesn't appear to have any documentation
- fpdf
  - https://pyfpdf.readthedocs.io/en/latest/
- ReportLab
  - Definetely has ability to create PDFs
  - https://www.reportlab.com/docs/reportlab-userguide.pdf
- pdfrw
  - seems to be more based around editing rather than creating
- PDFMiner
  - "PDFMiner is a text extraction tool for PDF documents." https://pypi.org/project/pdfminer/

### Decision
I ended up choosing FPDF because it seemed to have the best documentation