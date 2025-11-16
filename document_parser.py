import PyPDF2
import docx
import re
from typing import List, Dict
import pdfplumber

class DocumentParser:
    """
    Extracts text from documents and identifies road safety interventions
    """
    
    def __init__(self):
        self.intervention_keywords = [
            'rumble strip', 'speed hump', 'speed breaker', 'signage', 'road marking',
            'guard rail', 'crash barrier', 'street light', 'road furniture',
            'pavement marking', 'chevron sign', 'warning sign', 'regulatory sign',
            'reflector', 'delineator', 'traffic signal', 'pedestrian crossing',
            'speed limit', 'road widening', 'intersection improvement', 'curve improvement',
            'shoulder paving', 'drainage', 'cattle catcher', 'solar blinker'
        ]
    
    def extract_text(self, file) -> str:
        """
        Extract text from uploaded file based on file type
        """
        file_extension = file.name.split('.')[-1].lower()
        
        if file_extension == 'pdf':
            return self._extract_from_pdf(file)
        elif file_extension == 'docx':
            return self._extract_from_docx(file)
        elif file_extension == 'txt':
            return self._extract_from_txt(file)
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")
    
    def _extract_from_pdf(self, file) -> str:
        """Extract text from PDF using pdfplumber"""
        text = ""
        try:
            with pdfplumber.open(file) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() + "\n"
        except Exception as e:
            # Fallback to PyPDF2
            file.seek(0)
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        
        return text
    
    def _extract_from_docx(self, file) -> str:
        """Extract text from DOCX file"""
        doc = docx.Document(file)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    
    def _extract_from_txt(self, file) -> str:
        """Extract text from TXT file"""
        return file.read().decode('utf-8')
    
    def identify_interventions(self, text: str) -> List[Dict]:
        """
        Identify road safety interventions from extracted text
        """
        interventions = []
        lines = text.split('\n')
        
        for i, line in enumerate(lines):
            line_lower = line.lower()
            
            # Skip empty lines or very short lines
            if len(line.strip()) < 10:
                continue
            
            # Check for intervention keywords
            for keyword in self.intervention_keywords:
                if keyword in line_lower:
                    intervention = self._extract_intervention_details(line, lines, i)
                    if intervention and intervention['description']:
                        interventions.append(intervention)
                    break  # Only match one keyword per line
        
        # Remove exact duplicates based on description
        unique_interventions = []
        seen_descriptions = set()
        for intervention in interventions:
            desc = intervention['description'].strip().lower()
            if desc not in seen_descriptions and len(desc) > 10:
                seen_descriptions.add(desc)
                unique_interventions.append(intervention)
        
        return unique_interventions
    
    def _extract_intervention_details(self, line: str, all_lines: List[str], index: int) -> Dict:
        """
        Extract detailed information about an intervention
        """
        intervention = {
            'type': self._identify_intervention_type(line),
            'description': line.strip(),
            'location': self._extract_location(line),
            'chainage': self._extract_chainage(line),
            'quantity': self._extract_quantity(line),
            'unit': self._extract_unit(line)
        }
        
        return intervention
    
    def _identify_intervention_type(self, line: str) -> str:
        """Identify the type of intervention"""
        line_lower = line.lower()
        
        for keyword in self.intervention_keywords:
            if keyword in line_lower:
                return keyword.title()
        
        return "Other"
    
    def _extract_location(self, line: str) -> str:
        """Extract location/chainage information"""
        # Look for patterns like "at km 10.5" or "chainage 10+500"
        patterns = [
            r'at km\s*(\d+\.?\d*)',
            r'km\s*(\d+\.?\d*)',
            r'chainage\s*(\d+\+?\d*)',
            r'ch\s*(\d+\+?\d*)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, line, re.IGNORECASE)
            if match:
                return f"Km {match.group(1)}"
        
        return "Location not specified"
    
    def _extract_chainage(self, line: str) -> str:
        """Extract chainage information"""
        patterns = [
            r'(\d+\+\d+)',
            r'km\s*(\d+\.?\d*)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, line, re.IGNORECASE)
            if match:
                return match.group(1)
        
        return ""
    
    def _extract_quantity(self, line: str) -> float:
        """Extract quantity from line"""
        # Look for numbers followed by units
        patterns = [
            r'(\d+\.?\d*)\s*(?:nos?|numbers?|qty)',
            r'(\d+\.?\d*)\s*(?:m|meter|metre)',
            r'(\d+\.?\d*)\s*(?:km|kilometer|kilometre)',
            r'(\d+\.?\d*)\s*(?:sqm|sq\.m|square meter)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, line, re.IGNORECASE)
            if match:
                return float(match.group(1))
        
        # Default quantity
        return 1.0
    
    def _extract_unit(self, line: str) -> str:
        """Extract unit of measurement"""
        line_lower = line.lower()
        
        units = {
            'nos': 'Nos',
            'number': 'Nos',
            'meter': 'm',
            'metre': 'm',
            'kilometer': 'km',
            'kilometre': 'km',
            'square meter': 'sqm',
            'sqm': 'sqm',
            'sq.m': 'sqm'
        }
        
        for key, value in units.items():
            if key in line_lower:
                return value
        
        return 'Nos'
