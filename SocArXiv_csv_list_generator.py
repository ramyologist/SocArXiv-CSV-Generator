import csv
import requests
import re
from pylatexenc.latex2text import LatexNodes2Text
import streamlit as st



st.title('SocArXiv Preprints Link Generator')

st.write(
    '''
    This app allows you to generate links to SocArXiv preprints based on the selected subject.
    Simply choose a subject from the dropdown list and click on 'Create CSV File', 
    to generate a CSV file with a list containing authors, titles and links to the preprints of the selected subject.
    
    GitHub-Repo: https://github.com/ramyologist/SocArXiv-CSV-Generator
    
    Cheers, 
    
    ramyologist
    '''
)

from io import StringIO

base_url = "https://api.osf.io/v2/providers/preprints/socarxiv/preprints/"
subject_url = "https://api.osf.io/v2/providers/preprints/socarxiv/taxonomies/"

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

available_subjects = fetch_all_subjects()

def fetch_doi_metadata(doi):
    headers = {
        "Accept": "application/x-bibtex"
    }
    response = requests.get(f"http://dx.doi.org/{doi}", headers=headers)
    return response.text if response.status_code == 200 else None

def extract_bibtex_metadata(bibtex_str):
    year_match = re.search(r"year\s*=\s*{(\d{4})", bibtex_str)
    author_match = re.search(r"author\s*=\s*{([^}]+)", bibtex_str)
    
    year = year_match.group(1) if year_match else None
    author = author_match.group(1) if author_match else None
    def latex_to_unicode(latex_str):
        return LatexNodes2Text().latex_to_text(latex_str)
    if author:
        author = latex_to_unicode(author)
    
    return year, author

def fetch_all_preprints_with_year_and_author(progress_bar, subject_filter):
    preprints = []
    page = 1
    total_preprints = 0
    while True:
        params = {"page[size]": 100, "page": page, "filter[subjects]": subject_filter}
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
            metadata = fetch_doi_metadata(doi_link)
            _, author = extract_bibtex_metadata(metadata) if metadata else (None, None)
            preprints.append((author, title, osf_link, download_link))
        total_preprints += new_preprints_count
        progress_text.text(f"Total Preprints Fetched: {total_preprints}")
        progress_bar.progress(total_preprints/15000)
        page += 1
    return preprints

def create_csv_with_selected_columns(preprints):
    csv_file = StringIO()
    writer = csv.writer(csv_file)
    writer.writerow(["Author", "Title", "OSF Link", "Download Link"])
    for author, title, osf_link, download_link in preprints:
        writer.writerow((author, title, osf_link, download_link))
    return csv_file.getvalue()

subject_filter = st.selectbox("Select a subject:", available_subjects)

if st.button("Generate CSV"):
    progress_text = st.empty()
    progress_bar = st.empty()
    preprints = fetch_all_preprints_with_year_and_author(progress_bar, subject_filter)
    csv_content = create_csv_with_selected_columns(preprints)
    progress_bar.empty()
    st.download_button("Download CSV", csv_content, f"{subject_filter}_preprints.csv", "text/csv")
else:
    st.write(f"")
