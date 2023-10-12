import csv
import requests
import re
from pylatexenc.latex2text import LatexNodes2Text
import streamlit as st
from io import StringIO

# Set the title of the Streamlit app
st.title('SocArXiv Preprints Link Generator')

# Provide information about the app
st.write(
    '''
    \n Version 1.1.0.
    \n This app allows you to generate a list of SocArXiv preprints based on the selected subject and title search.
    Simply choose a subject from the dropdown list, enter keywords in the search box, and click on 'Search Preprints', 
    to generate a CSV file with a list containing authors, titles, subjects, and download links to the pdf-files.
    \n When the search is complete, a download button for the CSV file appears. 
    \n Searching across all subjects might take some time. Feel free to fetch yourself a drink in the meantime.
    \n Unfortunately, the Streamlit server sometimes crashes. In this case, you may consider downloading the code from my GitHub Repo and running it on a local host. 
    
    GitHub Repo: https://github.com/ramyologist/SocArXiv-CSV-Generator
    
    Cheers, 
    
    ramyologist
    '''
)

# Define the base URL for the SocArXiv API
base_url = "https://api.osf.io/v2/providers/preprints/socarxiv/preprints/"
# Define the URL for fetching subject data
subject_url = "https://api.osf.io/v2/providers/preprints/socarxiv/taxonomies/"

# Function to fetch all available subjects from the SocArXiv API
def fetch_all_subjects():
    subjects = []
    page = 1
    while True:
        params = {"page[size]": 100, "page": page}
        response = requests.get(subject_url, params=params)
        data = response.json()
        if "data" not in data or not data["data"]:
            break
        subjects.extend([subject["attributes"]["text"] for subject in data["data"]])
        page += 1
    return subjects

# Fetch all available subjects
available_subjects = fetch_all_subjects()

# Add "All Subjects" as an option at the beginning of the subject list
available_subjects.insert(0, "All Subjects")

# Create a dropdown to select a subject
subject_filter = st.selectbox("Select a subject:", available_subjects)

# Function to fetch metadata for a given DOI
def fetch_doi_metadata(doi):
    headers = {
        "Accept": "application/x-bibtex"
    }
    response = requests.get(f"http://dx.doi.org/{doi}", headers=headers)
    return response.text if response.status_code == 200 else None

# Function to extract year and author information from BibTeX metadata
def extract_bibtex_metadata(bibtex_str):
    year_match = re.search(r"year\s*=\s*{(\d{4})", bibtex_str)
    author_match = re.search(r"author\s*=\s*{([^}]+)", bibtex_str)
    
    year = year_match.group(1) if year_match else None
    author = author_match.group(1) if author_match else None
    
    # Convert LaTeX-encoded author names to text
    def latex_to_unicode(latex_str):
        return LatexNodes2Text().latex_to_text(latex_str)
    if author:
        author = latex_to_unicode(author)
    
    return year, author

# Function to fetch preprints for a specific subject and retrieve author and year information
def fetch_subject_preprints_with_year_and_author(subject_filter, search_keywords, progress_text, progress_bar):
    preprints = []
    page = 1
    total_preprints = 0
    while True:
        params = {
            "page[size]": 100,
            "page": page,
            "filter[subjects]": subject_filter if subject_filter != "All Subjects" else None,
        }
        response = requests.get(base_url, params=params)
        data = response.json()
        new_preprints_count = len(data.get("data", []))
        if not new_preprints_count:
            break
        for preprint in data["data"]:
            title = preprint["attributes"]["title"]
            osf_link = preprint["links"]["preprint_doi"].replace("https://doi.org/10.31235/osf.io/", "https://osf.io/preprints/socarxiv/") + "/"
            doi_link = f"https://doi.org/10.31235/osf.io/{osf_link.split('/')[-2]}"
            download_link = f"{osf_link}download"
            if search_keywords.lower() in title.lower():  # Filter by search keywords in title
                metadata = fetch_doi_metadata(doi_link)
                _, author = extract_bibtex_metadata(metadata) if metadata else (None, None)
                preprints.append((author, title, subject_filter, osf_link, download_link))
                total_preprints += 1
                progress_text.text(f"Total Preprints Fetched: {total_preprints}")
        progress_bar.progress(total_preprints/15000)
        page += 1
    return preprints

# Function to create a CSV file containing selected preprints' columns
def create_csv_with_selected_columns(preprints):
    csv_file = StringIO()
    writer = csv.writer(csv_file)
    writer.writerow(["Author", "Title", "Subject", "OSF Link", "Download Link"])
    for author, title, subject, osf_link, download_link in preprints:
        writer.writerow((author, title, subject, osf_link, download_link))
    return csv_file.getvalue()

# Create a text input for searching keywords in titles
search_keywords = st.text_input("Search Keywords in Titles")

# If the "Search Preprints" button is clicked
if st.button("Search Preprints"):
    progress_text = st.empty()
    progress_bar = st.progress(0.0)

    # Fetch and search preprints based on the selected subject and title keywords
    preprints = fetch_subject_preprints_with_year_and_author(subject_filter, search_keywords, progress_text, progress_bar)
    
    # Create a CSV file containing preprints' information
    csv_content = create_csv_with_selected_columns(preprints)
    
    # Remove progress bar
    progress_bar.empty()
    
    # Add a download button for the CSV file
    st.download_button("Download CSV", csv_content, f"preprints_by_title_and_subject.csv", "text/csv")
