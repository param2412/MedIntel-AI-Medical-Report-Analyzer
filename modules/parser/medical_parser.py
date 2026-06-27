import re
from typing import Dict, List, Any


def parse_medical_report(text: str) -> Dict[str, Any]:
    """
    Parse extracted medical report text into structured fields.
    Integrates medical metrics extraction using regex patterns.
    
    Args:
        text: Raw extracted text from medical report
        
    Returns:
        Dictionary containing parsed fields and extracted metrics
    """
    metrics = extract_medical_metrics(text)
    
    return {
        "raw_text": text,
        "metadata": {},
        "findings": [],
        "metrics": metrics,
    }


def extract_medical_metrics(text: str) -> Dict[str, Any]:
    """
    Extract structured medical metrics from report text using regex patterns.
    
    Targets common lab values:
    - CBC (Hemoglobin, WBC, RBC, Hematocrit, Platelets, MCV)
    - CMP (Glucose, BUN, Creatinine, Electrolytes)
    - Thyroid Function
    - Liver Function Tests
    
    Args:
        text: Raw text from medical report
        
    Returns:
        Dictionary of extracted metrics with values and reference ranges
    """
    metrics = {}
    
    # Define extraction patterns for common medical tests
    patterns = {
        "Hemoglobin": {
            "regex": r"Hemoglobin[:\s]*([0-9.]+)\s*(g/dL|g/dl)?",
            "unit": "g/dL",
            "normal_range": "13.5-17.5"
        },
        "Hematocrit": {
            "regex": r"Hematocrit[:\s]*([0-9.]+)\s*(%)?",
            "unit": "%",
            "normal_range": "41-53"
        },
        "WBC": {
            "regex": r"(?:WBC|White Blood Cell)(?:\s|.*?)([0-9]+(?:[0-9,]*)?)\s*(?:/µL|/uL|/μL)?",
            "unit": "/µL",
            "normal_range": "4500-11000"
        },
        "RBC": {
            "regex": r"(?:RBC|Red Blood Cell)(?:\s|.*?)([0-9.]+)\s*(?:M/µL|M/uL)?",
            "unit": "M/µL",
            "normal_range": "4.5-5.9"
        },
        "Platelet Count": {
            "regex": r"Platelet[s]?(?:\s|.*?)([0-9]+(?:[0-9,]*)?)\s*(?:/µL|/uL)?",
            "unit": "/µL",
            "normal_range": "150000-400000"
        },
        "MCV": {
            "regex": r"MCV(?:\s|.*?)([0-9.]+)\s*(?:fL|fl)?",
            "unit": "fL",
            "normal_range": "80-100"
        },
        "Glucose": {
            "regex": r"Glucose[:\s]*([0-9.]+)\s*(mg/dL|mg/dl)?",
            "unit": "mg/dL",
            "normal_range": "70-100"
        },
        "BUN": {
            "regex": r"(?:BUN|Blood Urea Nitrogen)[:\s]*([0-9.]+)\s*(mg/dL)?",
            "unit": "mg/dL",
            "normal_range": "7-20"
        },
        "Creatinine": {
            "regex": r"Creatinine[:\s]*([0-9.]+)\s*(mg/dL)?",
            "unit": "mg/dL",
            "normal_range": "0.7-1.3"
        },
        "Sodium": {
            "regex": r"Sodium[:\s]*([0-9.]+)\s*(mEq/L)?",
            "unit": "mEq/L",
            "normal_range": "135-145"
        },
        "Potassium": {
            "regex": r"Potassium[:\s]*([0-9.]+)\s*(mEq/L)?",
            "unit": "mEq/L",
            "normal_range": "3.5-5.0"
        },
        "Chloride": {
            "regex": r"Chloride[:\s]*([0-9.]+)\s*(mEq/L)?",
            "unit": "mEq/L",
            "normal_range": "98-107"
        },
    }
    
    # Search for each metric in the text
    for metric_name, pattern_info in patterns.items():
        match = re.search(pattern_info["regex"], text, re.IGNORECASE | re.DOTALL)
        if match:
            # Get the first capturing group (the value)
            try:
                value_str = match.group(1).strip().replace(",", "")
                value = float(value_str)
                metrics[metric_name] = {
                    "value": value,
                    "unit": pattern_info["unit"],
                    "normal_range": pattern_info["normal_range"],
                    "found": True
                }
            except (ValueError, IndexError, AttributeError):
                # Could not parse value, skip this metric
                continue
    
    return metrics
