"""Streamlit UI for MedIntel AI - Interactive PDF Upload and Medical Data Extraction."""

import streamlit as st
import requests
import json
from datetime import datetime
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="MedIntel AI - Medical Report Analyzer",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Styling
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stTitle {
        color: #003366;
    }
    .metric-container {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 8px;
        margin-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Configuration
BACKEND_URL = "http://localhost:5000"
UPLOAD_ENDPOINT = f"{BACKEND_URL}/upload"

# Header
st.title("📋 MedIntel AI - Medical Report Analyzer")
st.markdown("Extract and analyze medical lab data from PDF reports")

# Sidebar
with st.sidebar:
    st.header("ℹ️ Instructions")
    st.markdown("""
    **How to use:**
    1. Upload a medical PDF report using the file uploader
    2. The system will extract text and parse medical metrics
    3. View the results including raw text and parsed values
    
    **Supported formats:**
    - Medical lab reports (CBC, CMP, etc.)
    - Scanned PDFs with clear text
    - Multi-page documents
    
    **Contact:**
    Backend: http://localhost:5000
    """)

# Main content
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("📤 Upload PDF Report")
    
    uploaded_file = st.file_uploader(
        "Choose a medical PDF file",
        type=['pdf'],
        help="Upload a PDF medical report for analysis"
    )
    
    if uploaded_file is not None:
        st.success(f"✓ File selected: {uploaded_file.name}")
        
        if st.button("🔄 Process & Extract", key="process_btn"):
            with st.spinner("Processing PDF..."):
                try:
                    # Prepare file for upload
                    files = {
                        'file': (
                            uploaded_file.name,
                            uploaded_file.getvalue(),
                            'application/pdf'
                        )
                    }
                    response = requests.post(UPLOAD_ENDPOINT, files=files, timeout=30)
                    
                    if response.status_code == 200:
                        result = response.json()
                        st.session_state.last_result = result
                        st.success("✓ Processing complete!")
                    else:
                        error_data = response.json()
                        st.error(f"❌ Error: {error_data.get('error', 'Unknown error')}")
                
                except requests.exceptions.ConnectionError:
                    st.error("❌ Cannot connect to backend. Is Flask running on http://localhost:5000?")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

# Display results if available
if 'last_result' in st.session_state:
    result = st.session_state.last_result
    
    st.markdown("---")
    st.subheader("📊 Analysis Results")
    
    # Metadata
    with st.expander("📄 File Information", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Filename", result.get('filename', 'N/A'))
        with col2:
            st.metric("Pages", result.get('metadata', {}).get('page_count', 'N/A'))
        with col3:
            st.metric("Text Length", f"{result.get('raw_text_length', 0)} chars")
    
    # Medical Metrics
    metrics = result.get('parsed_metrics', {})
    
    if metrics:
        st.subheader("🔬 Extracted Medical Metrics")
        
        # Create metrics table
        metrics_data = []
        for metric_name, metric_info in sorted(metrics.items()):
            if metric_info.get('found', False):
                metrics_data.append({
                    "Test": metric_name,
                    "Value": f"{metric_info['value']} {metric_info['unit']}",
                    "Reference Range": metric_info['normal_range'],
                    "Status": "✓ Found"
                })
        
        if metrics_data:
            df = pd.DataFrame(metrics_data)
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("No medical metrics detected in the PDF. Try uploading a lab report.")
    
    # Raw text preview
    with st.expander("📝 Raw Extracted Text (Preview)", expanded=False):
        st.text_area(
            "First 500 characters of extracted text:",
            value=result.get('raw_text', ''),
            height=200,
            disabled=True
        )
    
    # Download options
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📥 Download Metrics as JSON"):
            json_str = json.dumps(metrics, indent=2)
            st.download_button(
                label="Download JSON",
                data=json_str,
                file_name=f"metrics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
    
    with col2:
        if st.button("🔄 Reset & Upload Another"):
            st.session_state.last_result = None
            st.rerun()

else:
    # Empty state
    col1, col2, col3 = st.columns(3)
    with col2:
        st.info("👈 Upload a medical PDF to get started!")

# Footer
st.markdown("---")
st.caption(f"MedIntel AI v1.0 | Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
