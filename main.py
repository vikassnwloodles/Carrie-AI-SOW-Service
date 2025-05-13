from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from ai_logic import generate_sow

app = FastAPI()

class FormInput(BaseModel):
    company_name: str
    industry: str
    goals: str
    current_tools: str
    challenges: str
    timeline: str
    budget: str
    # Add other expected fields

@app.post("/generate-sow")
async def generate_scope_of_work(data: FormInput):
    try:
        print(f"{data=}")
        sow = generate_sow(data)
        return {"sow": sow}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
