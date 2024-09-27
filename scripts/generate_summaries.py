import pandas as pd
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

# bart large model
tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large-cnn")
model = AutoModelForSeq2SeqLM.from_pretrained("facebook/bart-large-cnn")

summarizer = pipeline("summarization", model=model, tokenizer=tokenizer)

input_csv = '/Users/jye/Desktop/scrape_v2/outputs/structured_output_with_json.csv'
output_csv = '/Users/jye/Desktop/scrape_v2/outputs/structured_output_with_summaries.csv'

df = pd.read_csv(input_csv)

df['summarized_description'] = ''
df['summarized_responsibilities'] = ''

for index, row in df.iterrows():
    try:
        description_summary = summarizer(row['job_description'], max_length=150, min_length=50, do_sample=False)[0]['summary_text']
        df.at[index, 'summarized_description'] = description_summary
    except Exception as e:
        print(f"Error summarizing description for row {index}: {e}")

    try:
        responsibilities_summary = summarizer(row['job_responsibilities'], max_length=150, min_length=50, do_sample=False)[0]['summary_text']
        df.at[index, 'summarized_responsibilities'] = responsibilities_summary
    except Exception as e:
        print(f"Error summarizing responsibilities for row {index}: {e}")

df.to_csv(output_csv, index=False)

print(f"Summaries added and saved to {output_csv}")
