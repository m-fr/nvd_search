from itertools import filterfalse

from nvd_search.enums import Risk


def primary(metrics):
    m = list(filterfalse(lambda x: x['type'] != 'Primary', metrics))
    if not m:
        return metrics[0]
    else:
        return m[0]


def severity(metrics):
    risk = "none"
    if 'cvssMetricV31' in metrics:
        risk = primary(metrics['cvssMetricV31'])['cvssData']['baseSeverity']
    elif 'cvssMetricV30' in metrics:
        risk = primary(metrics['cvssMetricV30'])['cvssData']['baseSeverity']
    elif 'cvssMetricV2' in metrics:
        risk = primary(metrics['cvssMetricV2'])['baseSeverity']
    return Risk(risk.lower())
