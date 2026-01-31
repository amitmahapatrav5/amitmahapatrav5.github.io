from yaml import safe_load
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape


def render(json_file: Path, template_file: Path, output_file: Path):
    data = {}
    with json_file.open() as f:
        data = safe_load(f)

    projects = data.get("projects", [])
    experience = data.get("experience", [])

    projects_by_org = {}

    for project in projects:
        org = project.get("organization")
        name = project.get("name")

        if not org or not name:
            continue

        projects_by_org.setdefault(org, []).append({ #type: ignore
            "name": name,
            "url": project.get("url", "")
        })


    for exp in experience:
        org = exp.get("organization")

        if not org:
            exp["computed_highlights"] = []
            continue

        exp["computed_highlights"] = projects_by_org.get(org, []) # type: ignore

    env = Environment(
        loader=FileSystemLoader(str(template_file.parent)),
        autoescape=select_autoescape(['html','xml'])
    )
    tmpl = env.get_template(template_file.name)

    rendered = tmpl.render(resume=data)
    with output_file.open("w", encoding="utf-8") as out:
        out.write(rendered)


if __name__ == "__main__":
    json_file = Path().cwd() / 'resume-wip.yaml'

    pdf_template_file = Path().cwd() / 'pdf_template_wip.html'
    pdf_output_file = Path().cwd() / 'resume.pdf.html'
    render(json_file, pdf_template_file, pdf_output_file)