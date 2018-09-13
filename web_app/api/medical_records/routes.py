from flask import Blueprint, jsonify, request
from sqlalchemy.orm import sessionmaker, load_only
from ..models.models import MedicalRecord
from ..models.schema import MedicalRecordSchema
from ..models.schema import ReportSchema
from ..models.schema import CategorySchema
from collections import Counter

module = Blueprint('api.medical_records', __name__)

medical_records_schema = MedicalRecordSchema(many=True)
medical_record_schema = MedicalRecordSchema()
report_schema = ReportSchema(many=True)
category_schema = CategorySchema(many=True)

@module.route('/', methods=['GET'])
def index():
    medical_records = MedicalRecord.query.all()
    medical_records, errors = medical_records_schema.dump(medical_records, many=True)
    return jsonify({'medical_records': medical_records})

@module.route('/<medical_record>', methods=['GET'])
def show(medical_record):
    medical_record = MedicalRecord.query.get(medical_record)
    if medical_record is None:
        return jsonify({'message': 'Medical record not found!'}), 400
    medical_record, errors = medical_record_schema.dump(medical_record)
    return jsonify({'medical_record': medical_record})
    
@module.route('/', methods=['PUT', 'POST'])
def store():
    json_data = request.get_json()
    medical_record = MedicalRecord()
    message = 'Medical record created'
    
    if not json_data:
        return jsonify({'message': 'No input data provided'}), 400

    if 'id' in json_data:
        message = 'Medical record updated'
        medical_record = MedicalRecord.query.get(json_data['id'])

    if medical_record is None:
        return jsonify({'message': 'Medical record not found!'}), 400
    
    if 'patient_id' in json_data:
        medical_record.patient_id = json_data['patient_id']

    medical_record.bmi = json_data['bmi']
    medical_record.bp = json_data['bp']
    medical_record.complaint = json_data['complaint']
    medical_record.diagnosis = json_data['diagnosis']
    medical_record.height = json_data['height']
    medical_record.note = json_data['note']
    medical_record.pr = json_data['pr']
    medical_record.temperature = json_data['temperature']
    medical_record.treatment = json_data['treatment']
    medical_record.medical_status = json_data['medical_status']
    medical_record.weight = json_data['weight']
    medical_record.save()

    medical_record, errors = medical_record_schema.dump(medical_record)

    return jsonify({'message': message, 'medical_record': medical_record})

@module.route('/<medical_record>', methods=['DELETE'])
def delete(medical_record):
    query = MedicalRecord.query.get(medical_record)
    if MedicalRecord is None:
        return jsonify({'message': 'MedicalRecord not found!'}), 400
    dump, errors = medical_record_schema.dump(query)
    session = sessionmaker().object_session(query)
    session.delete(query)
    session.commit()
    return jsonify({'message': 'Medical record deleted', 'medical_record': dump})

@module.route('/report', methods=['GET'])
def report():
    query = MedicalRecord().report()
    status = [
        {'category': 'EENT', 'medical_status': [
            {'name': 'nose bleeding', 'count': 0},
            {'name': 'redness of eye', 'count': 0},
            {'name': 'lip bleeding', 'count': 0}
        ]},
        {'category': 'CARDIO VASCULAR', 'medical_status': [
            {'name': 'chest pain', 'count': 0}
        ]},
        {'category': 'RESPIRATORY', 'medical_status': [
            {'name': 'colds', 'count': 0},
            {'name': 'cough', 'count': 0}
        ]},
        {'category': 'GASTROINTESTINAL', 'medical_status': [
            {'name': 'hyperacidity', 'count': 0},
            {'name': 'LBM', 'count': 0},
            {'name': 'stomachache', 'count': 0},
            {'name': 'vomiting', 'count': 0}
        ]},
        {'category': 'MUSCULOSKELETAL', 'medical_status': [
            {'name': 'body malaise', 'count': 0},
            {'name': 'muscle pain', 'count': 0}
        ]},
        {'category': 'DERMA', 'medical_status': [
            {'name': 'hypersensitivity', 'count': 0},
            {'name': 'insect bite', 'count': 0},
            {'name': 'blisters', 'count': 0}
        ]},
        {'category': 'SURGICAL', 'medical_status': [
            {'name': 'abrasion', 'count': 0}
        ]},
        {'category': 'DENTAL', 'medical_status': [
            {'name': 'toothache', 'count': 0},
            {'name': 'consultations', 'count': 0}
        ]},
        {'category': 'NEUROLOGICAL', 'medical_status': [
            {'name': 'dizziness', 'count': 0},
            {'name': 'fever', 'count': 0},
            {'name': 'headache', 'count': 0}
        ]},
        {'category': 'REPRODUCTIVE', 'medical_status': [
            {'name': 'dysmenorrhea', 'count': 0}
        ]},
        {'category': 'MISCELLANEOUS', 'medical_status': [
            {'name': 'BP TAKING', 'count': 0},
            {'name': 'OTHER CONSULTATIONS', 'count': 0}
        ]}
    ]

    for category in status:
            for count, name in query:
                for item in category['medical_status']:
                    print(item['name'], name)
                    if item['name'] == name:
                        item['count'] = count
                        continue

    dump, errors = category_schema.dump(status, many=True)
    return jsonify({'report': dump})
