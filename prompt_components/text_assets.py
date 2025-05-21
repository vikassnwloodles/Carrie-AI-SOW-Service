# LOADING ASSETS REQUIRED BY THE PROMPT
PROMPT_ASSETS_DIR = "prompt_components/prompt_assets"
sow_template = open(f"{PROMPT_ASSETS_DIR}/sow_template.md").read()
assessment_form_template = open(f"{PROMPT_ASSETS_DIR}/form_template.md").read()
twm_logo_url = "https://www.3rdwave-marketing.com/carrie-aigent-intake/public/images/logo.png"
img_tag_for_logo = f'<img src="{twm_logo_url}" alt="Company Logo" style="display: block; margin: 0 auto; max-width: 450px;" />'
sow_css = open(f"{PROMPT_ASSETS_DIR}/sow_style.css").read()
sow_style_tag = f"""
    <style>
        {sow_css}
    </style>
"""