from .text_assets import (
    sow_style_tag,
    logo_md,
    sow_template,
    assessment_form_template,
)
from .prompt_templates.system_prompt_templates.system_prompt_template_v1 import (
    system_prompt_template,
)
from .prompt_templates.user_prompt_templates.user_prompt_template_v5 import (
    user_prompt_template,
)


def get_system_prompt(data=None):
    system_prompt = system_prompt_template

    return system_prompt


def get_user_prompt(data):
    user_prompt = user_prompt_template.format(
        data=data,
        sow_style_tag=sow_style_tag,
        logo_md=logo_md,
        sow_template=sow_template,
        assessment_form_template=assessment_form_template,
    )

    return user_prompt
