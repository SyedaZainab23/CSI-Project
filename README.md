This script allows you to retrieve PubMed articles based on a search term, perform Named Entity Recognition (NER) on the abstracts, and generate a word cloud visualization of the extracted entities.

## Requirements

Before running the script, ensure you have the following installed:

- Python 3.x
- pip (Python package manager)

## Installation

1. Clone or download the repository to your local machine.
2. Navigate to the project directory in your terminal/command prompt.
3. Install the required Python packages

scispacy==0.4.0
spacy==3.2.1
pandas==1.3.3
requests==2.26.0
wordcloud==1.8.1
matplotlib==3.4.3

!pip install https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.5.1/en_core_sci_sm-0.5.1.tar.gz
!pip install https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.5.1/en_core_sci_md-0.5.1.tar.gz
!pip install https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.5.1/en_ner_bc5cdr_md-0.5.1.tar.gz
     

## Usage

To run the script, follow these steps:

1. Open your terminal/command prompt.
2. Navigate to the directory where the script is located.
3. Run the script with the following command:

```
python script.py [search_term]
```

Replace `[search_term]` with the term you want to search for PubMed articles. For example:

```
python script.py Bcl-x
```

## Output

After running the script, the following files will be generated:

- `pubmed_articles_[search_term].xlsx`: Excel file containing retrieved PubMed articles.
- `pubmed_errors_[search_term].xlsx`: Excel file containing PubMed IDs with errors (if any).
- `abstract_entities_[search_term].csv`: CSV file containing extracted entities from abstracts.
- `wordcloud_[search_term].png`: Word cloud image representing the extracted entities.
