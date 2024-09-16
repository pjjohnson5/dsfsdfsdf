import os
import openai
import subprocess
import shutil
import logging
import json  # Import json module for parsing

def read_base_resume(file_path):
    # Read the base resume from a file
    with open(file_path, 'r') as f:
        base_resume = f.read()
    return base_resume

def get_buzzwords_with_chatgpt(job_description):
    # Use OpenAI to identify buzzwords in the job description
    prompt = f"""
You are an expert in resume writing and job description analysis.

Please identify the key buzzwords, skills, and important terms from the following job description:

<BEGIN JOB DESCRIPTION>
{job_description}
<END JOB DESCRIPTION>

Provide the buzzwords as a comma-separated list.
"""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an assistant that helps identify key buzzwords from job descriptions."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=150,
    )
    
    buzzwords_text = response['choices'][0]['message']['content']
    # Split the buzzwords into a list
    buzzwords = [word.strip() for word in buzzwords_text.split(',')]
    return buzzwords

def evaluate_buzzword_match_with_chatgpt(tailored_resume, buzzwords):
    # Use OpenAI to evaluate the buzzword match in the tailored resume
    prompt = f"""
You are an expert in resume evaluation.

The tailored resume is as follows:

<BEGIN RESUME>
{tailored_resume}
<END RESUME>

The key buzzwords from the job description are: {', '.join(buzzwords)}

When identifying buzzwords, please exclude the following educational degrees unless they specifically mention 'BS':
['BA', 'MS', 'CS', 'CE', 'IS']

Please evaluate how well the resume incorporates these buzzwords. Your response should be in the following JSON format:
{{
    "JD Match": "X/10",
    "MissingKeywords": ["keyword1", "keyword2"],
    "Profile Summary": "Your summary of the evaluation here."
}}

Fill in the details accurately.
"""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an assistant that evaluates resumes based on buzzword matching."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=300,
    )

    # Extract the response
    evaluation_result = response['choices'][0]['message']['content']

    # Attempt to parse the response as JSON
    try:
        evaluation_data = json.loads(evaluation_result)
        score = int(evaluation_data["JD Match"].split('/')[0])  # Extract the score as an integer
        missing_keywords = evaluation_data.get("MissingKeywords", [])
        profile_summary = evaluation_data.get("Profile Summary", "")
    except (json.JSONDecodeError, KeyError, ValueError) as e:
        # If parsing fails, log the response for debugging and use default values
        logging.error("Failed to parse JSON from ChatGPT response.")
        logging.error(f"ChatGPT Response: {evaluation_result}")
        score = 0  # Default score if extraction fails
        missing_keywords = []
        profile_summary = "Could not extract profile summary."

    return score, missing_keywords, profile_summary

def tailor_resume(base_resume, job_description, company_name, iteration, buzzwords, current_score):
    # Use OpenAI API to tailor the resume
    openai.api_key = os.getenv("OPENAI_API_KEY")
    if not openai.api_key:
        raise ValueError("Please set the OPENAI_API_KEY environment variable.")

    # Create the prompt for the API
    prompt = f"""
You are a professional resume writer.

The following is the base resume:

<BEGIN RESUME>
{base_resume}
<END RESUME>

The following is the job description for {company_name}:

<BEGIN JOB DESCRIPTION>
{job_description}
<END JOB DESCRIPTION>

The following are key buzzwords extracted from the job description:
{', '.join(buzzwords)}

Your task is to tailor the resume to achieve at least an 8/10 match score. The current match score is {current_score}/10. Use the buzzwords and the job description to modify the resume and improve this score.

Please tailor the resume by:
- Adding or removing skills from the skills section to match the keywords in the job description.
- Rewriting the job experience bullets to better align with the job description. You can change them however you like; feel free to make up details but try to get your inspiration from the provided resume.
- Look for easy substitutions. For example, substitute 'Kubernetes' with 'K8s' or 'Kubernetes (K8s)', 'Electrical Engineering (EE)', 'Bachelor of Science (BS)' and so on.
- Try your best to avoid niche business buzzwords from the job description that don't apply (e.g., 'Zoom Platform services'). Use more general terms instead (e.g., 'Application Platform services'). However, adding industry-specific buzzwords is encouraged.
- Use as many keywords and buzzwords from the job description as possible to maximize the chances of being selected by automated screening systems (ATS).
- Ensure that the tailored resume includes at least 80% of the buzzwords found in the job description.
- Aim to increase the match score to at least 8/10 in this attempt. This is attempt number {iteration}.
- Do not change other sections of the resume.
- Keep the resume in the same format as the base resume.
- Provide the tailored resume in Markdown format.
- The summary section at the top of the resume should be short and concise. No more then two sentences. The summary sections starts after: - [in/peyton-james-johnson]
- Make sure each job summary has at least three bullets of info
- Dont be afraid to add SRE if its a key word. Make up SRE bullets points if need. Site reliability engineer(SRE)
- The last thing is make sure everything fits on one page.

After providing the tailored resume, provide a summary of the changes made. The summary should start with the line "Summary of Changes:" and be in a separate section after the tailored resume.
"""

    # Call the OpenAI API
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that helps tailor resumes to job descriptions."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=2000,
    )

    # Extract the tailored resume and the summary of changes
    response_content = response['choices'][0]['message']['content']
    
    # Separate the tailored resume and summary of changes
    if "Summary of Changes:" in response_content:
        tailored_resume, summary_of_changes = response_content.split("Summary of Changes:", 1)
    else:
        tailored_resume = response_content
        summary_of_changes = "Could not extract summary of changes."

    return tailored_resume.strip(), summary_of_changes.strip()


