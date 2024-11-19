from transformers import BertTokenizer, BertForSequenceClassification, Trainer, TrainingArguments
import torch
import os
from extract_pdf import extract_text_from_pdf
from datasets import Dataset, DatasetDict

manual_labels = {
    "2401.14041.pdf": "positive",   # Paper with an optimistic tone or breakthrough
    "2306.02354-min.pdf": "neutral",   # Paper is purely informative, no strong sentiment
    "2310.16711-min.pdf": "neutral",
    "2104.06282-min.pdf": "neutral",
    "2201.12547.pdf": "positive",
    "2401.14041.pdf": "positive"
}

# Mapping of labels to integers for BERT
label_mapping = {"positive": 0, "neutral": 1, "negative": 2}

# Extract text, labels, and metadata from each paper
pdf_dir = "/Users/rogeriojorge/Dropbox/Papers_Read/Papers_To_Read"
papers = {}

for i, filename in enumerate(os.listdir(pdf_dir)):
    if filename.endswith('.pdf'):
        pdf_path = os.path.join(pdf_dir, filename)
        text = extract_text_from_pdf(pdf_path)
        # Assign label (manual or VADER as fallback)
        if filename in manual_labels:
            label = manual_labels[filename]
        else:
            continue
        #     label = get_sentiment_label_vader(text)
        papers[filename] = { 'text': text, 'label': label_mapping[label]}

# Prepare dataset for BERT
data = [{"text": paper['text'], "label": paper['label']} for paper in papers.values()]
dataset = Dataset.from_list(data)

# Split dataset into train and eval (e.g., 80-20 split)
train_test_split = dataset.train_test_split(test_size=0.2)
datasets = DatasetDict({
    "train": train_test_split["train"],
    "test": train_test_split["test"]
})

# Load a pre-trained model and tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=2)  # e.g., positive, neutral

# Tokenize dataset
def tokenize_function(examples):
    return tokenizer(examples["text"], padding="max_length", truncation=True)

tokenized_datasets = datasets.map(tokenize_function, batched=True)

# Training arguments
training_args = TrainingArguments(
    output_dir='./results',
    evaluation_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=8,
    num_train_epochs=3,
    weight_decay=0.01,
)

# Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets["train"],
    eval_dataset=tokenized_datasets["test"]
)

trainer.train()

# Save the trained model
model.save_pretrained("./trained_sentiment_model")
tokenizer.save_pretrained("./trained_sentiment_model")