#  Project:  ResumeCoverLetterGenerator
#  Author:   Samrat Baral

#  MIT License

#  Copyright (c) 2024 Samrat Baral

#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:

#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.

#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.

import json
import subprocess

# Path to your JSON file
json_filepath = 'resume.json'

def load_resume_data(json_filepath):
    with open(json_filepath, 'r') as file:
        resume_data = json.load(file)
    return resume_data

# Load the resume data from the JSON file
resume_data = load_resume_data(json_filepath)

def generate_latex(resume_data):
  # Start of the LaTeX document, correctly treated as a raw string
  latex_content = r"""
\documentclass[a4paper,10pt]{article}
\usepackage[left=0.35in,top=0.5in,right=0.25in,bottom=0.6in]{geometry}
\usepackage{hyperref}
\usepackage{fontawesome5}
\begin{document}

% Custom commands
\newcommand{\Name}[1]{{\Huge #1}}
\newcommand{\Phone}[1]{{ \faPhone\ #1}}
\newcommand{\Email}[1]{{ \faEnvelope\  #1}}
\newcommand{\Address}[1]{{ \faMapPin\ #1}}
\newcommand{\GitHubURL}[1]{{\faGithub\ #1}}
\newcommand{\LinkedInURL}[1]{{\faLinkedin\ #1}}

"""
  # Ensure all subsequent string additions are correctly handled
  # Example of adding personal information as raw strings
  pi = resume_data['personalInformation']
  latex_content += rf"\Name{{{pi['fullName']}}}" + "\n"
  latex_content += rf"\Email {{{pi['email']}}}" + "\n"
  latex_content += rf"\Phone {{{pi['phone']}}}" + "\n"
  latex_content += rf"\Address {{{pi['address']}}}" + "\n"
  latex_content += "\n"
  latex_content += rf"\GitHubURL {{{pi['githubUsername']}}}" + "\n"
  latex_content += rf"\LinkedInURL {{{pi['linkedinUsername']}}}" + "\n"


# {\href{https://www.linkedin.com/in/username/}{\faLinkedin\ username}}
  # And so on for the rest of the document content...


  # Skills
  latex_content += r"\section*{Skills}"
  for cat, skills in resume_data["skillsAndAbilities"].items():
    latex_content += f"\\textbf{{{cat}}}: "
    latex_content += f"{','.join(skills)} \\\\ \n"
    # latex_content += "\n"

  # Work Experience
  latex_content += r"\section*{Work Experience}"
  for exp in resume_data["workExperience"]:
    latex_content += f"{exp['positionOrRole']} at {exp['projectName']} \\ {exp['location']} \\ {exp['website']} \ {exp['duration']} \\\\ \n"
    for ach in exp["achievements"]:
      latex_content += f"- {ach} \\\\ \n"


  # Projects
  latex_content += r"\section*{Projects}"
  for proj in resume_data["projects"]:
    latex_content += f"{proj['name']} \\ {proj['description']} \\ {proj['githubLink']} \\\\ \n"

  # Leadership Roles , Awards and Volunteer Experience
  latex_content += r"\section*{Leadership Roles}"
  for role in resume_data["leadershipRolesAndAwards"]:
    latex_content += f"{role['event']} at {role['placement']} \\ {role['participants']} {role['gamesWon']}\\\\ \n"

  # Education
  latex_content += r"\section*{Education}"
  for edu in resume_data["educationAndCertification"]:
    latex_content += f"{edu['degree']} in {edu['field']} \\ {edu['institution']} \\ {edu['location']} \\ {edu['duration']} \\\\ \n"

  # Close the document
  latex_content += r"\end{document}"

  return latex_content

# Generate LaTeX content
latex_content = generate_latex(resume_data)

# Save to .tex file
tex_filename = "resume.tex"
with open(tex_filename, "w") as tex_file:
    tex_file.write(latex_content)

print(f"LaTeX content saved to {tex_filename}")


def compile_tex_to_pdf(tex_filename):
    try:
        subprocess.run(["pdflatex", tex_filename], check=True)
        print(f"PDF generated successfully from {tex_filename}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to compile {tex_filename} to PDF. Error: {e}")

# Compile the .tex file to PDF
compile_tex_to_pdf(tex_filename)
