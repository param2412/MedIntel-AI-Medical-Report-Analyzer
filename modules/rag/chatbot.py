# from typing import List


# def generate_response(query: str, context: List[str]) -> str:
#     """Generate a chatbot response using retrieved document context."""
#     return ""  # TODO: integrate RAG response generation


from typing import Dict, Any
import re


def _parse_range(range_str: str):
    """Attempt to parse a simple numeric range 'min - max' from a string."""
    if not range_str or not isinstance(range_str, str):
        return None
    m = re.search(r"([0-9]*\.?[0-9]+)\s*-\s*([0-9]*\.?[0-9]+)", range_str)
    if m:
        try:
            low = float(m.group(1))
            high = float(m.group(2))
            return low, high
        except ValueError:
            return None
    return None


def _to_float(value):
    try:
        return float(value)
    except Exception:
        return None


def answer_question_from_metrics(question: str, metrics: Dict[str, Any], raw_text: str) -> str:
    """
    Simple rule-based responder:
    - If question mentions a metric name (case-insensitive): return its value, unit, ref range and interpretation.
    - If question is generic (contains 'summary' or 'what does' or 'interpret'): return a short summary using metrics and top lines from raw_text.
    - Otherwise: return a fallback listing available metrics.
    """
    if not question:
        return "No question provided."

    q = question.lower().strip()

    # Normalize metric keys to map lowercase -> original name
    metric_map = {k.lower(): k for k in (metrics or {}).keys()}

    # 1) Metric-specific question: check if any metric name appears in the question
    for m_lower, m_orig in metric_map.items():
        if m_lower in q:
            info = metrics.get(m_orig, {}) or {}
            val = info.get("value", "N/A")
            unit = info.get("unit", "")
            ref = info.get("normal_range", "N/A")

            # Determine interpretation if possible
            interpretation = "Unknown"
            numeric_val = _to_float(val)
            parsed_range = None
            if isinstance(ref, (list, tuple)) and len(ref) == 2:
                try:
                    parsed_range = (float(ref[0]), float(ref[1]))
                except Exception:
                    parsed_range = None
            elif isinstance(ref, str):
                parsed_range = _parse_range(ref)

            if numeric_val is not None and parsed_range is not None:
                low, high = parsed_range
                if numeric_val < low:
                    interpretation = "Low"
                elif numeric_val > high:
                    interpretation = "High"
                else:
                    interpretation = "Normal"

            return (
                f"{m_orig}: {val} {unit}".strip()
                + f"\nReference range: {ref}"
                + f"\nInterpretation: {interpretation}"
            )

    # 2) Generic summary / interpret request
    if any(tok in q for tok in ("summary", "what does", "interpret")):
        lines = []
        if raw_text:
            for l in (raw_text or "").splitlines():
                l = l.strip()
                if l:
                    lines.append(l)
                if len(lines) >= 3:
                    break
        top_text = " ".join(lines)[:400]

        # Build succinct metrics summary
        if metrics:
            parts = []
            for k, v in (metrics or {}).items():
                value = v.get("value", "N/A") if isinstance(v, dict) else v
                unit = v.get("unit", "") if isinstance(v, dict) else ""
                parts.append(f"{k}: {value} {unit}".strip())
            metrics_summary = "; ".join(parts[:8])
            return f"Summary: {metrics_summary}\n\nTop context: {top_text}"
        else:
            return f"No structured metrics found. Top context: {top_text}"

    # 3) Fallback: list available metrics
    if metrics:
        available = ", ".join(sorted(metrics.keys()))
        return f"I couldn't find a specific metric in your question. Available metrics: {available}"
    else:
        return "No medical metrics are available from this report. Please provide a lab report containing measurable metrics."