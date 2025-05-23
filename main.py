from fastapi import FastAPI, HTTPException, Header, Request
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uuid
import pypandoc
import os
import textwrap

from ai_logic import generate_sow

from dotenv import load_dotenv
load_dotenv()



SECRET = os.environ.get("SECRET_KEY")

app = FastAPI()

# Mount the 'assets' folder at /assets
app.mount("/assets", StaticFiles(directory="assets"), name="assets")



@app.post("/generate-sow")
async def generate_scope_of_work(request: Request, x_webhook_secret: str = Header(None)):
    uuid4 = uuid.uuid4()

    if x_webhook_secret != SECRET:
        raise HTTPException(status_code=403, detail="Forbidden: Invalid secret")
    
    try:
        json_data = await request.json()  # Accept dynamic form data
        sow_md = generate_sow(json_data)

        # Adding logos on the top of `sow_md`
        LOGOS = textwrap.dedent(f"""\
        <table width="100%" style="table-layout: fixed; border: none;">
            <colgroup>
                <col style="width: 50%;" />
                <col style="width: 50%;" />
            </colgroup>
            <tr>
                <td style="text-align: left;">
                    <img height="80" src="https://www.3rdwave-marketing.com/carrie-aigent-intake/public/images/logo.png" />
                </td>
                <td style="text-align: right;">
                    <img height="80" src="{json_data['logo_path']}" />
                </td>
            </tr>
        </table>


        """)
        sow_md = LOGOS + sow_md

        # SAVING `sow_md` (WHICH IS IN Markdown FORMAT) TO A FILE (WILL READ LATER FOR HTML CONVERSION)
        os.makedirs("artifacts", exist_ok=True)
        open(f"artifacts/sow_{uuid4}.md", "w").write(sow_md)

        return {"sow": sow_md, "uuid": uuid4}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



# Define request schema
class UUIDRequest(BaseModel):
    uuid: str


@app.post("/download-sow")
async def download_sow(data: UUIDRequest):
    uuid_str = data.uuid

    # Assuming HTML files are saved like: sow/<uuid>.html
    html_path = f"artifacts/sow_{uuid_str}.md"
    if not os.path.exists(html_path):
        raise HTTPException(status_code=404, detail="HTML file not found")

    # with tempfile.TemporaryDirectory() as tmpdir:
    # docx_path = os.path.join(tmpdir, f"{uuid_str}.docx")
    docx_path = os.path.join("artifacts", f"sow_{uuid_str}.docx")

    try:
        pypandoc.convert_file(html_path, 'docx', outputfile=docx_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Conversion failed: {e}")

    def stream_docx():
        with open(docx_path, "rb") as f:
            yield from f

    return StreamingResponse(
        stream_docx(),
        media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        headers={'Content-Disposition': f'attachment; filename=ScopeOfWork_{uuid_str}.docx'}
    )