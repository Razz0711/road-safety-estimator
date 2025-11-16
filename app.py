import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
import io
from document_parser import DocumentParser
from matching_engine import MatchingEngine
from price_fetcher import PriceFetcher
from report_generator import ReportGenerator
from notification_service import get_notification_service
import time
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Road Safety Estimator",
    page_icon="🛣️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for animations and styling
st.markdown("""
<style>
    /* Clean professional background */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Main content area styling */
    .main > div {
        background: #ffffff;
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.15);
        border: 1px solid rgba(0, 0, 0, 0.05);
    }
    
    /* Animated title */
    @keyframes slideInFromLeft {
        0% { transform: translateX(-100%); opacity: 0; }
        100% { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes fadeInUp {
        0% { transform: translateY(30px); opacity: 0; }
        100% { transform: translateY(0); opacity: 1; }
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    @keyframes glow {
        0%, 100% { box-shadow: 0 0 5px #667eea, 0 0 10px #667eea; }
        50% { box-shadow: 0 0 20px #667eea, 0 0 30px #764ba2; }
    }
    
    h1 {
        animation: slideInFromLeft 0.8s ease-out;
        background: linear-gradient(45deg, #1e3a8a, #3b82f6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem !important;
        font-weight: 800 !important;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    
    h2, h3 {
        animation: fadeInUp 0.6s ease-out;
        color: #1e40af;
        font-weight: 700 !important;
    }
    
    /* Card styling */
    .stTabs [data-baseweb="tab-panel"] {
        animation: fadeInUp 0.5s ease-out;
        padding-top: 2rem;
    }
    
    /* Button animations */
    .stButton > button {
        background: linear-gradient(45deg, #2563eb, #1e40af) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(37, 99, 235, 0.3) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 6px 20px rgba(37, 99, 235, 0.5) !important;
        background: linear-gradient(45deg, #1d4ed8, #1e3a8a) !important;
    }
    
    /* File uploader styling */
    .uploadedFile {
        animation: fadeInUp 0.5s ease-out;
        border-radius: 15px;
        border: 2px dashed #2563eb !important;
        padding: 2rem;
        transition: all 0.3s ease;
    }
    
    .uploadedFile:hover {
        border-color: #1e40af !important;
        transform: scale(1.02);
    }
    
    /* Metric cards */
    [data-testid="stMetricValue"] {
        font-size: 2rem !important;
        font-weight: 700 !important;
        color: #1e40af !important;
    }
    
    [data-testid="stMetricLabel"] {
        font-weight: 600 !important;
        color: #64748b !important;
        font-size: 0.9rem !important;
    }
    
    /* Dataframe styling */
    .dataframe {
        animation: fadeInUp 0.6s ease-out;
        border-radius: 10px !important;
        overflow: hidden !important;
    }
    
    /* Progress bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #2563eb, #1e40af) !important;
    }
    
    /* Success/Error messages */
    .stSuccess, .stError, .stWarning, .stInfo {
        animation: fadeInUp 0.5s ease-out;
        border-radius: 10px !important;
        padding: 1rem !important;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e40af 0%, #1e3a8a 100%);
    }
    
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    [data-testid="stSidebar"] h2 {
        color: white !important;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: transparent;
        border-bottom: 2px solid #e2e8f0;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: #f8fafc;
        border-radius: 10px 10px 0 0;
        padding: 1rem 2rem;
        transition: all 0.3s ease;
        color: #64748b !important;
        font-weight: 600;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: #e2e8f0;
        transform: translateY(-2px);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(45deg, #2563eb, #1e40af) !important;
        color: white !important;
    }
    
    /* Floating animation for icons */
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    .floating {
        animation: float 3s ease-in-out infinite;
    }
    
    /* Spinner animation */
    .stSpinner > div {
        border-top-color: #2563eb !important;
        border-right-color: #1e40af !important;
    }
    
    /* Input fields */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select,
    .stDateInput > div > div > input {
        border-radius: 8px !important;
        border: 2px solid #e2e8f0 !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus,
    .stDateInput > div > div > input:focus {
        border-color: #2563eb !important;
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1) !important;
    }
    
    /* Dataframe styling */
    .dataframe {
        border-radius: 10px !important;
        border: 1px solid #e2e8f0 !important;
    }
    
    /* Checkbox styling */
    .stCheckbox {
        color: #1e293b !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'processed_data' not in st.session_state:
    st.session_state.processed_data = None
if 'report_generated' not in st.session_state:
    st.session_state.report_generated = False

def main():
    # Animated header
    st.markdown('<h1 class="floating">🛣️ Road Safety Estimator</h1>', unsafe_allow_html=True)
    st.markdown("""
        <div style='text-align: center; animation: fadeInUp 1s ease-out; margin-bottom: 2rem;'>
            <h3 style='color: #1e40af; font-weight: 600;'>✨ AI-Powered Road Safety Audit Cost Estimation System ✨</h3>
            <p style='color: #475569; font-size: 1.1rem;'>Transform your safety audits into actionable insights</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("## 📋 Process Flow")
        
        # Progress indicators with animations
        steps = [
            ("📄", "Upload Report", "upload"),
            ("🔍", "Extract Text", "extract"),
            ("📊", "Match Standards", "match"),
            ("💰", "Fetch Prices", "price"),
            ("📝", "Generate Report", "report")
        ]
        
        st.markdown("---")
        
        for emoji, step, key in steps:
            completed = st.session_state.get(f'{key}_completed', False)
            if completed:
                st.markdown(f"✅ **{emoji} {step}**")
            else:
                st.markdown(f"⚪ {emoji} {step}")
        
        st.markdown("---")
        
        # Animated info box
        st.markdown("""
            <div style='
                background: rgba(255, 255, 255, 0.2);
                padding: 1rem;
                border-radius: 15px;
                border: 2px solid rgba(255, 255, 255, 0.3);
                margin-top: 1rem;
                animation: glow 2s infinite;
            '>
                <p style='margin: 0; font-weight: 600; color: white;'>💡 Quick Tip</p>
                <p style='margin: 0.5rem 0 0 0; font-size: 0.9rem; color: white;'>
                    Upload clear, well-formatted documents for best results!
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        # Statistics (if available)
        if 'interventions' in st.session_state:
            st.markdown("---")
            st.markdown("### 📈 Current Session")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Items", len(st.session_state.interventions))
            with col2:
                if 'priced_data' in st.session_state:
                    total = sum(item.get('total_with_gst', 0) for item in st.session_state.priced_data)
                    st.metric("Total", f"₹{total/100000:.1f}L")
    
    # Main content with animated tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📤 Upload Document",
        "🔍 Smart Analysis", 
        "💰 Cost Estimation",
        "📊 Final Report"
    ])
    
    with tab1:
        upload_section()
    
    with tab2:
        analysis_section()
    
    with tab3:
        pricing_section()
    
    with tab4:
        report_section()

def upload_section():
    st.markdown("""
        <div style='text-align: center; margin-bottom: 2rem;'>
            <h2 style='color: #1e40af;'>📄 Upload Your Road Safety Audit Report</h2>
            <p style='color: #64748b; font-size: 1.05rem;'>Supported formats: PDF, DOCX, TXT</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        uploaded_file = st.file_uploader(
            "Drag and drop your file here",
            type=['pdf', 'docx', 'txt'],
            help="Upload your road safety audit report in PDF, DOCX, or TXT format",
            label_visibility="visible"
        )
        
        if uploaded_file is not None:
            st.markdown(f"""
                <div style='
                    background: linear-gradient(135deg, #10b981 0%, #059669 100%);
                    color: white;
                    padding: 1rem;
                    border-radius: 10px;
                    text-align: center;
                    margin: 1rem 0;
                    animation: fadeInUp 0.5s ease-out;
                    box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3);
                '>
                    ✅ <strong>File uploaded:</strong> {uploaded_file.name}
                </div>
            """, unsafe_allow_html=True)
            
            # Animated process button
            col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
            with col_btn2:
                if st.button("🚀 Process Document", type="primary", use_container_width=True):
                    # Progress bar animation
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    try:
                        # Initialize parser
                        status_text.text("🔄 Initializing parser...")
                        progress_bar.progress(20)
                        time.sleep(0.3)
                        
                        parser = DocumentParser()
                        
                        # Extract text
                        status_text.text("📖 Extracting text from document...")
                        progress_bar.progress(40)
                        text = parser.extract_text(uploaded_file)
                        st.session_state.extracted_text = text
                        time.sleep(0.3)
                        
                        # Identify interventions
                        status_text.text("🔍 Identifying interventions...")
                        progress_bar.progress(70)
                        interventions = parser.identify_interventions(text)
                        st.session_state.interventions = interventions
                        st.session_state.upload_completed = True
                        time.sleep(0.3)
                        
                        progress_bar.progress(100)
                        status_text.empty()
                        progress_bar.empty()
                        
                        st.balloons()
                        st.success(f"✅ Document processed successfully! Found **{len(interventions)}** interventions.")
                        time.sleep(1)
                        st.rerun()
                        
                    except Exception as e:
                        progress_bar.empty()
                        status_text.empty()
                        st.error(f"❌ Error processing document: {str(e)}")
    
    with col2:
        st.markdown("""
            <div style='
                background: #f8fafc;
                padding: 1.5rem;
                border-radius: 12px;
                border: 1px solid #e2e8f0;
                animation: fadeInUp 0.7s ease-out;
            '>
                <h3 style='color: #1e40af; margin-bottom: 1rem;'>📝 Supported Formats</h3>
                <ul style='list-style: none; padding: 0;'>
                    <li style='margin: 0.5rem 0; padding: 0.75rem; background: white; border-radius: 8px; border: 1px solid #e2e8f0; color: #1e293b;'>
                        📄 <strong>PDF</strong> (.pdf)
                    </li>
                    <li style='margin: 0.5rem 0; padding: 0.75rem; background: white; border-radius: 8px; border: 1px solid #e2e8f0; color: #1e293b;'>
                        📃 <strong>Word</strong> (.docx)
                    </li>
                    <li style='margin: 0.5rem 0; padding: 0.75rem; background: white; border-radius: 8px; border: 1px solid #e2e8f0; color: #1e293b;'>
                        📝 <strong>Text</strong> (.txt)
                    </li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown("""
            <div style='
                background: #f8fafc;
                padding: 1.5rem;
                border-radius: 12px;
                border: 1px solid #e2e8f0;
                animation: fadeInUp 0.9s ease-out;
            '>
                <h3 style='color: #1e40af; margin-bottom: 1rem;'>💡 Pro Tips</h3>
                <ul style='list-style: none; padding: 0; color: #475569;'>
                    <li style='margin: 0.5rem 0;'>✓ Ensure clear document quality</li>
                    <li style='margin: 0.5rem 0;'>✓ Include intervention details</li>
                    <li style='margin: 0.5rem 0;'>✓ Specify locations/chainage</li>
                    <li style='margin: 0.5rem 0;'>✓ Use standard terminology</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

def analysis_section():
    st.markdown("""
        <div style='text-align: center; margin-bottom: 2rem;'>
            <h2>🔍 Smart Intervention Analysis</h2>
            <p style='color: #718096;'>AI-powered identification and IRC standards matching</p>
        </div>
    """, unsafe_allow_html=True)
    
    if 'interventions' not in st.session_state:
        st.markdown("""
            <div style='
                text-align: center;
                padding: 3rem;
                background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
                border-radius: 20px;
                animation: fadeInUp 0.5s ease-out;
            '>
                <h3 style='color: #667eea;'>⚠️ No Document Processed Yet</h3>
                <p style='color: #718096; margin-top: 1rem;'>Please upload and process a document first!</p>
                <p style='font-size: 3rem; margin: 2rem 0;'>📄➡️🔍</p>
            </div>
        """, unsafe_allow_html=True)
        return
    
    interventions = st.session_state.interventions
    
    if len(interventions) == 0:
        st.info("No interventions identified in the document.")
        return
    
    # Display extracted text preview
    with st.expander("📄 Extracted Text Preview"):
        st.text_area(
            "Document Text",
            st.session_state.get('extracted_text', '')[:1000] + "...",
            height=200,
            disabled=True
        )
    
    # Display interventions with animation
    st.markdown(f"""
        <div style='
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 1.5rem;
            border-radius: 15px;
            text-align: center;
            margin: 2rem 0;
            animation: fadeInUp 0.5s ease-out;
        '>
            <h3 style='margin: 0; color: white;'>🔍 Identified Interventions</h3>
            <h1 style='margin: 0.5rem 0; font-size: 3rem; color: white;'>{len(interventions)}</h1>
            <p style='margin: 0; opacity: 0.9;'>Items detected in your document</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Match with IRC standards button
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    with col_btn2:
        if st.button("🔗 Match IRC Standards", type="primary", use_container_width=True):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                status_text.text("🔄 Loading IRC database...")
                progress_bar.progress(25)
                time.sleep(0.3)
                
                matcher = MatchingEngine()
                
                status_text.text("🔍 Matching interventions with standards...")
                progress_bar.progress(50)
                time.sleep(0.3)
                
                matched_data = matcher.match_standards(interventions)
                st.session_state.matched_data = matched_data
                st.session_state.match_completed = True
                
                progress_bar.progress(100)
                status_text.empty()
                progress_bar.empty()
                
                st.balloons()
                st.success("✅ Standards matched successfully!")
                time.sleep(1)
                st.rerun()
            except Exception as e:
                progress_bar.empty()
                status_text.empty()
                st.error(f"❌ Error matching standards: {str(e)}")
    
    # Display interventions table with better styling
    if interventions:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 📋 Detailed Intervention List")
        df = pd.DataFrame(interventions)
        
        # Style the dataframe
        st.dataframe(
            df,
            use_container_width=True,
            height=400
        )
    
    # Display matched data if available
    if 'matched_data' in st.session_state:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
            <div style='
                background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
                padding: 1rem;
                border-radius: 15px;
                text-align: center;
                margin: 2rem 0;
                animation: fadeInUp 0.5s ease-out;
            '>
                <h3 style='color: #667eea; margin: 0;'>📊 Matched IRC Standards</h3>
            </div>
        """, unsafe_allow_html=True)
        
        matched_df = pd.DataFrame(st.session_state.matched_data)
        st.dataframe(
            matched_df,
            use_container_width=True,
            height=400
        )

def pricing_section():
    st.markdown("""
        <div style='text-align: center; margin-bottom: 2rem;'>
            <h2>💰 Intelligent Cost Estimation</h2>
            <p style='color: #718096;'>Location-based pricing with real-time calculations</p>
        </div>
    """, unsafe_allow_html=True)
    
    if 'matched_data' not in st.session_state:
        st.markdown("""
            <div style='
                text-align: center;
                padding: 3rem;
                background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
                border-radius: 20px;
                animation: fadeInUp 0.5s ease-out;
            '>
                <h3 style='color: #667eea;'>⚠️ Analysis Not Complete</h3>
                <p style='color: #718096; margin-top: 1rem;'>Please complete the analysis section first!</p>
                <p style='font-size: 3rem; margin: 2rem 0;'>🔍➡️💰</p>
            </div>
        """, unsafe_allow_html=True)
        return
    
    matched_data = st.session_state.matched_data
    
    st.markdown("""
        <div style='
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
            padding: 2rem;
            border-radius: 20px;
            margin-bottom: 2rem;
            animation: fadeInUp 0.5s ease-out;
        '>
            <h3 style='color: #667eea; text-align: center; margin-bottom: 1.5rem;'>🎯 Configure Pricing Parameters</h3>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        location = st.selectbox(
            "📍 Select Location/State",
            [
                "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh",
                "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand",
                "Karnataka", "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur",
                "Meghalaya", "Mizoram", "Nagaland", "Odisha", "Punjab",
                "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana", "Tripura",
                "Uttar Pradesh", "Uttarakhand", "West Bengal",
                "Andaman and Nicobar Islands", "Chandigarh", "Dadra and Nagar Haveli and Daman and Diu",
                "Delhi", "Jammu and Kashmir", "Ladakh", "Lakshadweep", "Puducherry"
            ],
            help="Pricing varies by location"
        )
    
    with col2:
        price_year = st.selectbox(
            "📅 Price Reference Year",
            [2024, 2023, 2022, 2021],
            help="Inflation adjustments will be applied"
        )
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    with col_btn2:
        if st.button("💵 Calculate Prices", type="primary", use_container_width=True):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                status_text.text("🔄 Initializing price calculator...")
                progress_bar.progress(20)
                time.sleep(0.3)
                
                fetcher = PriceFetcher(location=location, year=price_year)
                
                status_text.text(f"📍 Applying {location} pricing...")
                progress_bar.progress(50)
                time.sleep(0.3)
                
                status_text.text("💰 Calculating costs with GST...")
                progress_bar.progress(80)
                priced_data = fetcher.calculate_costs(matched_data)
                st.session_state.priced_data = priced_data
                st.session_state.price_completed = True
                time.sleep(0.3)
                
                progress_bar.progress(100)
                status_text.empty()
                progress_bar.empty()
                
                st.balloons()
                st.success("✅ Prices calculated successfully!")
                time.sleep(1)
                st.rerun()
            except Exception as e:
                progress_bar.empty()
                status_text.empty()
                st.error(f"❌ Error calculating prices: {str(e)}")
    
    # Display priced data
    if 'priced_data' in st.session_state:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
            <div style='
                background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
                padding: 1rem;
                border-radius: 15px;
                text-align: center;
                margin: 2rem 0;
                animation: fadeInUp 0.5s ease-out;
            '>
                <h3 style='color: #667eea; margin: 0;'>📊 Comprehensive Cost Breakdown</h3>
            </div>
        """, unsafe_allow_html=True)
        
        priced_df = pd.DataFrame(st.session_state.priced_data)
        
        # Add total row
        total_cost = priced_df['total_cost'].sum() if 'total_cost' in priced_df.columns else 0
        total_with_gst = priced_df['total_with_gst'].sum() if 'total_with_gst' in priced_df.columns else 0
        
        # Animated metrics
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("📦 Total Items", len(priced_df))
        with col2:
            st.metric("💵 Subtotal", f"₹{total_cost/100000:.2f}L")
        with col3:
            st.metric("💰 With GST", f"₹{total_with_gst/100000:.2f}L")
        with col4:
            avg_cost = total_cost / len(priced_df) if len(priced_df) > 0 else 0
            st.metric("📊 Avg/Item", f"₹{avg_cost/1000:.1f}K")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.dataframe(priced_df, use_container_width=True, height=400)

def report_section():
    st.markdown("""
        <div style='text-align: center; margin-bottom: 2rem;'>
            <h2>📊 Generate Professional Report</h2>
            <p style='color: #718096;'>Create comprehensive PDF documentation with IRC citations</p>
        </div>
    """, unsafe_allow_html=True)
    
    if 'priced_data' not in st.session_state:
        st.markdown("""
            <div style='
                text-align: center;
                padding: 3rem;
                background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
                border-radius: 20px;
                animation: fadeInUp 0.5s ease-out;
            '>
                <h3 style='color: #667eea;'>⚠️ Pricing Not Complete</h3>
                <p style='color: #718096; margin-top: 1rem;'>Please complete the pricing section first!</p>
                <p style='font-size: 3rem; margin: 2rem 0;'>💰➡️📊</p>
            </div>
        """, unsafe_allow_html=True)
        return
    
    priced_data = st.session_state.priced_data
    
    st.markdown("""
        <div style='
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
            padding: 2rem;
            border-radius: 20px;
            margin-bottom: 2rem;
            animation: fadeInUp 0.5s ease-out;
        '>
            <h3 style='color: #667eea; text-align: center; margin-bottom: 1.5rem;'>📝 Report Configuration</h3>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        report_title = st.text_input("📄 Report Title", "Road Safety Audit Cost Estimate")
        project_name = st.text_input("🏗️ Project Name", "Highway Safety Improvement")
    
    with col2:
        consultant_name = st.text_input("👤 Consultant Name", "")
        report_date = st.date_input("📅 Report Date")
    
    col3, col4 = st.columns(2)
    with col3:
        include_citations = st.checkbox("📚 Include IRC Citations", value=True)
    with col4:
        include_charts = st.checkbox("📈 Include Charts and Graphs", value=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    with col_btn2:
        if st.button("📄 Generate Final Report", type="primary", use_container_width=True):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                status_text.text("📝 Initializing report generator...")
                progress_bar.progress(20)
                time.sleep(0.3)
                
                generator = ReportGenerator()
                
                status_text.text("📊 Creating cost breakdown...")
                progress_bar.progress(40)
                time.sleep(0.3)
                
                status_text.text("📚 Adding IRC citations...")
                progress_bar.progress(60)
                time.sleep(0.3)
                
                status_text.text("🎨 Formatting report...")
                progress_bar.progress(80)
                
                report_path = generator.generate_report(
                    data=priced_data,
                    title=report_title,
                    project_name=project_name,
                    consultant=consultant_name,
                    date=str(report_date),
                    include_citations=include_citations,
                    include_charts=include_charts
                )
                
                st.session_state.report_path = report_path
                st.session_state.report_completed = True
                st.session_state.project_name = project_name
                st.session_state.report_date = report_date
                st.session_state.consultant_name = consultant_name
                
                progress_bar.progress(100)
                status_text.empty()
                progress_bar.empty()
                
                st.balloons()
                st.success("✅ Report generated successfully!")
                
            except Exception as e:
                progress_bar.empty()
                status_text.empty()
                st.error(f"❌ Error generating report: {str(e)}")
        
        # Show download and email options if report was generated
        if st.session_state.get('report_completed') and st.session_state.get('report_path'):
            report_path = st.session_state.report_path
            project_name = st.session_state.get('project_name', 'Road Safety Project')
            report_date = st.session_state.get('report_date', 'Unknown')
            consultant_name = st.session_state.get('consultant_name', 'Unknown')
            priced_data = st.session_state.get('priced_data', [])
            
            # Download button
            st.markdown("<br>", unsafe_allow_html=True)
            with open(report_path, 'rb') as f:
                st.download_button(
                    label="📥 Download Report (PDF)",
                    data=f,
                    file_name=f"road_safety_report_{report_date}.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                    key="download_report_btn"
                )
            
            # Email Sharing Section - Professional Design
            st.markdown("<br><br>", unsafe_allow_html=True)
            
            # Get notification service
            notification_service = get_notification_service()
            config = notification_service.get_configuration_instructions()
            
            # Container with professional styling
            with st.container():
                st.markdown("""
                    <div style='
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        padding: 2rem;
                        border-radius: 12px;
                        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                        margin-bottom: 1.5rem;
                    '>
                        <h3 style='color: white; margin: 0; text-align: center; font-weight: 600;'>
                            📧 Share Report via Email
                        </h3>
                        <p style='color: rgba(255, 255, 255, 0.9); text-align: center; margin-top: 0.5rem; margin-bottom: 0;'>
                            Send the PDF report directly to your recipient's inbox
                        </p>
                    </div>
                """, unsafe_allow_html=True)
                
                # Configuration Status - Compact design
                if config['email']['configured']:
                    st.success("✅ Email service ready", icon="✅")
                else:
                    col_warn, col_info = st.columns([3, 1])
                    with col_warn:
                        st.warning("⚠️ Email not configured - Setup required", icon="⚠️")
                    with col_info:
                        if st.button("ℹ️ Setup Guide", key="email_setup_btn", use_container_width=True):
                            st.session_state.show_email_setup = not st.session_state.get('show_email_setup', False)
                            st.rerun()
                    
                    if st.session_state.get('show_email_setup', False):
                        with st.expander("📋 Email Setup Instructions (FREE with Gmail)", expanded=True):
                            st.markdown(config['email']['instructions'])
                            if st.button("✖️ Close", key="close_setup_btn"):
                                st.session_state.show_email_setup = False
                                st.rerun()
                
                # Email Form - Clean design
                st.markdown("<br>", unsafe_allow_html=True)
                
                col1, col2 = st.columns([3, 1])
                with col1:
                    email_address = st.text_input(
                        "Recipient Email",
                        placeholder="Enter recipient's email address",
                        label_visibility="collapsed",
                        key="recipient_email"
                    )
                with col2:
                    send_button = st.button(
                        "📤 Send", 
                        use_container_width=True, 
                        type="primary",
                        disabled=not email_address
                    )
                
                if send_button:
                    if email_address:
                        # Email subject and body with HTML formatting
                        subject = f"Road Safety Cost Estimate Report - {project_name}"
                        body = f"""<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 10px 10px 0 0; }}
        .content {{ background: #f9f9f9; padding: 20px; border: 1px solid #e0e0e0; }}
        .info-box {{ background: white; border-left: 4px solid #667eea; padding: 15px; margin: 15px 0; }}
        .info-item {{ margin: 8px 0; }}
        .info-label {{ font-weight: bold; color: #667eea; }}
        .footer {{ background: #f0f0f0; padding: 15px; text-align: center; border-radius: 0 0 10px 10px; font-size: 12px; color: #666; }}
        hr {{ border: none; border-top: 2px solid #e0e0e0; margin: 20px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h2 style="margin: 0;">📋 Road Safety Cost Estimate Report</h2>
        </div>
        <div class="content">
            <p>Dear Recipient,</p>
            <p>Please find attached the Road Safety Cost Estimate Report for your review.</p>
            
            <div class="info-box">
                <h3 style="color: #667eea; margin-top: 0;">Project Information:</h3>
                <div class="info-item"><span class="info-label">• Project Name:</span> {project_name}</div>
                <div class="info-item"><span class="info-label">• Report Date:</span> {report_date}</div>
                <div class="info-item"><span class="info-label">• Consultant:</span> {consultant_name}</div>
                <div class="info-item"><span class="info-label">• Total Items:</span> {len(priced_data)}</div>
                <div class="info-item"><span class="info-label">• Estimated Cost:</span> ₹{sum(item.get('total_with_gst', 0) for item in priced_data)/100000:.2f} Lakhs</div>
            </div>
            
            <hr>
            
            <p>The attached PDF contains a comprehensive breakdown of all road safety items, quantities, rates, and cost estimates.</p>
            <p>If you have any questions or require clarification, please feel free to reach out.</p>
            
            <p style="margin-top: 30px;">
                <strong>Best regards,</strong><br>
                Road Safety Estimator Team
            </p>
        </div>
        <div class="footer">
            This report was automatically generated by Road Safety Estimator
        </div>
    </div>
</body>
</html>"""
                        
                        with st.spinner("📨 Sending email..."):
                            success, msg = notification_service.send_email(
                                email_address,
                                subject,
                                body,
                                report_path
                            )
                            
                            if success:
                                st.success(f"✅ Email sent successfully to **{email_address}**", icon="✅")
                                st.balloons()
                            else:
                                st.error(f"❌ Failed to send email: {msg}", icon="❌")
                                if not config['email']['configured']:
                                    st.info("💡 **Setup Required:** Configure Gmail SMTP in `.env` file. Click 'Setup Guide' above for instructions.", icon="💡")
                    else:
                        st.warning("⚠️ Please enter a valid email address", icon="⚠️")
                
                # Footer info - subtle
                st.markdown("""
                    <div style='
                        text-align: center; 
                        padding: 1rem; 
                        color: #666; 
                        font-size: 0.85rem;
                        margin-top: 1rem;
                        border-top: 1px solid #e0e0e0;
                    '>
                        🔒 Secure • 🆓 Free Gmail SMTP • 📎 PDF Attachment Included
                    </div>
                """, unsafe_allow_html=True)
    
    # Preview section
    if 'priced_data' in st.session_state:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
            <div style='
                background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
                padding: 1rem;
                border-radius: 15px;
                text-align: center;
                margin: 2rem 0;
                animation: fadeInUp 0.5s ease-out;
            '>
                <h3 style='color: #667eea; margin: 0;'>�️ Report Preview</h3>
            </div>
        """, unsafe_allow_html=True)
        
        with st.expander("📊 View Data Summary", expanded=False):
            df = pd.DataFrame(priced_data)
            st.dataframe(df, use_container_width=True, height=300)
            
            if include_charts:
                import plotly.express as px
                
                if 'category' in df.columns and 'total_cost' in df.columns:
                    st.markdown("<br>", unsafe_allow_html=True)
                    fig = px.pie(
                        df, 
                        values='total_cost', 
                        names='category',
                        title='Cost Distribution by Category',
                        color_discrete_sequence=px.colors.sequential.Purples_r
                    )
                    fig.update_layout(
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        font=dict(size=14)
                    )
                    st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()
