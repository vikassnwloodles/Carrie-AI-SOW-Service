from fastapi import FastAPI, HTTPException, Header, Request
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uuid
import pypandoc
import os
import textwrap

from ai_logic import generate_sow
from utils import download_file
from consts import SERVICE_PROVIDER_LOGO_PATH, ARTIFACTS_DIR

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

        # # Adding logos on the top of `sow_md`
        # LOGOS = textwrap.dedent(f"""\
        # <table width="100%" style="table-layout: fixed; border: none;">
        #     <colgroup>
        #         <col style="width: 50%;" />
        #         <col style="width: 50%;" />
        #     </colgroup>
        #     <tr>
        #         <td style="text-align: left;">
        #             <img height="80" src="https://www.3rdwave-marketing.com/carrie-aigent-intake/public/images/logo.png" />
        #         </td>
        #         <td style="text-align: right;">
        #             <img height="80" src="{json_data['logo_path']}" />
        #         </td>
        #     </tr>
        # </table>


        # """)
        
        # DOWNLOADING CLIENT LOGO
        client_logo_path = f"{ARTIFACTS_DIR}/client_logo_{uuid4}.png"
        download_file(url=json_data['logo_path'], filename=client_logo_path)

        # Adding logos on the top of `sow_md`
        LOGO_TEMPLATE = textwrap.dedent(f"""\
        <p>
            <img src="{SERVICE_PROVIDER_LOGO_PATH}" style="float: left; height: 80px; display: block;" />
            <img src="{client_logo_path}" style="float: right; height: 80px; display: block;" />
        </p>
        <br clear="both">
        <br>
        
        """)

        sow_md_with_logos = LOGO_TEMPLATE + sow_md

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
async def download_sow(data: UUIDRequest):
    uuid_str = data.uuid

    # Checking file existance
    md_path = f"{ARTIFACTS_DIR}/sow_{uuid_str}.md"
    if not os.path.exists(md_path):
        raise HTTPException(status_code=404, detail="Markdown file not found")

    docx_path = os.path.join(ARTIFACTS_DIR, f"sow_{uuid_str}.docx")
    client_logo_path = f"{ARTIFACTS_DIR}/client_logo_{uuid_str}.png"

    # REPLACE `LOGO_TEMPLATE` WITH THE FOLLOWING ONE
    LOGO_TEMPLATE_MOD = textwrap.dedent(f"""\
    <table width="100%" style="table-layout: fixed; border: none;">
        <colgroup>
            <col style="width: 50%;" />
            <col style="width: 50%;" />
        </colgroup>
        <tr>
            <td style="text-align: left;">
                <img height="80" src="{SERVICE_PROVIDER_LOGO_PATH}" />
            </td>
            <td style="text-align: right;">
                <img height="80" src="{client_logo_path}" />
            </td>
        </tr>
    </table>
    <br>
    
    """)

    sow_md_path = f"{ARTIFACTS_DIR}/sow_{uuid_str}.md"
    sow_md = open(sow_md_path).read()
    sow_md_with_logos = LOGO_TEMPLATE_MOD + sow_md

    try:
        sow_html_with_logos = pypandoc.convert_text(sow_md_with_logos, 'html', format="md")
        pypandoc.convert_text(sow_html_with_logos, 'docx', format="html", outputfile=docx_path)
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