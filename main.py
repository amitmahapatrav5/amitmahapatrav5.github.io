import json
from jinja2 import Template

def load_resume_data(json_file_path="resume.json"):
    """Load resume data from JSON file"""
    try:
        with open(json_file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: {json_file_path} not found!")
        return None
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return None

def generate_resume(resume_data, template_path="template.html", output_path="index.html"):
    """Generate HTML resume from template and data"""
    try:
        # Load template
        with open(template_path, 'r', encoding='utf-8') as file:
            template_content = file.read()

        template = Template(template_content)

        # Render template with data
        html_content = template.render(resume=resume_data)

        # Write output
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(html_content)

        print(f"Resume generated successfully: {output_path}")
        return True
    except FileNotFoundError as e:
        print(f"Error: Template file not found - {e}")
        return False
    except Exception as e:
        print(f"Error generating resume: {e}")
        return False

def main():
    """Main function to run the resume generator"""
    print("Resume Generator Starting...")

    # Load resume data
    resume_data = load_resume_data()
    if not resume_data:
        return

    # Generate resume
    success = generate_resume(resume_data)
    if success:
        print("Resume generation completed!")
        print("Open resume.html in your browser to view the result.")
    else:
        print("Failed to generate resume.")

if __name__ == "__main__":
    main()
