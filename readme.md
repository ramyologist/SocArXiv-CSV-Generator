# SocArXiv Preprints Link Generator

![GitHub](https://img.shields.io/github/license/ramyologist/SocArXiv-CSV-Generator)

This Streamlit app allows you to generate a list of SocArXiv preprints based on the selected subject and title search. You can filter preprints by subject, search for keywords in titles, and export the results to a CSV file.

## Features

- Select a subject from the dropdown list or choose "All Subjects" to search in all subjects.
- Enter keywords in the search box to filter preprints by title.
- Real-time progress bar displays the count of preprints included in the CSV file during the search.

## Requirements

- Python 3.x
- Install the required Python packages by running `pip install -r requirements.txt`.

## Usage

1. Clone or download this repository to your local machine.
2. Install the required Python packages by running `pip install -r requirements.txt`.
3. Run the Streamlit app by executing `streamlit run SocArXiv_csv_list_generator.py`.
4. Select a subject from the dropdown list or choose "All Subjects" to search in all subjects.
5. Enter keywords in the search box to filter preprints by title.
6. Click the "Search Preprints" button to initiate the search.
7. The progress bar will show the progress of fetching and filtering preprints.
8. Once the search is complete, a download button for the CSV file will appear.
9. Click the "Download CSV" button to save the preprints' information as a CSV file.

## New in Version 1.1.0

- Now supports searching for preprints based on their titles.
- Added a "Subject" column in the CSV file to indicate the selected subject for each preprint.
- Implemented a progress bar that displays the real-time count of preprints included in the CSV file during the search.

## Acknowledgments

- Special thanks to the [SocArXiv](https://osf.io/preprints/socarxiv/) platform for providing access to preprints data.

If you encounter any issues or have suggestions for improvements, please feel free to [open an issue](https://github.com/ramyologist/SocArXiv-CSV-Generator/issues).
