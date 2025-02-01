import fitz  # PyMuPDF
import spacy
import time
import networkx as nx
from pyvis.network import Network
from pathlib import Path
import json

# Function to extract text from a single PDF
def extract_text_from_pdf(pdf_path):
    print(f"Extracting text from {pdf_path}...")
    doc = fitz.open(pdf_path)
    text = ""
    for page_num in range(len(doc)):
        print(f"Processing page {page_num + 1} of {len(doc)}...")
        page = doc[page_num]
        text += page.get_text()
    return text

def perform_ner(text):
    print("Performing Named Entity Recognition...")
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    print(f"Extracted {len(entities)} entities.")
    return entities
# Function to visualize entities as a 3D network
def visualize_entities(entities, output_file):
    G = nx.Graph()

    # Add nodes and edges based on entities
    for entity, label in entities:
        G.add_node(entity, label=label)

    # Example: Connect entities with the same label
    for i, (entity1, label1) in enumerate(entities):
        for j, (entity2, label2) in enumerate(entities):
            if i != j and label1 == label2:
                G.add_edge(entity1, entity2)

    # Visualize using pyvis
    net = Network(height="750px", width="100%", notebook=False, cdn_resources="in_line", layout=True)
    net.from_nx(G)
    net.write_html(output_file)
    print(f"Visualization saved to {output_file}. Open this file in a browser to view the graph.")

# Main function to process all PDFs in a folder
def process_pdfs_in_folder(folder_path):
    pdf_folder = Path(folder_path)
    pdf_files = list(pdf_folder.glob("*.pdf"))

    all_entities = []

    for pdf_file in pdf_files:
        print(f"Processing {pdf_file.name}...")
        text = extract_text_from_pdf(pdf_file)
        entities = perform_ner(text)
        all_entities.extend(entities)

    # Visualize all entities from all PDFs
    json_output_file = "content/results/entities.json"
    save_entities_to_json(all_entities, json_output_file)
    
    output_file = "content/results/combined_entity_network.html"
    visualize_entities(all_entities, output_file)
    print("Visualization saved as combined_entity_network.html")
    print("All PDFs have been processed.")


def save_entities_to_json(entities, output_file):
    # Group entities by their labels
    entity_dict = {}
    for entity, label in entities:
        if label not in entity_dict:
            entity_dict[label] = []
        if entity not in entity_dict[label]:
            entity_dict[label].append(entity)

    # Save the dictionary as a JSON file
    with open(output_file, "w") as f:
        json.dump(entity_dict, f, indent=4)
    print(f"Entities saved to {output_file}")

# Usage
if __name__ == "__main__":
    folder_path = "content/pdf"  # Replace with the path to your PDF folder
    start_time = time.time()
    process_pdfs_in_folder(folder_path)
    elapsed_time = time.time() - start_time
    print(f"Processing completed in {elapsed_time:.2f} seconds.")