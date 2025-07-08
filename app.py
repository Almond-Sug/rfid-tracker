# app.py
from flask import Flask, request, jsonify, render_template, Response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import csv
from collections import defaultdict
from statistics import mean


app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'rfid.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Part(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(64), unique=True, nullable=False)
    zone = db.Column(db.String(64))
    subzone = db.Column(db.String(64))
    last_scanned = db.Column(db.DateTime, default=datetime.utcnow)
    technician = db.Column(db.String(64))
    job_id = db.Column(db.String(64))

    def to_dict(self):
        return {
            'tag': self.tag,
            'zone': self.zone,
            'subzone': self.subzone,
            'last_scanned': self.last_scanned.isoformat() + 'Z',
            'technician': self.technician,
            'job_id': self.job_id
        }
        
class ScanLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    part_id = db.Column(db.Integer, db.ForeignKey('part.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    zone = db.Column(db.String(64))
    subzone = db.Column(db.String(64))
    technician = db.Column(db.String(64))
    job_id = db.Column(db.String(64))


with app.app_context():
    db.create_all()

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/simulate')
def simulate():
    return render_template('simulate.html')

@app.route('/new-part')
def new_part():
    return render_template('new_part.html')

@app.route('/history/<tag>')
def scan_history(tag):
    part = Part.query.filter_by(tag=tag).first_or_404()
    logs = ScanLog.query.filter_by(part_id=part.id).order_by(ScanLog.timestamp.desc()).all()
    return render_template('history.html', part=part, logs=logs)


@app.route('/api/parts', methods=['GET'])
def get_parts():
    zone_filter = request.args.get('zone')
    job_filter = request.args.get('job_id')
    query = Part.query
    if zone_filter:
        query = query.filter_by(zone=zone_filter)
    if job_filter:
        query = query.filter_by(job_id=job_filter)
    parts = query.all()
    return jsonify([p.to_dict() for p in parts])

@app.route('/api/parts/<tag>', methods=['DELETE'])
def delete_part(tag):
    part = Part.query.filter_by(tag=tag).first()
    if part:
        db.session.delete(part)
        db.session.commit()
        return jsonify({'message': 'Part deleted'}), 200
    return jsonify({'error': 'Part not found'}), 404

@app.route('/api/summary')
def summary():
    zones = ['Receiving', 'Warehouse', 'Machine Shop', 'Shipping']
    counts = {zone: Part.query.filter_by(zone=zone).count() for zone in zones}
    return jsonify(counts)

@app.route('/api/zone-times')
def zone_times():
    logs = ScanLog.query.order_by(ScanLog.part_id, ScanLog.timestamp).all()
    times_by_zone = defaultdict(list)
    last_seen = {}

    for log in logs:
        if log.part_id in last_seen:
            prev = last_seen[log.part_id]
            delta = (log.timestamp - prev['timestamp']).total_seconds() / 60  # in minutes
            times_by_zone[prev['zone']].append(delta)
        last_seen[log.part_id] = {'timestamp': log.timestamp, 'zone': log.zone}

    avg_times = {zone: round(mean(times), 1) for zone, times in times_by_zone.items() if times}
    return jsonify(avg_times)

@app.route('/export-csv')
def export_csv():
    zone = request.args.get('zone')
    job_id = request.args.get('job_id')

    query = Part.query
    if zone:
        query = query.filter_by(zone=zone)
    if job_id:
        query = query.filter_by(job_id=job_id)
    parts = query.all()

    def generate():
        yield 'Tag,Zone,Subzone,Last Scanned,Technician,Job ID\n'
        for part in parts:
            yield f"{part.tag},{part.zone},{part.subzone},{part.last_scanned.isoformat()},{part.technician},{part.job_id}\n"

    return Response(generate(), mimetype='text/csv',
                    headers={"Content-Disposition": "attachment;filename=rfid_export.csv"})

@app.route('/api/scan', methods=['POST'])
def scan_part():
    data = request.json
    tag = data.get('tag')
    zone = data.get('zone')
    subzone = data.get('subzone')
    technician = data.get('technician')
    job_id = data.get('job_id')

    part = Part.query.filter_by(tag=tag).first()
    if not part:
        part = Part(tag=tag)
        db.session.add(part)

    part.zone = zone
    part.subzone = subzone
    part.technician = technician
    part.job_id = job_id
    part.last_scanned = datetime.utcnow()
    log = ScanLog(
    part_id=part.id,
    zone=zone,
    subzone=subzone,
    technician=technician,
    job_id=job_id
    )
    db.session.add(log)
    db.session.commit()
    return jsonify({'message': 'Scan recorded'}), 200

if __name__ == '__main__':
    app.run(debug=True)