def main():
    # Set up logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Path to the base resume (always "base.md")
    base_resume_path = "base.md"
    base_resume = read_base_resume(base_resume_path)

    while True:
        # Ask for the job description
        print("\nPlease enter the job description (paste the text and then enter 'END' on a new line):")
        job_description_lines = []
        while True:
            line = input()
            if line.strip().upper() == 'END':
                break
            job_description_lines.append(line)
        job_description = '\n'.join(job_description_lines)

        # Ask for the company name
        company_name = input("Enter the company name: ")

        # Get buzzwords from the job description using ChatGPT
        job_buzzwords = get_buzzwords_with_chatgpt(job_description)
        logging.info(f"Identified Buzzwords: {job_buzzwords}")

        # Tailoring loop to achieve desired keyword match criteria
        tailored_resume = base_resume
        summary_of_changes = ""
        max_attempts = 10  # Maximum number of attempts to avoid infinite loop
        attempt = 0
        buzzword_match_after = 0
        missing_keywords = []

        while attempt < max_attempts:
            attempt += 1
            logging.info(f"Attempt #{attempt}: Tailoring the resume to improve keyword match.")

            # Tailor the resume (include buzzwords and current score in the call)
            tailored_resume, summary_of_changes = tailor_resume(
                tailored_resume, job_description, company_name, attempt, job_buzzwords, buzzword_match_after
            )

            # Evaluate keyword match using ChatGPT
            buzzword_match_after, missing_keywords, profile_summary = evaluate_buzzword_match_with_chatgpt(
                tailored_resume, job_buzzwords
            )
            logging.info(f"Buzzword Match After Attempt #{attempt}: {buzzword_match_after}/10")
            logging.info(f"Missing Keywords: {missing_keywords}")
            logging.info(f"Evaluation Summary: {profile_summary}")

            # Check if the desired criteria are met (3 or fewer keywords missing)
            if len(missing_keywords) <= 4:
                logging.info(f"Desired keyword match criteria achieved after {attempt} attempts: 3 or fewer missing keywords.")
                break
        else:
            logging.info(f"Could not achieve the desired keyword match criteria after {max_attempts} attempts.")

        # Save only the tailored resume as "resume.md"
        tailored_markdown_file = "resume.md"
        with open(tailored_markdown_file, 'w') as f:
            f.write(tailored_resume)

        # Call the CLI to create the PDF from "resume.md"
        try:
            subprocess.run(['python3', 'resume.py', tailored_markdown_file], check=True)
            print("PDF generated as resume.pdf.")

            # Define the new PDF filename
            pdf_output_filename = f"Peyton Johnson's {company_name} Resume.pdf"

            # Copy the generated PDF to the new filename
            shutil.copy('resume.pdf', pdf_output_filename)
            print(f"PDF copied and renamed to {pdf_output_filename}.")
        except subprocess.CalledProcessError as e:
            print(f"An error occurred while creating the PDF: {e}")
        except FileNotFoundError:
            print("resume.pdf not found. Ensure the resume.py script generates this file correctly.")

        # Output keyword match and summary
        print(f"\nBuzzword Match After: {buzzword_match_after}/10")
        print(f"Missing Keywords: {missing_keywords}")
        print("\nProfile Summary:")
        print(profile_summary)
        print("\nSummary of Changes:")
        print(summary_of_changes)

        # Ask if the user wants to tailor another resume
        repeat = input("\nDo you want to tailor another resume? (yes/no): ").lower()
        if repeat != 'yes':
            break


if __name__ == "__main__":
    main()
