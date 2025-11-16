from fpdf import FPDF
import pandas as pd
from typing import List, Dict
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px

class PDF(FPDF):
    """Extended FPDF class with Unicode support"""
    def __init__(self):
        super().__init__()
        self.add_page()
        
class ReportGenerator:
    """
    Generates comprehensive PDF reports with cost breakdowns and IRC citations
    """
    
    def __init__(self):
        self.pdf = None
    
    def _clean_text(self, text: str) -> str:
        """Remove or replace Unicode characters that FPDF can't handle"""
        if not isinstance(text, str):
            return str(text)
        # Replace common Unicode characters
        replacements = {
            '\u2022': '-',  # Bullet point
            '\u2013': '-',  # En dash
            '\u2014': '--', # Em dash
            '\u2018': "'",  # Left single quote
            '\u2019': "'",  # Right single quote
            '\u201c': '"',  # Left double quote
            '\u201d': '"',  # Right double quote
            '\u20b9': 'Rs.',# Rupee symbol
        }
        for old, new in replacements.items():
            text = text.replace(old, new)
        # Remove any remaining non-Latin-1 characters
        text = text.encode('latin-1', 'ignore').decode('latin-1')
        return text
    
    def generate_report(
        self,
        data: List[Dict],
        title: str = "Road Safety Audit Cost Estimate",
        project_name: str = "Highway Safety Improvement",
        consultant: str = "",
        date: str = None,
        include_citations: bool = True,
        include_charts: bool = True
    ) -> str:
        """
        Generate a comprehensive PDF report
        """
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        
        # Initialize PDF
        self.pdf = FPDF()
        self.pdf.add_page()
        
        # Generate report sections
        self._add_cover_page(title, project_name, consultant, date)
        self._add_executive_summary(data)
        self._add_detailed_estimate(data)
        
        if include_citations:
            self._add_irc_citations(data)
        
        self._add_cost_summary(data)
        
        # Save PDF
        filename = f"road_safety_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        self.pdf.output(filename)
        
        return filename
    
    def _add_cover_page(self, title: str, project: str, consultant: str, date: str):
        """Add cover page to report"""
        self.pdf.set_font("Arial", "B", 24)
        self.pdf.cell(0, 60, "", ln=True)
        self.pdf.cell(0, 20, self._clean_text(title), ln=True, align="C")
        
        self.pdf.set_font("Arial", "", 16)
        self.pdf.cell(0, 15, self._clean_text(project), ln=True, align="C")
        
        self.pdf.cell(0, 30, "", ln=True)
        
        self.pdf.set_font("Arial", "", 12)
        if consultant:
            self.pdf.cell(0, 10, self._clean_text(f"Prepared by: {consultant}"), ln=True, align="C")
        self.pdf.cell(0, 10, f"Date: {date}", ln=True, align="C")
        
        self.pdf.add_page()
    
    def _add_executive_summary(self, data: List[Dict]):
        """Add executive summary section"""
        self.pdf.set_font("Arial", "B", 16)
        self.pdf.cell(0, 10, "Executive Summary", ln=True)
        self.pdf.ln(5)
        
        df = pd.DataFrame(data)
        
        # Calculate summary statistics
        total_items = len(df)
        total_cost = df['total_with_gst'].sum() if 'total_with_gst' in df.columns else 0
        
        self.pdf.set_font("Arial", "", 11)
        
        summary_text = f"""
This report presents a detailed cost estimate for road safety interventions identified 
during the safety audit. The estimate includes {total_items} intervention items with a 
total estimated cost of Rs. {total_cost:,.2f} (including GST).

All cost estimates are based on IRC (Indian Roads Congress) standards and current 
market rates. The interventions are categorized and priced according to their type 
and specifications.
        """
        
        self.pdf.multi_cell(0, 6, self._clean_text(summary_text.strip()))
        self.pdf.ln(10)
    
    def _add_detailed_estimate(self, data: List[Dict]):
        """Add detailed cost estimate table"""
        self.pdf.add_page()
        self.pdf.set_font("Arial", "B", 14)
        self.pdf.cell(0, 10, "Detailed Cost Estimate", ln=True)
        self.pdf.ln(5)
        
        # Table header
        self.pdf.set_font("Arial", "B", 8)
        self.pdf.cell(10, 8, "No.", 1)
        self.pdf.cell(50, 8, "Intervention", 1)
        self.pdf.cell(30, 8, "Location", 1)
        self.pdf.cell(20, 8, "Qty", 1)
        self.pdf.cell(20, 8, "Unit", 1)
        self.pdf.cell(30, 8, "Rate (Rs.)", 1)
        self.pdf.cell(30, 8, "Cost (Rs.)", 1)
        self.pdf.ln()
        
        # Table data
        self.pdf.set_font("Arial", "", 7)
        
        for i, item in enumerate(data, 1):
            intervention = self._clean_text(item.get('intervention_type', ''))[:25]
            location = self._clean_text(item.get('location', ''))[:15]
            quantity = item.get('quantity', 0)
            unit = self._clean_text(item.get('unit', ''))
            rate = item.get('adjusted_rate', 0)
            cost = item.get('total_with_gst', 0)
            
            self.pdf.cell(10, 7, str(i), 1)
            self.pdf.cell(50, 7, intervention, 1)
            self.pdf.cell(30, 7, location, 1)
            self.pdf.cell(20, 7, f"{quantity:.2f}", 1)
            self.pdf.cell(20, 7, unit, 1)
            self.pdf.cell(30, 7, f"{rate:,.2f}", 1)
            self.pdf.cell(30, 7, f"{cost:,.2f}", 1)
            self.pdf.ln()
        
        self.pdf.ln(5)
    
    def _add_irc_citations(self, data: List[Dict]):
        """Add IRC code citations"""
        self.pdf.add_page()
        self.pdf.set_font("Arial", "B", 14)
        self.pdf.cell(0, 10, "IRC Code References", ln=True)
        self.pdf.ln(5)
        
        # Get unique IRC codes
        irc_codes = set()
        for item in data:
            if 'irc_code' in item:
                irc_codes.add(item['irc_code'])
        
        self.pdf.set_font("Arial", "", 10)
        
        irc_descriptions = {
            'IRC:99-2018': 'Tentative Guidelines on the Provision of Road Traffic Calming Measures',
            'IRC:35-2015': 'Code of Practice for Road Markings',
            'IRC:SP:73-2018': 'Manual of Specifications and Standards for Expressways',
            'IRC:67-2012': 'Code of Practice for Road Signs',
            'IRC:SP:21-2009': 'Standard Specifications and Code of Practice for Road Bridges',
            'IRC:93-1985': 'Guidelines on Design and Installation of Road Traffic Signals',
            'IRC:103-2012': 'Guidelines for Pedestrian Facilities'
        }
        
        for code in sorted(irc_codes):
            description = irc_descriptions.get(code, 'IRC Standard')
            self.pdf.multi_cell(0, 6, self._clean_text(f"- {code}: {description}"))
            self.pdf.ln(2)
    
    def _add_cost_summary(self, data: List[Dict]):
        """Add cost summary section"""
        self.pdf.add_page()
        self.pdf.set_font("Arial", "B", 14)
        self.pdf.cell(0, 10, "Cost Summary", ln=True)
        self.pdf.ln(5)
        
        df = pd.DataFrame(data)
        
        # Category-wise summary
        if 'category' in df.columns:
            self.pdf.set_font("Arial", "B", 11)
            self.pdf.cell(0, 8, "Category-wise Breakdown:", ln=True)
            self.pdf.ln(2)
            
            self.pdf.set_font("Arial", "B", 9)
            self.pdf.cell(100, 8, "Category", 1)
            self.pdf.cell(40, 8, "Count", 1)
            self.pdf.cell(50, 8, "Total Cost (Rs.)", 1)
            self.pdf.ln()
            
            self.pdf.set_font("Arial", "", 9)
            category_summary = df.groupby('category').agg({
                'total_with_gst': 'sum',
                'intervention_type': 'count'
            })
            
            for category, row in category_summary.iterrows():
                self.pdf.cell(100, 7, self._clean_text(str(category)), 1)
                self.pdf.cell(40, 7, str(row['intervention_type']), 1)
                self.pdf.cell(50, 7, f"{row['total_with_gst']:,.2f}", 1)
                self.pdf.ln()
        
        # Grand total
        self.pdf.ln(10)
        self.pdf.set_font("Arial", "B", 12)
        
        subtotal = df['total_cost'].sum() if 'total_cost' in df.columns else 0
        gst = df['gst_amount'].sum() if 'gst_amount' in df.columns else 0
        total = df['total_with_gst'].sum() if 'total_with_gst' in df.columns else 0
        
        self.pdf.cell(140, 8, "Subtotal:", 1)
        self.pdf.cell(50, 8, f"Rs. {subtotal:,.2f}", 1)
        self.pdf.ln()
        
        self.pdf.cell(140, 8, "GST @ 18%:", 1)
        self.pdf.cell(50, 8, f"Rs. {gst:,.2f}", 1)
        self.pdf.ln()
        
        self.pdf.set_font("Arial", "B", 13)
        self.pdf.cell(140, 10, "Grand Total:", 1)
        self.pdf.cell(50, 10, f"Rs. {total:,.2f}", 1)
