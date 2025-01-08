import numpy as np
from langchain_groq import ChatGroq
import streamlit as st
from dotenv import load_dotenv
import os


load_dotenv()


groq_api_key = os.getenv('GROQ_API_KEY')


llm = ChatGroq(
    temperature=0,
    groq_api_key=groq_api_key,  # Replace with your actual Groq API key
    model_name="llama-3.1-70b-versatile"
)


def add_background_image(image_url):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("{image_url}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


def gather_inputs():
    st.title("**Recipe Recommendation ChatBot**")
    st.markdown(
        """
        **Welcome to the Recipe Recommendation Chat Bot! 🥗**  
        Fill in your preferences below, and we'll generate a personalized recipe for you.
        """
    )

    
    dish_type = st.text_input("**What would you like to prepare? (e.g., vegan pasta, Biryani)**", key="dish")

    people_count = st.slider("**How many people are you cooking for?**", min_value=1, max_value=10, step=1)

    time_available = st.number_input("**How much time do you have? (in minutes)**", min_value=1, step=5)

    dietary_requirements = st.multiselect(
        "**Select any dietary requirements:**",
        ["None", "Vegetarian", "Pescatarian", "Vegan", "Dairy-Free", "Gluten-Free", "Keto", "Paleo"],
        default="None"
    )

    user_input = {
        'dish_type': dish_type,
        'people_count': people_count,
        'time_available': time_available,
        'dietary_requirements': ", ".join(dietary_requirements) if dietary_requirements else "None"
    }

    return user_input


def generate_response(user_input):

    dish_type = user_input['dish_type']
    people_count = user_input['people_count']
    time_available = user_input['time_available']
    dietary_requirements = user_input['dietary_requirements']


    prompt = f"""
    Generate a recipe for **{dish_type}** that serves **{people_count}** people. 
    The recipe should take approximately **{time_available}** minutes to prepare.
    The user has the following dietary requirements: **{dietary_requirements}**.
    
    The recipe should be structured as follows:

    **Preparation Time:**
    <Time in minutes>

    **Difficulty:**
    <Beginner/Intermediate/Advanced>

    **Ingredients:**
    <List of ingredients with quantities>

    **Kitchen Tools Needed:**
    <List of tools, e.g., pot, frying pan, etc.>

    **Instructions:**
    <Step-by-step preparation instructions>

    **Macros:**
    **Total Calories:** <calories>
    **Carbs:** <g>
    **Proteins:** <g>
    **Fats:** <g>
    """

    res = llm.invoke(prompt)
    return res.content


def main():

    add_background_image("https://img.freepik.com/premium-photo/cooking-ingredient-white-table-background_826551-2435.jpg?w=900")

    user_input = gather_inputs()  

    if st.button("**🍴 Generate My Recipe**"):
        with st.spinner("**Generating your recipe...**"):
            recipe = generate_response(user_input)

        st.success("**Here’s your personalized recipe! 🍽️**")
        st.markdown(f"### **{user_input['dish_type'].capitalize()}**")
        st.markdown(f"**{recipe}**")


if __name__ == "__main__":
    main()
