## 1. Link Scraping (`grab_links.py`)

This script uses Selenium to scrape job links from Indeed based on specified job roles. It accepts an input CSV file containing job roles and outputs a CSV file with the corresponding job links.

### Key Features:
- **Selenium WebDriver**: Automates web browsing to search for jobs and collect job links.
- **Error Handling**: Catches and logs any element or timeout exceptions that may occur during scraping.
- **Customizable Inputs**: Reads from an input CSV (`input_csv`) containing job roles and writes output to a specified CSV (`output_csv`).

### Usage:

```bash
python grab_links.py --input_csv "/path/to/your/input.csv" --output_csv "/path/to/your/output.csv"
```

### 2. `generate_bullet_points.py`

This script generates bullet points from text, specifically job descriptions and responsibilities. It utilizes the `facebook/bart-large-cnn` model for summarization and then processes the text into a bullet-pointed format.

**Key Functions:**
- `clean_hyphens(text)`: Cleans up hyphen-related issues in the text.
- `generate_bullet_points(text, max_length=100, num_beams=4)`: Generates bullet points either by directly converting shorter text to bullet points or summarizing and then converting the summary to bullet points using a pre-trained BART model.

**Usage:**
- The script reads an input CSV containing job descriptions and job responsibilities.
- It applies the `generate_bullet_points()` function to each row and saves the output to a new CSV.

**Input/Output:**
- Input: `/outputs/structured_output_with_summaries.csv`
- Output: `/outputs/structured_output_with_bullets.csv`

### 3. `prefect_server.py`

This script sets up a Prefect server workflow for processing jobs by scraping data and handling them with Prefect tasks.

**Key Components:**
- `process_job_data(job_url)`: A task that scrapes job data from a given URL.
- `process_links(input_csv)`: Reads a CSV of job URLs and processes each one by scraping and saving the data.
- `has_empty_attributes(data)`: Checks if scraped data has any empty attributes.

**Usage:**
- You can trigger this script as part of a larger Prefect flow.
- It reads job links from a CSV file and processes the scraped data to save it in structured format.

**Input/Output:**
- Input: `/outputs/output.csv`
- Output: `/outputs/structured_output_with_json.csv`

### 4. `scrape.py`

This script contains the logic for scraping job data from various websites. It is responsible for extracting structured information, formatting it into JSON, and saving it into a CSV file.

**Key Components:**
- Uses a scraping engine (`app.scrape_url()`) to fetch job data.
- Processes extracted job data and checks for completeness using `has_empty_attributes()`.

**Usage:**
- This script is triggered by `prefect_server.py` to scrape job listings from given URLs.
- It outputs structured JSON data and saves the result into a CSV file.

---

## Installation

1. Clone this repository.
2. Install the necessary dependencies:
    ```bash
    pip install pandas transformers prefect
    ```

## How to Run

1. **Generate Bullet Points:**
    ```bash
    python generate_bullet_points.py
    ```

2. **Start Prefect Server for Scraping:**
    ```bash
    python prefect_server.py
    ```









## Dependencies

- **Pandas**: For reading and writing CSV files.
- **Transformers (Hugging Face)**: To load the `BART` model for summarization.
- **Prefect**: For orchestrating workflows and managing tasks.
