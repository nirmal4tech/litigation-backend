from app.models.diary import DiaryEntry
from app.models.hearing import HearingEntry
from app.models.cost import CostEntry
from app.models.retention import DataRetentionLog

def archive_old_entries(db, user_id, case_id, days=30):

    db.query(DiaryEntry)\
      .filter(DiaryEntry.case_id==case_id)\
      .filter(DiaryEntry.is_archived==False)\
      .update({"is_archived":True})

    db.add(DataRetentionLog(
        user_id=user_id,
        action="archived",
        target=f"case:{case_id}"
    ))

    db.commit()
