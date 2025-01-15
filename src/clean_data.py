import pandas as pd
import os
import argparse

def clean_and_restructure_data(df):
    """
    Clean and restructure the scraped data for chatbot training.
    Deduplicates rows with the same question and answer, keeping only the first.
    """
    # Step 1: Standardize text (lowercase, strip whitespace)
    df['question'] = df['question'].str.lower().str.strip()
    df['answer'] = df['answer'].str.lower().str.strip()

    # Step 2: Filter out invalid rows
    # Remove rows with empty 'question' or 'answer'
    df = df.dropna(subset=['question', 'answer'])
    # Remove rows where 'answer' is too short to be meaningful
    df = df[df['answer'].str.len() > 20]

    # Step 3: Deduplicate rows based on 'question' and 'answer'
    df = df.drop_duplicates(subset=['question', 'answer'])

    # Step 4: Keep only relevant columns
    df = df[['url', 'question', 'answer']]

    return df

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Clean and restructure scraped data for chatbot training.")
    parser.add_argument("file_path", type=str, help="Path to the input CSV file.")
    args = parser.parse_args()

    # Extract filename and directory for output
    file_path = args.file_path
    file_dir, file_name = os.path.split(file_path)
    base_name, ext = os.path.splitext(file_name)
    output_name = f"cleaned-{base_name}{ext}"
    output_path = os.path.join(file_dir, output_name)

    # Load the data
    print(f"[INFO] Loading data from: {file_path}")
    data = pd.read_csv(file_path)

    # Clean and restructure the data
    cleaned_data = clean_and_restructure_data(data)

    # Save the cleaned data
    cleaned_data.to_csv(output_path, index=False)
    print(f"[INFO] Data cleaning completed. Cleaned data saved to: {output_path}")

if __name__ == "__main__":
    main()
