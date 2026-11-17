# Fast_Api

A small patient management API built with FastAPI. It can list patient records, look up a record by ID, and create a record.

## Setup on Windows PowerShell

From the project folder, create and activate a virtual environment, then install the dependencies:

```powershell
python -m venv myenv
.\myenv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Create your local data file from the example:

```powershell
Copy-Item patient.example.json patient.json
```

`patient.json` is ignored by Git so local patient data is not pushed to the public repository. Use only fictional sample records in any data you choose to publish.

## Run the API

```powershell
python -m uvicorn main:app --reload
```

Open <http://127.0.0.1:8000/> for the root response or <http://127.0.0.1:8000/docs> for the interactive API documentation.

## Endpoints

- `GET /` — API welcome message
- `GET /view` — list patient records
- `GET /patient/{patient_id}` — look up a patient by ID
- `POST /create` — add a patient record
