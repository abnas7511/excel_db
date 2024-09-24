from flask import Flask, request, jsonify, send_from_directory
import pandas as pd
from db_config import UserInfo, session

app = Flask(__name__, instance_relative_config=True)


@app.route('/')
def index():
    return send_from_directory('templates','index.html')

#route for handling bulk entry
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and file.filename.endswith('.xlsx'):
        try:
            df = pd.read_excel(file)
            required_columns = ['User', 'Email ID', 'Role', 'Application Mapped', 'License Type']
            if not all(col in df.columns for col in required_columns):
                return jsonify({"error": "Missing required columns in the Excel file"}), 400
            users = []
            for index, row in df.iterrows():
                user = UserInfo(
                    user=row['User'],
                    emailid=row['Email ID'],
                    role=row['Role'],
                    application_mapped=row['Application Mapped'],
                    license_type=row['License Type']
                )
                users.append(user)
            session.bulk_save_objects(users)
            session.commit()
            return jsonify({"message": "Data uploaded and stored successfully"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "Invalid file format. Only .xlsx files are allowed"}), 400

#route for handling single entry
@app.route('/users', methods = ['POST'])
def insert_user():
    try:
        data = request.get_json()
        if not all(key in data for key in ['user','emailid','role','application_mapped','license_type']):
            return jsonify({"error": "Missing required fields"}), 400
        user = UserInfo(
            user=data['user'],
            emailid=data['emailid'],
            role=data['role'],
            application_mapped=data['application_mapped'],
            license_type=data['license_type']
        )
        session.add(user)
        session.commit()
        return jsonify({"message": "User added successfully","id": user.id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#route for deleting an entry
@app.route('/users/<int:id>',methods=['DELETE'])
def delete_user(id):
    try:
        user = session.query(UserInfo).filter_by(id=id).first()
        if user:
            session.delete(user)
            session.commit()
            return jsonify({"message": f"User with ID:{id}  deleted successfully"}), 200
        else:
            return jsonify({"error": f"User with ID:{id} not found"}), 404
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500

#route for updating an entry
@app.route('/users/<int:id>',methods =['PUT'])
def update_user(id):
    try:
        data = request.get_json()
        user = session.query(UserInfo).filter_by(id=id).first()
        if user:
            user.user = data.get('user',user.user)
            user.emailid = data.get('emailid',user.emailid)
            user.role = data.get('role',user.role)
            user.application_mapped = data.get('application_mapped',user.application_mapped)
            user.license_type = data.get('license_type',user.license_type)
            session.commit()
            return jsonify({"message": f"User with ID:{id} updated successfully"}), 200
        else:
            return jsonify({"error": f"User with ID:{id} not found"}), 404
    except Exception as e:
        return jsonify({"error":str(e)}),500

#route for getting all users
@app.route('/users', methods=['GET'])
def get_users():
    try:
        users = session.query(UserInfo).all()
        result = []
        for user in users:
            result.append({
                'user': user.user,
                'emailid': user.emailid,
                'role': user.role,
                'application_mapped': user.application_mapped,
                'license_type': user.license_type
            })
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
