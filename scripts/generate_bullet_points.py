import pandas as pd
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large-cnn")
model = AutoModelForSeq2SeqLM.from_pretrained("facebook/bart-large-cnn")

def clean_hyphens(text):
    # enhyphen handling cause thats an issue?
    text = text.replace("- -", "-").strip()
    text = text.replace("--", "-").strip()
    text = text.replace("- ", "-").strip()
    return text


def generate_bullet_points(text, max_length=100, num_beams=4):
    #nc
    if pd.isnull(text) or not text.strip():
        return ""
    
    # if short alr js convert to bp
    if len(text.split(',')) <= 8:  # can adjust
        bullet_points = text.split(',')
        return "\n".join([f"- {point.strip()}" for point in bullet_points if point])
    
    # sum
    inputs = tokenizer.encode("summarize: " + text, return_tensors="pt", max_length=512, truncation=True)
    summary_ids = model.generate(inputs, max_length=max_length, num_beams=num_beams, early_stopping=True)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    
    # remove problem prefixes
    summary = summary.replace("Summarize:", "").strip()
    
    summary = clean_hyphens(summary)
    
    bullet_points = summary.split('. ')
    bullet_points = [f"- {point.strip()}" for point in bullet_points if point]
    
    
    return "\n".join(bullet_points)

# load
input_csv = '/Users/jye/Desktop/scrape_v2/outputs/structured_output_with_summaries.csv'
df = pd.read_csv(input_csv)

df['job_description_bullets'] = df['job_description'].apply(lambda x: generate_bullet_points(str(x)))
df['job_responsibilities_bullets'] = df['job_responsibilities'].apply(lambda x: generate_bullet_points(str(x)))

# save to file
output_csv = '/Users/jye/Desktop/scrape_v2/outputs/structured_output_with_bullets.csv'
df.to_csv(output_csv, index=False)

print(f"Bullet points generated and saved to {output_csv}")
