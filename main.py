from fastapi import FastAPI, HTTPException, Request
from fastapi import Header, Depends
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from datetime import datetime
import uuid
import pypandoc
import os

from ai_logic import generate_sow
from utils import download_file
from consts import SERVICE_PROVIDER_LOGO_URL, ARTIFACTS_DIR
from assets.templates import LOGO_TEMPLATE, LOGO_TEMPLATE_MOD

from dotenv import load_dotenv

load_dotenv()


SECRET = os.environ.get("SECRET_KEY")

app = FastAPI()

# Mount the 'assets' folder at /assets
app.mount("/assets", StaticFiles(directory="assets"), name="assets")


def is_authenticated(x_webhook_secret: str = Header(...)):
    if x_webhook_secret != SECRET:
        raise HTTPException(status_code=403, detail="Forbidden: Invalid secret")


@app.post("/generate-sow")
async def generate_scope_of_work(request: Request, _: None = Depends(is_authenticated)):
    uuid4 = uuid.uuid4()

    try:
        json_data = await request.json()  # Accept dynamic form data
        sow_md = generate_sow(json_data)

        client_logo_url = ""
        if "logo_path" in json_data:
            # DOWNLOADING CLIENT LOGO
            client_logo_path = f"{ARTIFACTS_DIR}/client_logo_{uuid4}.png"
            client_logo_url = json_data["logo_path"]
            download_file(url=client_logo_url, filename=client_logo_path)

        # Adding logos on the top of `sow_md`
        sow_md_with_logos = (
            LOGO_TEMPLATE.format(SERVICE_PROVIDER_LOGO_URL, client_logo_url) + sow_md
        )

        # SAVING `sow_md` (WHICH IS IN Markdown FORMAT) TO A FILE (WILL READ LATER FOR HTML CONVERSION)
        os.makedirs(f"{ARTIFACTS_DIR}", exist_ok=True)
        sow_md_path = f"{ARTIFACTS_DIR}/sow_{uuid4}.md"
        open(sow_md_path, "w").write(sow_md)

        return {"sow": sow_md_with_logos, "uuid": uuid4}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Define request schema
class UUIDRequest(BaseModel):
    uuid: str


@app.post("/download-sow")
async def download_sow(data: UUIDRequest, _: None = Depends(is_authenticated)):
    uuid_str = data.uuid

    # Checking file existance
    md_path = f"{ARTIFACTS_DIR}/sow_{uuid_str}.md"
    if not os.path.exists(md_path):
        raise HTTPException(status_code=404, detail="Markdown file not found")

    docx_path = os.path.join(ARTIFACTS_DIR, f"sow_{uuid_str}.docx")

    client_logo_path = f"{ARTIFACTS_DIR}/client_logo_{uuid_str}.png"
    if not os.path.exists(client_logo_path):
        client_logo_path = ""

    sow_md_path = f"{ARTIFACTS_DIR}/sow_{uuid_str}.md"
    sow_md = open(sow_md_path).read()
    sow_md_with_logos = (
        LOGO_TEMPLATE_MOD.format(SERVICE_PROVIDER_LOGO_URL, client_logo_path) + sow_md
    )

    try:
        sow_html_with_logos = pypandoc.convert_text(
            sow_md_with_logos, "html", format="md"
        )
        pypandoc.convert_text(
            sow_html_with_logos, "docx", format="html", outputfile=docx_path
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Conversion failed: {e}")

    def stream_docx():
        with open(docx_path, "rb") as f:
            yield from f

    date_str = datetime.now().strftime('%Y%m%d')
    return StreamingResponse(
        stream_docx(),
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={
            f"Content-Disposition": f"attachment; filename=sow-by-3rdwave-marketing-{date_str}.docx"
        },
    )
