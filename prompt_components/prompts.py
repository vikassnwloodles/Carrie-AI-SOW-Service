from .text_assets import (
    sow_style_tag,
    img_tag_for_logo,
    sow_template,
    assessment_form_template,
)


def get_system_prompt(data=None):
    system_prompt = "You are a helpful AI consultant."

    return system_prompt


def get_user_prompt(data):
    user_prompt = f"""
        Generate a detailed Scope of Work (SOW) for the following client and return as HTML:
        {data}

        The generated HTML must include the following styles:
        {sow_style_tag}

        The generated HTML must include the following <img> tag as the first line inside the <body> tag:
        {img_tag_for_logo}

        Use the following SOW template for reference:
        {sow_template}

        To fill "Alignment with Assessment" column, refer to the following form:
        {assessment_form_template}
        """

    return user_prompt
