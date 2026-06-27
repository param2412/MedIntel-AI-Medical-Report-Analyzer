#!/usr/bin/env python
"""Quick test script for PDF extraction and medical metrics parsing."""

from modules.ocr.pdf_extractor import extract_text_from_pdf
from modules.parser.medical_parser import parse_medical_report

# Extract and parse
text = extract_text_from_pdf('data/uploaded_reports/sample_report.pdf')
parsed = parse_medical_report(text)

print("=" * 60)
print("EXTRACTED TEXT (First 400 chars)")
print("=" * 60)
print(text[:400])
print()
print("=" * 60)
print("PARSED MEDICAL METRICS")
print("=" * 60)

metrics = parsed['metrics']
found_metrics = {k: v for k, v in sorted(metrics.items()) if v.get('found')}

if found_metrics:
    for name, info in found_metrics.items():
        print(f"✓ {name}: {info['value']} {info['unit']} (ref: {info['normal_range']})")
else:
    print("No metrics found")

print()
print(f"Total metrics extracted: {len(found_metrics)}")
