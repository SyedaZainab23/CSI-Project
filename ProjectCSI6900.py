import argparse
import pandas as pd
import requests
from xml.etree import ElementTree
import spacy
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Load the SciSpacy model
nlp_sm = spacy.load("en_core_sci_sm")

def get_pubmed_articles(query, max_results=1000):
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {
        "db": "pubmed",
        "retmode": "xml",
        "term": query,
        "retmax": max_results
    }
    search_response = requests.get(base_url, params=params)
    search_xml = ElementTree.fromstring(search_response.content)
    pmids = [pmid.text for pmid in search_xml.findall(".//IdList/Id")]
    total_found = int(search_xml.find(".//Count").text)
    articles = []
    errors = []
    for pmid in pmids:
        fetch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
        fetch_params = {
            "db": "pubmed",
            "retmode": "xml",
            "id": pmid
        }
        fetch_response = requests.get(fetch_url, params=fetch_params)
        if fetch_response.status_code == 200:
            article_xml = ElementTree.fromstring(fetch_response.content)
            title = article_xml.find(".//ArticleTitle").text
            abstract_element = article_xml.find(".//AbstractText")
            abstract = abstract_element.text if abstract_element is not None else "Abstract not available"
            articles.append({'pubmedid': pmid, 'title': title, 'abstract': abstract})
        else:
            errors.append(pmid)
            print(f"Error fetching article with PMID {pmid}")
    return articles, total_found, errors

def main():
    # Argument parser
    parser = argparse.ArgumentParser(description="PubMed Article Retrieval and NER Word Cloud Generation")
    parser.add_argument("query", type=str, help="Search term for PubMed articles")

    # Parse command line arguments
    args = parser.parse_args()

    # Example usage:
    articles, total_found, errors = get_pubmed_articles(args.query)

    # Convert articles data into a pandas DataFrame
    df = pd.DataFrame(articles)

    # Save DataFrame to Excel file
    excel_filename = f"pubmed_articles_{args.query}.xlsx"
    df.to_excel(excel_filename, index=False)
    print(f"Excel file '{excel_filename}' saved successfully.")

    # Save errors to a separate Excel sheet
    errors_df = pd.DataFrame({"PubMed IDs with Errors": errors})
    errors_excel_filename = f"pubmed_errors_{args.query}.xlsx"
    errors_df.to_excel(errors_excel_filename, index=False)
    print(f"Excel file '{errors_excel_filename}' saved successfully.")

    # Perform NER on all abstracts
    all_entities = []
    for abstract in df['abstract']:
        if abstract is not None:  # Check if abstract is not None
            doc = nlp_sm(abstract)
            entities = [ent.text for ent in doc.ents]
            all_entities.extend(entities)

    # Save the extracted entities to a DataFrame
    df_entities = pd.DataFrame({"Entities": all_entities})

    # Save the DataFrame to a CSV file
    entities_csv_filename = f"abstract_entities_{args.query}.csv"
    df_entities.to_csv(entities_csv_filename, index=False)
    print(f"CSV file '{entities_csv_filename}' saved successfully.")

    # Generate a word cloud for the unique terms
    wordcloud = WordCloud(width=800, height=800, background_color='white', min_font_size=10).generate(' '.join(all_entities))

    # Display the word cloud
    plt.figure(figsize=(8, 8), facecolor=None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad=0)

    # Save the word cloud to an image file
    wordcloud_image_filename = f"wordcloud_{args.query}.png"
    wordcloud.to_file(wordcloud_image_filename)
    print(f"Word cloud image '{wordcloud_image_filename}' saved successfully.")

    # Show the word cloud
    plt.show()


if __name__ == "__main__":
    main()
