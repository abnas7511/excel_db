from flask import Flask, request, jsonify
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, LargeBinary
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv
import os

app = Flask(__name__, instance_relative_config=True)

load_dotenv()

# Connection details
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_HOST = os.getenv('POSTGRES_HOST')
POSTGRES_PORT = os.getenv('POSTGRES_PORT')
POSTGRES_DB = os.getenv('POSTGRES_DB')

# PostgreSQL connection string
DATABASE_URL = f'postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'
engine = create_engine(DATABASE_URL, echo=True, pool_size=5, max_overflow=10)
Base = declarative_base()

# FileInfo table definition
class FileInfo(Base):
    __tablename__ = 'file_info'
    id = Column(Integer, primary_key=True)
    filename = Column(String, nullable=False)
    file_data = Column(LargeBinary, nullable=False)

# Creating the table
Base.metadata.create_all(engine)

# Creating a session
Session = sessionmaker(bind=engine)
session = Session()

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and file.filename.endswith('.xlsx'):
        try:
            # Reading the Excel file
            df = pd.read_excel(file)

            # Convert DataFrame to bytes
            file_data = df.to_csv(index=False).encode('utf-8')

            # Store the file info in the database
            file_info = FileInfo(filename=file.filename, file_data=file_data)
            session.add(file_info)
            session.commit()

            return jsonify({"message": "File uploaded and stored successfully"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "Invalid file format. Only .xlsx files are allowed"}), 400

if __name__ == '__main__':
    app.run(debug=True)
