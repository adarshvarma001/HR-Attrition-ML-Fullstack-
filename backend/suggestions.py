from typing import Dict

def suggestions_for_row(row: Dict) -> str:
    suggestions = []
    ot = str(row.get('OverTime', '')).lower()
    if ot.startswith('y') or ot in ['yes','true','1']:
        suggestions.append("Reduce overtime / offer flexible hours")

    try:
        if int(row.get('MonthlyIncome', 0)) < 3000:
            suggestions.append("Consider a salary review / retention bonus")
    except Exception:
        pass

    try:
        if int(row.get('WorkLifeBalance', 3)) <= 2:
            suggestions.append("Improve work-life balance (remote days / flexible schedule)")
    except Exception:
        pass

    try:
        if int(row.get('YearsSinceLastPromotion', 0)) >= 4:
            suggestions.append("Offer career progression/promotion or targeted training")
    except Exception:
        pass

    try:
        if int(row.get('DistanceFromHome', 0)) >= 20:
            suggestions.append("Consider remote or relocation support")
    except Exception:
        pass

    if not suggestions:
        suggestions.append("Manager check-in and engagement survey")

    return "; ".join(suggestions)
