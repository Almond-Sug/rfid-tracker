from app import db, Part
from datetime import datetime, timedelta
from app import app  # make sure you're importing the Flask app too

with app.app_context():
    # Optional: clear old test parts
    Part.query.filter(Part.tag.in_(['PART-RECENT', 'PART-YELLOW', 'PART-RED'])).delete()

    # Create test parts
    part_recent = Part(
        tag='PART-RECENT',
        zone='Warehouse',
        subzone='A1',
        technician='Test',
        job_id='JOB-001',
        last_scanned=datetime.utcnow()
    )

    part_yellow = Part(
        tag='PART-YELLOW',
        zone='Warehouse',
        subzone='A1',
        technician='Test',
        job_id='JOB-002',
        last_scanned=datetime.utcnow() - timedelta(minutes=45)
    )

    part_red = Part(
        tag='PART-RED',
        zone='Warehouse',
        subzone='A1',
        technician='Test',
        job_id='JOB-003',
        last_scanned=datetime.utcnow() - timedelta(hours=3)
    )

    db.session.add_all([part_recent, part_yellow, part_red])
    db.session.commit()
    print("Test parts added.")
