
import csv
import requests
import streamlit as st

st.title('SocArXiv Preprints Link Generator')

st.write(
'''
This app allows you to generate links to SocArXiv preprints based on the selected subject.
Simply choose a subject from the dropdown list and click on 'Create CSV File', 
to generate a CSV file with a list containing authors, titles and links to the preprints of the selected subject.
\n GitHub-Repo: https://github.com/ramyologist/SocArXiv-CSV-Generator
\n Cheers, 
\n ramyologist
'''
)
from io import StringIO


def normalize_authors(authors):
    normalized_authors = []
    for author in authors:
        if isinstance(author, str):
            normalized_authors.append(author)
        elif isinstance(author, list):
            normalized_author = ", ".join(author)
            normalized_authors.append(normalized_author)
    return normalized_authors
for author in authors:
if isinstance(author, str):
normalized_authors.append(author)
elif isinstance(author, list):
normalized_author = ", ".join(author)
normalized_authors.append(normalized_author)
return normalized_authors
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

def fetch_all_preprints(progress_bar, subject_filter):
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

author_data = preprint["relationships"].get("contributors", {}).get("data", [])
if author_data and isinstance(author_data[0], str):
authors = ", ".join(author_data)
elif author_data and isinstance(author_data[0], dict):
authors = ", ".join([author["attributes"]["full_name"] for author in author_data])
else:
authors = ""

doi = preprint["links"]["preprint_doi"].replace("https://doi.org/10.31235/osf.io/", "https://osf.io/preprints/socarxiv/") + "/"
download_link = f"{doi}download"
subjects = ", ".join([subject["attributes"]["text"] for subject in preprint["relationships"].get("subjects", {}).get("data", [])])
preprints.append((authors, title, doi, download_link, subjects))
total_preprints += new_preprints_count
progress_text.text(f"Total Preprints Fetched: {total_preprints}")
progress_bar.progress(total_preprints/15000)
page += 1
return preprints

def create_csv(preprints):
csv_file = StringIO()
writer = csv.writer(csv_file)
writer.writerow(["Authors", "Title", "DOI", "Download Link", "Subjects"])
for authors, title, doi, download_link, subjects in preprints:
writer.writerow((authors, title, doi, download_link, subjects))
return csv_file.getvalue()

# Dropdown for subject filtering
subject_filter = st.selectbox("Select a subject:", available_subjects)

if st.button("Generate CSV"):
progress_text = st.empty()
progress_bar = st.empty()
preprints = fetch_all_preprints(progress_bar, subject_filter)
csv_content = create_csv(preprints)
progress_bar.empty()
st.download_button("Download CSV", csv_content, f"{subject_filter}_preprints.csv", "text/csv")
else:
st.write(f"")
