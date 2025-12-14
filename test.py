from yaml import safe_load
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape


def render(json_file, template_file, output_file):
    json_file = Path(json_file)
    template_file = Path(template_file)
    output_file = Path(output_file)
    data = {}
    with json_file.open() as f:
        data = safe_load(f)
    env = Environment(
        loader=FileSystemLoader(str(template_file.parent)),
        autoescape=select_autoescape(['html','xml'])
    )
    tmpl = env.get_template(template_file.name)
    
    rendered = tmpl.render(resume=data)
    with output_file.open("w", encoding="utf-8") as out:
        out.write(rendered)
    print(f"Rendered {output_file}")

if __name__ == "__main__":
    json_file = Path().cwd() / 'resume-wip.yaml'

    html_template_file = Path().cwd() / 'html_template.html'
    html_output_file = Path().cwd() / 'index.html'
    render(json_file, html_template_file, html_output_file)

    pdf_template_file = Path().cwd() / 'pdf_template.html'
    pdf_output_file = Path().cwd() / 'resume.pdf.html'
    render(json_file, pdf_template_file, pdf_output_file)