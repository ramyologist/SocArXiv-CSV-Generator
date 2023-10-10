SocArXiv Preprints Link Generator

The "SocArXiv Preprints Link Generator" is a Streamlit app that allows users to generate a list of SocArXiv preprints based on their chosen subject. The app fetches preprints data from the SocArXiv API and provides a downloadable CSV file containing preprint information, including authors, titles, and download links to the PDF files.
Features

    Select a subject from the dropdown list.
    Click the "Fetch Preprints" button to generate a CSV file.
    Download the CSV file containing preprints' information.

Usage

    Launch the Streamlit app.
    Choose a subject from the dropdown list.
    Click the "Fetch Preprints" button.
    Wait for the preprints to be fetched (a progress bar is displayed).
    Once all preprints are fetched, a "Download CSV" button will appear.
    Click the "Download CSV" button to download the CSV file containing preprints' information.

Dependencies

The code uses the following Python libraries and modules:

    csv: For CSV file handling.
    requests: For making HTTP requests to the SocArXiv API.
    re: For regular expressions to parse DOI metadata.
    pylatexenc.latex2text: For converting LaTeX-encoded author names to text.
    streamlit: For creating the web application.

Configuration

    base_url: The base URL for the SocArXiv API.
    subject_url: The URL for fetching subject data.
    fetch_all_subjects(): Function to fetch all available subjects from the SocArXiv API.
    fetch_doi_metadata(doi): Function to fetch metadata for a given DOI.
    extract_bibtex_metadata(bibtex_str): Function to extract year and author information from BibTeX metadata.
    fetch_all_preprints_with_year_and_author(progress_bar, subject_filter): Function to fetch preprints for a selected subject and retrieve author and year information.
    create_csv_with_selected_columns(preprints): Function to create a CSV file containing selected preprints' columns.

Usage Notes

    The Streamlit app may experience occasional crashes. In such cases, you can consider downloading the code from the GitHub repository provided and running it on a local host.

GitHub Repository

    GitHub Repo

Author

    This Streamlit app is created by "ramyologist."

Version

    Version 1.0.0

This app provides a convenient way to access and organize SocArXiv preprints data based on subject preferences and export it in a CSV format for further analysis or reference.
