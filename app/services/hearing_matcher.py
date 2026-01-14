from sqlalchemy.orm import Session
from app.models.meta import Stage

KEYWORD_MAP = {
    "mediation": ["mediation","counselling","settlement"],
    "evidence": ["evidence","affidavit","witness"],
    "arguments": ["argument","final hearing"],
    "interim": ["interim","maintenance","custody"],
    "judgment": ["judgment","order"]
}

def match_hearing(text: str, case_type: str, db: Session):

    text = text.lower()
    scores = {}

    for stage_slug, words in KEYWORD_MAP.items():
        for w in words:
            if w in text:
                scores[stage_slug] = scores.get(stage_slug,0)+1

    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    results = []

    for slug,_ in ranked[:3]:
        stage = db.query(Stage).filter(
            Stage.case_type_slug==case_type,
            Stage.slug==slug
        ).first()

        if stage:
            results.append(stage)

    return results
