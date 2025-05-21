user_prompt_template = """
Generate a detailed Scope of Work (SOW) for the following client and return the result as HTML.

### 🧾 Client Information:
{data}

---

### 🎨 Styling Instructions:
Include the following CSS styles in the HTML:
{sow_style_tag}

---

### 🖼️ Logo Placement:
Include the following <img> tag as the **first line inside the <body> tag**:
{img_tag_for_logo}

---

### 📄 Template Reference:
Use the following SOW template as the base structure:
{sow_template}

---

### ✅ Alignment Instructions:
To fill the "Alignment with Assessment" column, refer to this form:
{assessment_form_template}
"""
