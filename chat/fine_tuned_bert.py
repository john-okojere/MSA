import os
import torch
from transformers import BertTokenizer, BertForSequenceClassification, Trainer, TrainingArguments
from datasets import Dataset
import pandas as pd
from sklearn.model_selection import train_test_split
import nltk

# Load the dataset
dataset_path = '../data/Dataset.txt'  # Adjust path if necessary
with open(dataset_path, 'r', errors='ignore') as f:
    raw_doc = f.read()

# Sample preprocessing (adjust as needed)
nltk.download('punkt')

# Split data (this is a simplified example)
sentences = nltk.sent_tokenize(raw_doc)
labels = [0] * len(sentences)  # Placeholder labels; adapt based on your dataset

# Create a DataFrame
data = pd.DataFrame({'text': sentences, 'label': labels})

# Split into training and test sets
train_texts, val_texts, train_labels, val_labels = train_test_split(
    data['text'], data['label'], test_size=0.2, random_state=42
)

# Tokenize and encode the data
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

def encode_data(texts, labels):
    encodings = tokenizer(texts.tolist(), truncation=True, padding=True, max_length=512)
    dataset = Dataset.from_dict({
        'input_ids': encodings['input_ids'],
        'attention_mask': encodings['attention_mask'],
        'labels': labels.tolist()
    })
    return dataset

# Create datasets
train_dataset = encode_data(train_texts, train_labels)
val_dataset = encode_data(val_texts, val_labels)

# Initialize BERT model
model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=2)

# Set up training arguments
training_args = TrainingArguments(
    output_dir='./results',  # Directory where the model checkpoints will be saved
    per_device_train_batch_size=8,
    num_train_epochs=3,
    logging_dir='./logs',    # Directory for storing logs
)

# Create Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset
)

# Train the model
trainer.train()

# Ensure the directory exists
output_dir = './fine_tuned_bert'
os.makedirs(output_dir, exist_ok=True)

# Save the model
model.save_pretrained(output_dir)
tokenizer.save_pretrained(output_dir)
