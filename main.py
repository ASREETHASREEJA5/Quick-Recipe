import numpy as np
from langchain_groq import ChatGroq
import streamlit as st


llm = ChatGroq(
    temperature=0,
    groq_api_key='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',  # Replace with your actual Groq API key
    model_name="llama-3.1-70b-versatile"
)

# Function to gather user input
def gather_inputs():
    # Ask the user for basic recipe preferences
    st.title("Recipe Recommendation")
    
    # Input for what the user would like to prepare
    dish_type = st.text_input("What would you like to prepare? (e.g., vegan pasta, chicken curry)")

    # Number of people
    people_count = st.number_input("How many people are you cooking for?", min_value=1, step=1)

    # Time available for cooking
    time_available = st.number_input("How much time do you have? (in minutes)", min_value=1, step=5)

    # Dietary requirements dropdown
    dietary_requirements = st.selectbox(
        "Do you have any dietary requirements?",
        ("None", "Vegetarian", "Pescatarian", "Vegan", "Dairy-Free", "Gluten-Free", "Keto", "Paleo")
    )
    
    # Store the inputs as a dictionary
    user_input = {
        'dish_type': dish_type,
        'people_count': people_count,
        'time_available': time_available,
        'dietary_requirements': dietary_requirements
    }

    return user_input

# Function to generate the Llama prompt based on user inputs
def generate_response(user_input):
    # Extracting user inputs
    dish_type = user_input['dish_type']
    people_count = user_input['people_count']
    time_available = user_input['time_available']
    dietary_requirements = user_input['dietary_requirements']

    # Creating the Llama prompt
    prompt = f"""
    Generate a recipe for {dish_type} that serves {people_count} people. 
    The recipe should take approximately {time_available} minutes to prepare.
    The user has the following dietary requirements: {dietary_requirements}.
    
    The recipe should be structured as follows:

    Preparation Time:
    <Time in minutes>

    Difficulty:
    <Beginner/Intermediate/Advanced>

    Ingredients:
    <List of ingredients with quantities>

    Kitchen Tools Needed:
    <List of tools, e.g., pot, frying pan, etc.>

    Instructions:
    <Step-by-step preparation instructions>

    Macros:
    Total Calories: <calories>
    Carbs: <g>
    Proteins: <g>
    Fats: <g>
    """

    res = llm.invoke(prompt)
    return res.content

# Main Streamlit app
def main():
    user_input = gather_inputs()  # Collect user inputs

    if st.button("Get Recipe"):
        recipe = generate_response(user_input)

        # Display the recipe
        st.write(recipe)

# Run the app
if __name__ == "__main__":
    main()
