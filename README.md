# ResumeAI Tailoring Script

The goal of this script is to increase your chances of landing job interviews by tailoring your resume to align closely with the job description and optimizing it for Applicant Tracking Systems (ATS). By incorporating relevant buzzwords and key skills, this script helps your resume rank higher in ATS screenings, making it more likely to be seen by recruiters and hiring managers.

## How It Helps You Get More Job Interviews

Many companies use ATS to screen resumes before they reach a human recruiter. These systems look for specific keywords and phrases to match candidates to job descriptions. This script helps you beat the ATS by:
- **Extracting Relevant Buzzwords:** Uses OpenAI's GPT-4 to identify important keywords, skills, and terms from the job description.
- **Tailoring Your Resume:** Iteratively customizes your base resume to include as many relevant buzzwords as possible.
- **Optimizing for ATS:** Ensures that your resume is formatted in an ATS-friendly way, increasing its chances of passing the initial screening.

By focusing on these aspects, the script helps make your resume more appealing to both ATS and human recruiters, ultimately increasing the likelihood of getting an interview.

## Features

- **Buzzword Extraction:** Uses GPT-4 to extract key buzzwords and skills from the job description, excluding specific educational degrees except for 'BS'.
- **Resume Tailoring:** Modifies the base resume to include as many relevant buzzwords as possible, ensuring it aligns closely with the job requirements.
- **Evaluation:** Iteratively evaluates the tailored resume, aiming to minimize the number of missing buzzwords to three or fewer.
- **PDF Generation:** Converts the tailored resume into a PDF file, keeping the formatting simple and ATS-friendly.

## How It Works

1. **Input Job Description:** The user inputs a job description and the target company name.
2. **Extract Buzzwords:** The script extracts key buzzwords from the job description using GPT-4, excluding specific degree-related terms that may not be relevant.
3. **Tailor the Resume:** The script iteratively modifies the base resume to include the buzzwords, aiming to reduce the number of missing keywords to three or fewer.
4. **Optimize for ATS:** The tailored resume is kept in a straightforward format, avoiding complex formatting that can confuse ATS.
5. **Generate PDF:** Once the tailoring process is complete, the script generates an ATS-friendly PDF file of the tailored resume.

## Prerequisites

- Python 3.x
- OpenAI Python library (`openai`)
- An OpenAI API key with access to GPT-4
- Pandoc and a PDF engine (e.g., LaTeX) installed on your system for PDF generation
- Necessary Python modules: `os`, `subprocess`, `shutil`, `logging`, `json`

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/resume-tailoring.git
   cd resume-tailoring
   ```

2. **Install Python Dependencies**
   ```bash
   pip install openai
   ```

3. **Set Up OpenAI API Key**
Set your OpenAI API key as an environment variable. You can use google on how to you get your API key:
   ```bash
   export OPENAI_API_KEY="your_openai_api_key"
   ```
## Usage

1. **Prepare the Base Resume:**  
   Place your base resume in the same directory as the script and name it `base.md`. Use chatgpt to convert your PDF resume to Markdown Langue. 

2. **Run the Script:**

   ```bash
   python3 tailor_resume.py
   ```
## Provide Job Description and Company Name:
- When prompted, paste the job description text.
- Enter `END` on a new line to finish the input.
- Provide the target company name.

## Tailoring Process:
The script will tailor the resume iteratively. It will stop when it successfully reduces the number of missing keywords to three or fewer.

## Output:
- The tailored resume will be saved as `resume.md`.
- A PDF file named `Peyton Johnson's <Company Name> Resume.pdf` will be generated.

## Example

```bash
python3 tailor_resume.py
```

## How It Beats the ATS

- **Keyword Optimization:** The script ensures that the resume includes as many relevant keywords from the job description as possible. ATS often rank resumes based on the presence of these keywords.
- **ATS-Friendly Format:** The generated resume avoids complex formatting elements like tables, images, or graphics that can confuse ATS. It maintains a simple structure that is easily parsed by most systems.
- **Custom Tailoring:** By focusing on the specific requirements of each job description, the script ensures that each tailored resume is unique and directly relevant to the position, increasing its chances of passing the ATS screening.

## Configuration and Customization

- **Excluding Keywords:**  
  By default, the script excludes specific educational keywords such as 'BA', 'MS', 'CS', 'CE', and 'IS' from the buzzword extraction. You can modify the `get_buzzwords_with_chatgpt` function to adjust these exclusions if needed.

- **Max Attempts:**  
  The maximum number of tailoring attempts is set to 10 by default. This can be adjusted in the `main` function.

- **Tweaking the Tailoring Process:**  
  You might need to tweak the `tailor_resume` function to better align with the requirements of your specific job field. Adjusting the prompts or tailoring logic can help improve the quality of the generated resume for your industry.

## Notes

- The script currently requires an OpenAI GPT-4 API key. Make sure you have access to GPT-4 in your OpenAI account.

- The script assumes that `pandoc` and a PDF engine are installed for generating PDFs. On macOS, this can be done using Homebrew: