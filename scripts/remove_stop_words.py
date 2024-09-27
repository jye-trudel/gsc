import pandas as pd
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# ld
tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large")
model = AutoModelForSeq2SeqLM.from_pretrained("facebook/bart-large")


def remove_stop_words_with_bart(text, max_length=100, num_beams=4):
    if pd.isnull(text) or not text.strip():
        return ""


    prompt = f"Simplify: {text}"
    

    inputs = tokenizer.encode(prompt, return_tensors="pt", max_length=512, truncation=True)
    

    summary_ids = model.generate(inputs, max_length=max_length, num_beams=num_beams, early_stopping=True)
    

    simplified_text = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    simplified_text = simplified_text.replace("Simplify: ", "").strip()

    return simplified_text


input_csv = '/Users/jye/Desktop/scrape_v2/outputs/structured_output_with_bullets.csv'
df = pd.read_csv(input_csv)


df['job_description_clean'] = df['job_description'].apply(lambda x: remove_stop_words_with_bart(str(x)))


df['job_responsibilities_clean'] = df['job_responsibilities'].apply(lambda x: remove_stop_words_with_bart(str(x)))


output_csv = '/Users/jye/Desktop/scrape_v2/outputs/structured_output_with_stopwords_removed.csv'
df.to_csv(output_csv, index=False)

print(f"Stop words removed and saved to {output_csv}")
