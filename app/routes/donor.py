from fastapi import FastAPI, Path
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

donors = {
    1: {
        "name": "kyalo",
        "age": "10",
        "user_id": 1
    },
    2: {
        "name": "kamau",
        "age": "20",
        "user_id": 2
    },
    3: {
        "name": "kamene",
        "age": "30",
        "user_id": 3
    }
}


class Donor(BaseModel):
    name: str
    age: int
    user_id: int


class UpdateDonor(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    user_id: Optional[int] = None


@app.get("/")
def index():
    return {"name": "First Data"}


@app.get("/get-donor/{donor_id}")
def get_donor(donor_id: int = Path(..., description="The ID of the donor you want to view", gt=0)):
    return donors.get(donor_id, {"Data": "Not Found"})


@app.get("/get-by-name")
def get_donor(*, donor_id: int, name: Optional[str] = None, test: int):
    for donor_id in donors:
        if donors[donor_id]["name"] == name:
            return donors[donor_id]
    return {"Data": "Not Found"}


@app.post("/create-donor/{donor_id}")
def create_donor(donor_id: int, donor: Donor):
    if donor_id in donors:
        return {"Error": "Donor ID already exists"}
    donors[donor_id] = donor
    return donors[donor_id]


@app.put("/update-donor/{donor_id}")
def update_donor(donor_id: int, donor: Donor):
    if donor_id not in donors:
        return {"Error": "Donor ID does not exist"}

    if donor.name is not None:
        donors[donor_id]["name"] = donor.name

    if donor.age is not None:
        donors[donor_id]["age"] = donor.age

    if donor.user_id is not None:
        donors[donor_id]["user_id"] = donor.user_id

    donors[donor_id] = donor
    return donors[donor_id]


@app.delete("/delete-donor/{donor_id}")
def delete_donor(donor_id: int):
    if donor_id not in donors:
        return {"Error": "Donor ID does not exist"}
    del donors[donor_id]
    return {"Message": "Donor deleted successfully"}
