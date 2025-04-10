import pandas as pd
from fpdf import FPDF
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

class ExportManager:
    @staticmethod
    def export_to_excel(entries, filename):
        df = pd.DataFrame(entries, columns=['Date', 'Type', 'Amount', 'Currency', 'Category'])
        df.to_excel(filename, index=False)

    @staticmethod
    def export_to_pdf(fig, entries, filename):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        
        # Add chart image
        fig.savefig('temp_plot.png')
        pdf.image('temp_plot.png', x=10, y=30, w=190)
        
        # Add table data
        pdf.ln(100)
        pdf.cell(200, 10, txt="Transaction Details", ln=True)
        for entry in entries:
            pdf.cell(200, 10, txt=f"{entry[0]} | {entry[1]} | {entry[2]} {entry[3]} | {entry[4]}", ln=True)
        
        pdf.output(filename)