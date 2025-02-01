import subprocess
import sys

def install_requirements():
    """
    Install required libraries for the NLP analysis project.
    """
    requirements = [
        'nltk',
        'scikit-learn',
        'pandas',
        'numpy',
        'networkx',
        'plotly',
        'beautifulsoup4',
        'spacy',
        'matplotlib',
        'scipy',
        'PyMuPDF',  # This is the package name for fitz
        'pyvis'
    ]
    
    print("Starting installation of required packages...")
    
    # Check Python version
    python_version = sys.version.split()[0]
    if not python_version.startswith('3.9'):
        print(f"Warning: Current Python version is {python_version}. This script was designed for Python 3.9.x")
        response = input("Do you want to continue anyway? (y/n): ")
        if response.lower() != 'y':
            print("Installation cancelled.")
            return

    # Install each package
    for package in requirements:
        try:
            print(f"\nInstalling {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"Successfully installed {package}")
        except subprocess.CalledProcessError as e:
            print(f"Error installing {package}: {str(e)}")
            continue

    # Additional setup for spacy and nltk
    try:
        print("\nDownloading spaCy English language model...")
        subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
    except subprocess.CalledProcessError as e:
        print(f"Error downloading spaCy model: {str(e)}")

    try:
        print("\nDownloading required NLTK data...")
        import nltk
        nltk_downloads = [
            'punkt',
            'stopwords',
            'wordnet',
            'averaged_perceptron_tagger'
        ]
        for item in nltk_downloads:
            print(f"Downloading {item}...")
            nltk.download(item)
        print("Successfully downloaded NLTK data")
    except Exception as e:
        print(f"Error downloading NLTK data: {str(e)}")

    print("\nInstallation process completed!")

    # Verify installations
    print("\nVerifying installations...")
    try:
        import nltk
        import sklearn
        import pandas
        import numpy
        import networkx
        import plotly
        import bs4
        import spacy
        import matplotlib
        import scipy
        import fitz  # PyMuPDF
        import pyvis
        # pathlib is part of standard library, no need to verify
        print("All packages successfully imported!")
    except ImportError as e:
        print(f"Warning: Some packages may not have installed correctly: {str(e)}")

if __name__ == "__main__":
    install_requirements()