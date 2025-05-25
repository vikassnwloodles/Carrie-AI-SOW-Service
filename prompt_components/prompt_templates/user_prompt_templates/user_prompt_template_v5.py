user_prompt_template = """
Generate a detailed Scope of Work (SOW) using the following JSON. Only return Markdown, no extra explanation.

### 🧾 JSON:

<JSON Begins>
{data}
<JSON Ends>

---

### 📄 Template Reference:
Use the following SOW Template as a structural guide only—don’t copy it verbatim. Instead, generate dynamic content using the provided JSON data, while ensuring that certain key elements like the document title and main section headings remain consistent with those in the original SOW template to maintain clarity and standardization.
I'm mentioning the document title and main section headings below for your reference.
Document Tilte:
# AI Audit/Readiness Assessment Statement of Work
Main Section Headings:
## 1. Objectives
## 2. Scope of Work
## 3. Methodology
## 4. Deliverables
## 5. Timeline & Responsibilities
## 6. Timeline Variability Notice
## 7. Budget & Compliance

Don't try to figure out the **Cost Estimate**. Instead, say—Budget will be determined based on platform licenses, configuration, and training needs. Don’t mention any tool/software name in the SOW. Instead, use the term "AI module(s)".
Render the following tables dynamically using JSON data and Assessment Form Template:
1. Table under the title "Platform Integration & Use Cases" (refer to the following SOW Template)
2. Table under the title "Timeline & Responsibilities" (refer to the following SOW Template)

<SOW Template Begins>
{sow_template}
<SOW Template Ends>

---

<Assessment Form Template Begins>
{assessment_form_template}
<Assessment Form Template Ends>
"""
