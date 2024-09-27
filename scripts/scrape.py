import pandas as pd
import os
import json
from firecrawl import FirecrawlApp
from pydantic import BaseModel
from dotenv import load_dotenv


load_dotenv()
api_key = os.getenv('FIRECRAWL_API_KEY')
app = FirecrawlApp(api_key=api_key)

#app = FirecrawlApp(api_key='') --> replaced with env

class ExtractSchema(BaseModel):
    job_name: str
    job_location: str
    job_description: str
    qualifications: str
    job_responsibilities: str

def has_empty_attributes(data):
    """Check if any attribute in the scraped data is empty."""
    for key, value in data.items():
        if value is None or value == '':
            print(f"Skipping job due to empty attribute: {key}")
            return True
    return False

def process_links(input_csv):
    try:
        df = pd.read_csv(input_csv)
        print(f"CSV loaded successfully from {input_csv}")

        if 'link' not in df.columns:
            raise ValueError("CSV must contain a 'link' column with job URLs.")
        
        all_data = []

        for index, row in df.iterrows():
            job_url = row['link']
            print(f"Processing: {job_url}")

            try:
                data = app.scrape_url(job_url, {
                    'formats': ['extract'],
                    'extract': {
                        'schema': ExtractSchema.model_json_schema(),
                    }
                })
                print(f"Scraped data for {job_url}: {data['extract']}")
                
                if has_empty_attributes(data['extract']):
                    print(f"Job at {job_url} has empty attributes and will be skipped.")
                    continue 

                structured_json = json.dumps(data['extract']) 
                

                data_with_json = data['extract']
                data_with_json['structured_schema_json'] = structured_json
                all_data.append(data_with_json)

            except Exception as e:
                print(f"Error scraping {job_url}: {e}")


        if all_data:
            output_df = pd.DataFrame(all_data)
            output_csv = os.path.join(os.path.dirname(input_csv), 'structured_output_with_json.csv')
            
            try:
                output_df.to_csv(output_csv, index=False)
                print(f"CSV saved successfully at {output_csv}")
            except Exception as e:
                print(f"Error saving CSV: {e}")
        else:
            print("No data was scraped, nothing to save.")


        if os.path.exists(input_csv):
            os.remove(input_csv)
            print(f"{input_csv} deleted.")
        else:
            print(f"File {input_csv} not found.")

    except Exception as e:
        print(f"Error reading or processing CSV: {e}")

if __name__ == "__main__":
    input_csv = '/Users/jye/Desktop/scrape_v2/outputs/output.csv'
    print(f"Starting process for {input_csv}")
    process_links(input_csv)
