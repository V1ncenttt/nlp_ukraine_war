import torch
from torch.utils.data import DataLoader, RandomSampler, SequentialSampler, TensorDataset
from transformers import BertTokenizer, BertForSequenceClassification, AdamW
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from seaborn import heatmap

# Load your dataset
df = pd.read_csv("data/training_aggregated.csv")
df.loc[df["sentiment"] == -1, "sentiment"] = 2

# Tokenization and Input Formatting
tokenizer = BertTokenizer.from_pretrained("bert-base-multilingual-cased")

# Tokenize all texts and map the labels
input_ids = []
attention_masks = []
labels = []

for text, label in zip(df["text"], df["sentiment"]):
    encoded_dict = tokenizer.encode_plus(
        text,
        add_special_tokens=True,
        max_length=64,
        pad_to_max_length=True,
        return_attention_mask=True,
        return_tensors="pt",
    )

    input_ids.append(encoded_dict["input_ids"])
    attention_masks.append(encoded_dict["attention_mask"])
    labels.append(label)

# Convert lists to tensors
input_ids = torch.cat(input_ids, dim=0)
attention_masks = torch.cat(attention_masks, dim=0)
labels = torch.tensor(labels)

# Split data into train and validation sets
train_inputs, validation_inputs, train_labels, validation_labels = train_test_split(
    input_ids, labels, random_state=2018, test_size=0.1
)
train_masks, validation_masks, _, _ = train_test_split(
    attention_masks, labels, random_state=2018, test_size=0.1
)

# Create DataLoaders
batch_size = 32
train_data = TensorDataset(train_inputs, train_masks, train_labels)
train_sampler = RandomSampler(train_data)
train_dataloader = DataLoader(train_data, sampler=train_sampler, batch_size=batch_size)

validation_data = TensorDataset(validation_inputs, validation_masks, validation_labels)
validation_sampler = SequentialSampler(validation_data)
validation_dataloader = DataLoader(
    validation_data, sampler=validation_sampler, batch_size=batch_size
)

# Load BertForSequenceClassification, the pretrained BERT model with a single linear classification layer on top
model = BertForSequenceClassification.from_pretrained(
    "bert-base-multilingual-cased",
    num_labels=3,
    output_attentions=False,
    output_hidden_states=False,
)

# If you have a GPU, put everything on cuda
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# Optimizer & Learning Rate Scheduler
optimizer = AdamW(model.parameters(), lr=2e-5, eps=1e-8)

# Training Loop
# Note: This is a simplified version of the training loop
for epoch_i in range(0, 4):
    # Training
    model.train()
    for step, batch in enumerate(train_dataloader):
        b_input_ids = batch[0].to(device)
        b_input_mask = batch[1].to(device)
        b_labels = batch[2].to(device)
        model.zero_grad()
        outputs = model(
            b_input_ids,
            token_type_ids=None,
            attention_mask=b_input_mask,
            labels=b_labels,
        )
        loss = outputs.loss
        loss.backward()
        optimizer.step()

# Evaluation
model.eval()
predictions, true_labels = [], []

for batch in validation_dataloader:
    batch = tuple(t.to(device) for t in batch)
    b_input_ids, b_input_mask, b_labels = batch
    with torch.no_grad():
        outputs = model(b_input_ids, token_type_ids=None, attention_mask=b_input_mask)
    logits = outputs.logits
    logits = logits.detach().cpu().numpy()
    label_ids = b_labels.to("cpu").numpy()
    predictions.append(logits)
    true_labels.append(label_ids)

# Flatten the predictions and true values for aggregate classification report
flat_predictions = np.concatenate(predictions, axis=0)
flat_predictions = np.argmax(flat_predictions, axis=1).flatten()
flat_true_labels = np.concatenate(true_labels, axis=0)

# Confusion Matrix
cm = confusion_matrix(flat_true_labels, flat_predictions)
plt.figure(figsize=(8, 8))
heatmap(cm, annot=True, fmt="g", cmap="Blues")
plt.xlabel("Predicted labels")
plt.ylabel("True labels")
plt.show()
