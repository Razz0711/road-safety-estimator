# 🚦 Road Safety Estimator# 🛣️ Road Safety Estimator



**AI-Powered Cost Estimation Tool for Road Safety Projects**AI-Powered Road Safety Audit Cost Estimation System



A comprehensive Streamlit application that analyzes documents, identifies road safety interventions, matches them with IRC (Indian Roads Congress) standards, and generates detailed cost estimates with professional PDF reports.## Overview



---This application automatically processes road safety audit reports and generates detailed cost estimates based on IRC (Indian Roads Congress) standards.



## 🎯 Features## Features



### 📄 Document Processing### 1. 📄 Document Parser

- **Multi-format Support**: PDF, DOCX, and TXT files- Extracts text from PDF, DOCX, and TXT files

- **Intelligent Parsing**: Automatic text extraction and analysis- Identifies road safety interventions automatically

- **Intervention Detection**: AI-powered identification of road safety measures- Extracts locations, chainages, and quantities



### 🔍 IRC Standard Matching### 2. 🔍 Matching Engine

- **Fuzzy Matching Engine**: Accurate matching with IRC specifications- Matches interventions with IRC standards

- **Comprehensive Database**: Based on IRC standards (SP:98-2013, SP:87-2013, etc.)- Uses fuzzy matching for accurate identification

- **Multiple Categories**: Traffic Calming, Road Marking, Safety Barriers, Signage, Traffic Control- References IRC codes and specifications



### 💰 Cost Estimation### 3. 💰 Price Fetcher

- **Location-Based Pricing**: Adjustments for all 36 Indian states/UTs- Calculates costs based on location

- **Inflation Calculation**: Year-based price adjustments- Applies inflation adjustments

- **GST Inclusion**: Automatic 18% GST calculation- Includes GST calculations

- **Detailed Breakdown**: Item-wise cost analysis

### 4. 📊 Report Generator

### 📊 Professional Reports- Creates comprehensive PDF reports

- **PDF Generation**: Comprehensive cost estimation reports- Includes cost breakdowns

- **IRC Citations**: Proper referencing of standards- Provides IRC citations

- **Visual Layout**: Clean, professional formatting- Generates summary statistics



---## Installation



## 🚀 Quick Start1. Create a virtual environment:

```cmd

```cmdpython -m venv venv

# Install dependencies```

pip install -r requirements.txt

2. Activate the virtual environment:

# Run application```cmd

venv\Scripts\python.exe -m streamlit run app.pyvenv\Scripts\activate

```

# Access at: http://localhost:8501

```3. Install dependencies:

```cmd

---pip install -r requirements.txt

```

## 📦 Core Files

## Usage

```

road-safety-estimator/1. Run the application:

├── app.py                  # Main Streamlit application```cmd

├── document_parser.py      # Document processingstreamlit run app.py

├── matching_engine.py      # IRC matching logic```

├── price_fetcher.py        # Cost calculation

├── report_generator.py     # PDF generation2. Open your browser to `http://localhost:8501`

├── GPT_Input_DB.xlsx      # IRC standards database

└── requirements.txt        # Dependencies3. Follow the workflow:

```   - Upload your road safety audit report

   - Review identified interventions

---   - Match with IRC standards

   - Calculate prices

## 🎮 Usage   - Generate final report



1. **Upload Document** → PDF/DOCX/TXT with road safety audit report## Database

2. **Review Analysis** → Check identified interventions and IRC matches

3. **Calculate Prices** → Select location and yearPlace your `GPT_Input_DB.xlsx` file in the project root directory. The file should contain:

4. **Generate Report** → Download professional PDF

- **Intervention Type**: Type of safety intervention

---- **IRC Code**: Relevant IRC standard code

- **Specification**: Detailed specifications

## 🌍 Coverage- **Unit**: Unit of measurement

- **Standard Rate**: Base rate per unit

- **36 Locations**: All Indian states and union territories- **Category**: Category classification

- **Location Factors**: Region-specific price adjustments

- **IRC Standards**: Complete specifications database## Supported Interventions



---- Rumble Strips

- Speed Humps

## 🔧 Tech Stack- Road Markings

- Guard Rails

- **Frontend**: Streamlit- Signage

- **Backend**: Python 3.13.2- Street Lights

- **Document Processing**: PyPDF2, pdfplumber, python-docx- Crash Barriers

- **Data Analysis**: pandas, numpy- Delineators

- **Matching**: fuzzywuzzy, Levenshtein- Traffic Signals

- **Reports**: FPDF- Pedestrian Crossings

- And more...

---

## IRC Standards Covered

**Built for Road Safety** 🚗🛣️✨

- IRC:99-2018 (Traffic Calming)
- IRC:35-2015 (Road Markings)
- IRC:67-2012 (Road Signs)
- IRC:SP:73-2018 (Expressways)
- IRC:93-1985 (Traffic Signals)
- IRC:103-2012 (Pedestrian Facilities)

## Output

The system generates:
- Detailed cost estimates
- Category-wise breakdown
- IRC code references
- PDF reports
- Excel exports

## Technology Stack

- **Frontend**: Streamlit
- **Data Processing**: Pandas, NumPy
- **Document Parsing**: PyPDF2, pdfplumber, python-docx
- **Matching**: FuzzyWuzzy
- **Report Generation**: FPDF
- **Visualization**: Plotly

## Project Structure

```
road-safety-estimator/
├── app.py                  # Main Streamlit application
├── document_parser.py      # Document text extraction
├── matching_engine.py      # IRC standard matching
├── price_fetcher.py        # Price calculation
├── report_generator.py     # PDF report generation
├── requirements.txt        # Python dependencies
├── GPT_Input_DB.xlsx      # IRC standards database
└── README.md              # Documentation
```

## License

MIT License

## Contact

For questions or support, please contact the development team.
