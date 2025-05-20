from fastapi import FastAPI, HTTPException, Header, Depends, Request
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import List, Optional
from auth import create_access_token, verify_token
from ai_logic import generate_sow
from dotenv import load_dotenv
import os
load_dotenv()

SECRET = os.environ.get("SECRET_KEY")

JWT_LOGIN_CREDS = {"username": os.environ.get("JWT_USERNAME"), 
                   "password": os.environ.get("JWT_PASSWORD")}

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class FormInput(BaseModel):
    organization_name: str
    director_name: str
    email: str
    phone: str
    address: str
    city: str
    state: str
    zip_code: str
    is_501c3: bool
    is_for_profit: bool
    annual_budget: str
    ein: Optional[str]
    narrative: str
    services: str
    vision_mission: str
    website: Optional[str]
    logo_path: Optional[str]
    ai_goals: Optional[List[str]]
    ai_pain_points: Optional[str]
    leadership_commitment: Optional[str]
    ai_metrics: Optional[List[str]]
    ai_budget: Optional[str]
    ownership_cost: Optional[str]
    target_clients: Optional[List[str]]
    service_type: Optional[str]
    follow_up_methods: Optional[List[str]]
    data_sources: Optional[List[str]]
    data_quality: Optional[str]
    data_governance: Optional[str]
    infrastructure_support: Optional[str]
    system_integration: Optional[str]
    data_security: Optional[str]
    privacy_assessment: Optional[str]
    ai_experience: Optional[str]
    ai_champions: Optional[str]
    change_management: Optional[str]
    resistance_plan: Optional[str]
    workflow_mapping: Optional[str]
    process_flexibility: Optional[str]
    ai_business_functions: Optional[List[str]]
    identified_use_cases: Optional[str]
    use_case_metrics: Optional[List[str]]
    customer_impact: Optional[str]
    customer_feedback: Optional[str]
    competitor_usage: Optional[str]
    ai_urgency: Optional[str]
    ethical_guidelines: Optional[str]
    transparency_importance: Optional[str]
    ai_transparency: Optional[str]
    ai_risks: Optional[str]
    failure_plan: Optional[str]
    ai_timeline: Optional[str]
    timeline_flexibility: Optional[str]
    tech_partners: Optional[str]
    vendor_expertise: Optional[str]
    ai_kpis: Optional[str]
    ai_success_definition: Optional[str]



# @app.post("/token")
# def login(form_data: OAuth2PasswordRequestForm = Depends()):
#     if form_data.username != JWT_LOGIN_CREDS["username"] or form_data.password != JWT_LOGIN_CREDS["password"]:
#         raise HTTPException(status_code=400, detail="Invalid credentials")
#     access_token = create_access_token(data={"sub": form_data.username})
#     return {"access_token": access_token, "token_type": "bearer"}


# Dependency to protect routes
def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    return payload["sub"]


# @app.post("/generate-sow")
# async def generate_scope_of_work(data: FormInput, user: str = Depends(get_current_user)):
#     try:
#         print(f"func:generate_scope_of_work>{data=}")
#         sow = generate_sow(data)
#         return {"sow": sow}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-sow")
# async def generate_scope_of_work(data: FormInput, x_webhook_secret: str = Header(None)):
async def generate_scope_of_work(request: Request, x_webhook_secret: str = Header(None)):
    if x_webhook_secret != SECRET:
        raise HTTPException(status_code=403, detail="Forbidden: Invalid secret")
    
    try:
        # print(f"func:generate_scope_of_work>{data=}")
        # sow = generate_sow(data)
        # return {"sow": sow}
        form_data = await request.form()  # Accept dynamic form data
        data_dict = dict(form_data)  # Convert from MultiDict to plain dict
        sow = generate_sow(data_dict)
        return {"sow": sow}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

