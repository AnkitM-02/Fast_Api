from fastapi import FastAPI, Path, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated
import json

app = FastAPI()


class Patient(BaseModel):
    id: Annotated[str, Field(..., description='ID of the patient', examples=['P001'])]
    name: Annotated[str, Field(..., description='Name of the patient')]
    city: Annotated[str, Field(..., description='City where the patient lives')]
    age: Annotated[int, Field(..., gt=0, lt=120, description='Age of the patient')]
    gender: Annotated[str, Field(..., description='male, female or others')]
    height: Annotated[float, Field(..., gt=0, description='Height in metres')]
    weight: Annotated[float, Field(..., gt=0, description='Weight in kg')]

    @computed_field
    @property
    def bmi(self) -> float:
        return round(self.weight / (self.height ** 2), 2)

    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return "Underweight"
        elif self.bmi < 25:
            return "Normal"
        elif self.bmi < 30:
            return "Overweight"
        else:
            return "Obese"


def load_data():
    with open('patient.json', 'r') as f:
        data = json.load(f)
    return data


def save_data(data):
    with open('patient.json', 'w') as f:
        json.dump(data, f)


@app.get("/")
def read_root():
    return {"message": "patient management system"}


@app.get("/ankit")
def ankit():
    return {"important": "fully manageable system"}


@app.get("/view")
def view():
    values = load_data()
    return values


@app.get("/patient/{patient_id}")
def patient_details(
    patient_id: str = Path(..., description="ID of patient", examples=["P001"])
):
    values = load_data()
    if patient_id in values:
        return values[patient_id]
    raise HTTPException(status_code=404, detail="patient not found")


@app.post('/create')
def create_patient(patient: Patient):

    # load existing data
    data = load_data()

    # check if the patient already exists
    if patient.id in data:
        raise HTTPException(status_code=400, detail='Patient already exists')

    # add the new patient (id is the key, so exclude it from the value)
    data[patient.id] = patient.model_dump(exclude=['id'])

    # save into the json file
    save_data(data)

    return JSONResponse(status_code=201, content={'message': 'Patient created successfully'})