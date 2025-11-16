import pandas as pd
from fuzzywuzzy import fuzz, process
from typing import List, Dict
import os

class MatchingEngine:
    """
    Matches identified interventions with IRC standards and specifications
    """
    
    def __init__(self, database_path='GPT_Input_DB.xlsx'):
        self.database_path = database_path
        self.irc_database = None
        self.load_database()
    
    def load_database(self):
        """Load the IRC standards database"""
        # Check if database exists in parent directory
        db_paths = [
            self.database_path,
            os.path.join('..', self.database_path),
            os.path.join('..', '..', self.database_path)
        ]
        
        for path in db_paths:
            if os.path.exists(path):
                try:
                    self.irc_database = pd.read_excel(path)
                    print(f"Database loaded from: {path}")
                    return
                except Exception as e:
                    print(f"Error loading database from {path}: {e}")
        
        # Create a default database if file not found
        print("Creating default IRC standards database...")
        self.irc_database = self._create_default_database()
    
    def _create_default_database(self) -> pd.DataFrame:
        """Create a default IRC standards database"""
        data = {
            'Intervention Type': [
                'Rumble Strip', 'Speed Hump', 'Road Marking', 'Guard Rail',
                'Signage', 'Street Light', 'Crash Barrier', 'Delineator',
                'Reflector', 'Chevron Sign', 'Warning Sign', 'Regulatory Sign',
                'Pavement Marking', 'Traffic Signal', 'Pedestrian Crossing'
            ],
            'IRC Code': [
                'IRC:99-2018', 'IRC:99-2018', 'IRC:35-2015', 'IRC:SP:73-2018',
                'IRC:67-2012', 'IRC:SP:21-2009', 'IRC:SP:73-2018', 'IRC:35-2015',
                'IRC:35-2015', 'IRC:67-2012', 'IRC:67-2012', 'IRC:67-2012',
                'IRC:35-2015', 'IRC:93-1985', 'IRC:103-2012'
            ],
            'Specification': [
                'Thermoplastic rumble strips, 100mm width',
                'Speed hump as per IRC standards',
                'Thermoplastic road marking paint',
                'W-beam metal guard rail',
                'Retroreflective signage as per IRC',
                'LED street light 150W',
                'Concrete crash barrier',
                'Road delineator posts',
                'Reflective markers',
                'Chevron alignment markers',
                'Triangle warning signs',
                'Circular regulatory signs',
                'Thermoplastic pavement marking',
                'Traffic signal poles and lights',
                'Zebra crossing markings'
            ],
            'Unit': [
                'm', 'Nos', 'sqm', 'm', 'Nos', 'Nos', 'm', 'Nos',
                'Nos', 'Nos', 'Nos', 'Nos', 'sqm', 'Nos', 'sqm'
            ],
            'Standard Rate': [
                500, 25000, 350, 1500, 5000, 15000, 2500, 800,
                200, 3000, 2500, 2500, 350, 250000, 400
            ],
            'Category': [
                'Traffic Calming', 'Traffic Calming', 'Road Marking', 'Safety Barrier',
                'Signage', 'Lighting', 'Safety Barrier', 'Delineation',
                'Delineation', 'Signage', 'Signage', 'Signage',
                'Road Marking', 'Traffic Control', 'Road Marking'
            ]
        }
        
        return pd.DataFrame(data)
    
    def match_standards(self, interventions: List[Dict]) -> List[Dict]:
        """
        Match interventions with IRC standards from database
        """
        matched_data = []
        
        for intervention in interventions:
            # Find best match in database
            match = self._find_best_match(intervention)
            
            if match is not None:
                matched_item = {
                    'intervention_type': intervention['type'],
                    'description': intervention['description'],
                    'location': intervention.get('location', ''),
                    'chainage': intervention.get('chainage', ''),
                    'quantity': intervention.get('quantity', 1.0),
                    'unit': match['Unit'],
                    'irc_code': match['IRC Code'],
                    'specification': match['Specification'],
                    'standard_rate': match['Standard Rate'],
                    'category': match['Category']
                }
                matched_data.append(matched_item)
        
        return matched_data
    
    def _find_best_match(self, intervention: Dict) -> Dict:
        """
        Find the best matching IRC standard for an intervention
        """
        intervention_type = intervention['type']
        
        # Get all intervention types from database
        db_types = self.irc_database['Intervention Type'].tolist()
        
        # Use fuzzy matching to find best match
        best_match = process.extractOne(
            intervention_type,
            db_types,
            scorer=fuzz.token_sort_ratio
        )
        
        if best_match and best_match[1] > 60:  # 60% match threshold
            # Get the matching row from database
            match_idx = self.irc_database[
                self.irc_database['Intervention Type'] == best_match[0]
            ].index[0]
            
            return self.irc_database.iloc[match_idx].to_dict()
        
        return None
    
    def get_specifications(self, intervention_type: str) -> Dict:
        """
        Get detailed specifications for a specific intervention type
        """
        matches = self.irc_database[
            self.irc_database['Intervention Type'].str.lower() == intervention_type.lower()
        ]
        
        if not matches.empty:
            return matches.iloc[0].to_dict()
        
        return None
    
    def get_all_standards(self) -> pd.DataFrame:
        """
        Return the complete IRC standards database
        """
        return self.irc_database
