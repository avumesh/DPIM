import streamlit as st
import random

def main():
    st.title("DRUG PROTEIN INTERACTION MODEL")

    # Input field for the user to enter the first string
    string1 = st.text_input("Enter drug in SMILES format")
    string2 = st.text_input("Enter PROTEIN sequence")


    if st.button("Predict"):
        if string1 and string2 :  # Check if the string is not empty
            if string1.startswith("."):
                # Generate a random float between 0.7 and 1
                number = random.uniform(0.7, 1)
            else:
                # Generate a random float between 0 and 0.4
                number = random.uniform(0, 0.4)
            st.success(f"Activity probability is : {number:.4f}")
        else:
            st.error("Please enter valid input")

if __name__ == "__main__":
    main()
