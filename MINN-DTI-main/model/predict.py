import torch
from torch import nn
import numpy as np
from sklearn.preprocessing import LabelEncoder
import pandas as pd
import streamlit as st

def main():
    # Title for the Streamlit app
    st.title("DRUG PROTEIN INTERACTION PREDICTION")

    # Input fields for the user to enter strings
    string1 = st.text_input("Enter drug in SMILES format")
    string2 = st.text_input("Enter the PROTEIN sequence")

    # Button to perform concatenation
    if st.button("predict"):
        if string1 and string2:
            # Define the model
             class RNNModel(nn.Module):
                 def __init__(self, input_dim, embed_dim, hidden_dim, output_dim):
                    super(RNNModel, self).__init__()
                    self.embedding = nn.Embedding(input_dim, embed_dim)
                    self.lstm = nn.LSTM(embed_dim, hidden_dim, batch_first=True)
                    self.fc = nn.Linear(hidden_dim, output_dim)

                    def forward(self, x):
                        x = self.embedding(x)
                        _, (h_n, _) = self.lstm(x)
                        x = self.fc(h_n[-1])
                        return x

                    def tokenize_sequences(sequences, fixed_len):
                         tokenizer = LabelEncoder()
                         all_chars = set(''.join(sequences))
                         tokenizer.fit(list(all_chars))
                         tokenized = [tokenizer.transform(list(seq)) for seq in sequences]
                         padded = np.array([np.pad(x, (0, fixed_len - len(x)), mode='constant', constant_values=0) for x in tokenized])
                         return padded
# Load the trained model
                    input_dim = 124
                    embed_dim = 64
                    hidden_dim = 128
                    output_dim = 1
                    model = RNNModel(input_dim, embed_dim, hidden_dim, output_dim)
                    model.load_state_dict(torch.load('rnn_model.pth'))
                    model.eval()  # Set the model to evaluation mode

# Example input data
                    input_smiles = string1
                    input_proteins = string2
# Tokenize the input data
                    max_length = max(max(len(s) for s in input_smiles), max(len(s) for s in input_proteins))
                    input_smiles_tensor = torch.tensor(tokenize_sequences(input_smiles, max_length), dtype=torch.long)
                    input_proteins_tensor = torch.tensor(tokenize_sequences(input_proteins, max_length), dtype=torch.long)

# Make predictions
                    with torch.no_grad():
                        combined_input = torch.cat((input_smiles_tensor, input_proteins_tensor), dim=1)
                        outputs = model(combined_input)
                        predicted_probabilities = torch.sigmoid(outputs).squeeze().numpy()
                 st.success(f"Activity Probability: {""}")
        else:
            st.error("Please enter Valid inputs")

if __name__ == "__main__":
    main()
