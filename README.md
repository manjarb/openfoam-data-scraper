
# Web Scraper and Cleaner for Chatbot Training

This project includes a web scraper and a data cleaning script designed to extract and prepare Q&A data from websites for chatbot training. The tool allows dynamic control over crawling depth, page limits, and output customization.

---

## **Features**
- **Web Scraper**:
  - Extracts headers and their associated content from web pages.
  - Handles headers with embedded links (`<a>` tags).
  - Dynamically follows links within the same domain.
  - Supports depth-limited crawling.
- **Data Cleaner**:
  - Cleans and restructures scraped data into a Q&A format.
  - Deduplicates rows to ensure unique Q&A pairs.
  - Filters out irrelevant or invalid data.

---

## **Important Note**
The scraper is designed to:
- Crawl only the **same main domain and its subdomains** as the starting URL.
- Ensure that links to external or unrelated domains are ignored.

This behavior guarantees focused data collection relevant to the starting domain.

---

## **Requirements**
### **Python Dependencies**
- Install dependencies using `pip`:
  ```bash
  pip install -r requirements.txt
  ```

### **Required Libraries**
- `requests`
- `beautifulsoup4`
- `pandas`
- `tldextract`

---

## **Usage**

### **1. Run the Scraper**
The scraper extracts data from a specified URL.

#### **Command**
```bash
python src/scraper.py <start_url> <output_file> --max_pages <max_pages> --max_depth <max_depth>
```

#### **Arguments**
- `<start_url>`: The starting URL for scraping.
- `<output_file>`: The name of the CSV file to save the scraped data.
- `--max_pages`: (Optional) Maximum number of pages to scrape (default: 100).
- `--max_depth`: (Optional) Maximum depth for crawling (default: 3).

#### **Example**
```bash
python src/scraper.py "https://cfd.direct/openfoam/management/" "cfd-derict.csv" --max_pages 100 --max_depth 3
```

---

### **2. Run the Data Cleaner**
The cleaner processes the scraped data to remove invalid rows, deduplicate, and restructure it.

#### **Command**
```bash
python src/clean_data.py <file_path>
```

#### **Arguments**
- `<file_path>`: Path to the scraped CSV file.

#### **Example**
```bash
python src/clean_data.py cfd-derict.csv
```

---

### **3. Run Both with the Bash Script**
To streamline the process, use the `run_all.sh` script to run both the scraper and cleaner sequentially.

#### **Command**
```bash
./run_all.sh <start_url> <output_file> <max_pages> <max_depth>
```

#### **Arguments**
- `<start_url>`: The starting URL for scraping.
- `<output_file>`: The name of the CSV file to save the scraped data.
- `<max_pages>`: Maximum number of pages to scrape.
- `<max_depth>`: Maximum depth for crawling.

#### **Example**
```bash
./run_all.sh "https://cfd.direct/openfoam/management/" "cfd-derict.csv" 100 3
```

---

## **Output**
### **Scraper Output**
The scraper saves a CSV file with the following structure:
| **url**                   | **question**            | **answer**                      |
|---------------------------|-------------------------|----------------------------------|
| https://example.com/page1 | What is OpenFOAM?       | OpenFOAM is a CFD simulation... |
| https://example.com/page2 | How to install OpenFOAM?| Follow these steps to install...|

### **Cleaner Output**
The cleaner saves a cleaned version of the CSV file, prefixed with `cleaned-`:
| **url**                   | **question**            | **answer**                      |
|---------------------------|-------------------------|----------------------------------|
| https://example.com/page1 | What is OpenFOAM?       | OpenFOAM is a CFD simulation... |
| https://example.com/page2 | How to install OpenFOAM?| Follow these steps to install...|

---

## **Error Handling**
- The scraper and cleaner will terminate with an error message if something goes wrong.
- Use the `--max_pages` and `--max_depth` arguments to avoid excessive crawling.

---

## **Development Notes**
- **Modularity**: The scraper and cleaner are separate scripts, ensuring reusability and easy testing.
- **Scalability**: Supports large-scale scraping with controlled limits on pages and depth.

---

## **Future Enhancements**
- Add support for scraping additional content types (e.g., lists, tables).
- Implement more advanced cleaning techniques (e.g., NLP-based content filtering).
- Add support for multithreaded scraping to improve performance.

---

## **License**
This project is licensed under the MIT License.
