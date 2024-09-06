# Flask File Upload and Storage

This project is a simple Flask application that allows users to upload Excel files and stores their data in a PostgreSQL database. It uses SQLAlchemy for ORM and `pandas` to process Excel files.

## Features

- **File Upload:** Users can upload `.xlsx` files.
- **Data Processing:** The application reads the Excel file and converts it to a CSV format in memory.
- **Database Storage:** File information and data are stored in a PostgreSQL database.

## Prerequisites

- Python 3.6+
- PostgreSQL
- Flask
- SQLAlchemy
- pandas
- python-dotenv

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/abnas7511/excel_db.git
    cd your-repo
    ```

2. **Create a virtual environment and activate it:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required packages:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Create a `.env` file in the root directory with the following content:**

    ```env
    POSTGRES_USER=your_postgres_user
    POSTGRES_PASSWORD=your_postgres_password
    POSTGRES_HOST=localhost
    POSTGRES_PORT=5432
    POSTGRES_DB=your_database_name
    ```

## Usage

1. **Run the Flask application:**

    ```bash
    python app.py
    ```

2. **Upload a file using a POST request to `/upload`:**

    You can use tools like `curl` or Postman to upload your `.xlsx` file.

    Example using `curl`:

    ```bash
    curl -X POST -F "file=@path/to/your/file.xlsx" http://localhost:5000/upload
    ```

## Code Explanation

- **Flask Application:** Handles file uploads and error responses.
- **SQLAlchemy Models:** Defines the `FileInfo` table to store file information and data.
- **File Handling:** Reads the uploaded Excel file and converts it to CSV format before storing it in the database.

## Contributing

Feel free to open issues or submit pull requests for enhancements or bug fixes.

## License

This project is licensed under the MIT License.

---
