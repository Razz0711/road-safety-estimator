import pandas as pd
from typing import List, Dict
from datetime import datetime

class PriceFetcher:
    """
    Fetches prices and calculates total costs for interventions
    """
    
    def __init__(self, location: str = "Tamil Nadu", year: int = 2024):
        self.location = location
        self.year = year
        # Price adjustment factors based on regional cost variations
        self.price_adjustment_factors = {
            # Southern States
            "Tamil Nadu": 1.00,
            "Karnataka": 1.05,
            "Kerala": 1.08,
            "Andhra Pradesh": 0.98,
            "Telangana": 1.02,
            "Puducherry": 1.03,
            
            # Western States
            "Maharashtra": 1.10,
            "Gujarat": 1.07,
            "Goa": 1.12,
            "Dadra and Nagar Haveli and Daman and Diu": 1.05,
            
            # Northern States
            "Delhi": 1.15,
            "Haryana": 1.08,
            "Punjab": 1.06,
            "Himachal Pradesh": 1.10,
            "Jammu and Kashmir": 1.12,
            "Ladakh": 1.18,
            "Chandigarh": 1.12,
            "Uttarakhand": 1.08,
            "Uttar Pradesh": 0.95,
            
            # Eastern States
            "West Bengal": 1.00,
            "Bihar": 0.90,
            "Jharkhand": 0.92,
            "Odisha": 0.93,
            "Sikkim": 1.15,
            "Assam": 0.95,
            "Arunachal Pradesh": 1.20,
            "Nagaland": 1.12,
            "Manipur": 1.10,
            "Mizoram": 1.12,
            "Tripura": 1.05,
            "Meghalaya": 1.08,
            "Andaman and Nicobar Islands": 1.25,
            
            # Central States
            "Madhya Pradesh": 0.94,
            "Chhattisgarh": 0.92,
            "Rajasthan": 0.98,
            
            # Union Territories
            "Lakshadweep": 1.30,
        }
    
    def calculate_costs(self, matched_data: List[Dict]) -> List[Dict]:
        """
        Calculate total costs for all interventions
        """
        priced_data = []
        
        for item in matched_data:
            # Get base rate
            base_rate = item.get('standard_rate', 0)
            
            # Apply location adjustment
            adjusted_rate = self._apply_location_adjustment(base_rate)
            
            # Apply year adjustment (inflation)
            adjusted_rate = self._apply_year_adjustment(adjusted_rate)
            
            # Calculate quantity
            quantity = item.get('quantity', 1.0)
            
            # Calculate total cost
            total_cost = adjusted_rate * quantity
            
            # Add GST (18%)
            gst_amount = total_cost * 0.18
            total_with_gst = total_cost + gst_amount
            
            # Create priced item
            priced_item = {
                **item,
                'adjusted_rate': round(adjusted_rate, 2),
                'total_cost': round(total_cost, 2),
                'gst_amount': round(gst_amount, 2),
                'total_with_gst': round(total_with_gst, 2),
                'location': self.location,
                'price_year': self.year
            }
            
            priced_data.append(priced_item)
        
        return priced_data
    
    def _apply_location_adjustment(self, base_rate: float) -> float:
        """
        Apply location-based price adjustment
        """
        factor = self.price_adjustment_factors.get(self.location, 1.0)
        return base_rate * factor
    
    def _apply_year_adjustment(self, rate: float) -> float:
        """
        Apply inflation adjustment based on year
        """
        current_year = datetime.now().year
        years_diff = current_year - self.year
        
        # Assume 5% annual inflation
        inflation_rate = 0.05
        adjustment_factor = (1 + inflation_rate) ** years_diff
        
        return rate * adjustment_factor
    
    def get_price_summary(self, priced_data: List[Dict]) -> Dict:
        """
        Generate a summary of prices
        """
        if not priced_data:
            return {}
        
        df = pd.DataFrame(priced_data)
        
        summary = {
            'total_items': len(df),
            'total_cost_before_gst': df['total_cost'].sum(),
            'total_gst': df['gst_amount'].sum(),
            'total_cost_with_gst': df['total_with_gst'].sum(),
            'average_cost_per_item': df['total_cost'].mean(),
            'category_breakdown': df.groupby('category')['total_with_gst'].sum().to_dict()
        }
        
        return summary
    
    def get_category_costs(self, priced_data: List[Dict]) -> pd.DataFrame:
        """
        Get costs grouped by category
        """
        df = pd.DataFrame(priced_data)
        
        category_summary = df.groupby('category').agg({
            'total_cost': 'sum',
            'gst_amount': 'sum',
            'total_with_gst': 'sum',
            'intervention_type': 'count'
        }).rename(columns={'intervention_type': 'count'})
        
        return category_summary
    
    def export_to_excel(self, priced_data: List[Dict], filename: str = "cost_estimate.xlsx"):
        """
        Export priced data to Excel
        """
        df = pd.DataFrame(priced_data)
        
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            # Main data sheet
            df.to_excel(writer, sheet_name='Detailed Estimate', index=False)
            
            # Summary sheet
            summary_df = self.get_category_costs(priced_data)
            summary_df.to_excel(writer, sheet_name='Category Summary')
            
            # Price summary
            price_summary = self.get_price_summary(priced_data)
            summary_data = pd.DataFrame([price_summary])
            summary_data.to_excel(writer, sheet_name='Overall Summary', index=False)
        
        return filename
