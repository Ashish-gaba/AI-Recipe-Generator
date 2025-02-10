import streamlit as st
import requests

st.title("AI-Powered Nutrition Assistant")

# User input fields
ingredients = st.text_input("Enter ingredients (e.g., oats, chia seeds):")
diet_type = st.selectbox("Select Diet Type:", ["High-Protein", "Vegan", "Keto", "Paleo", "Mediterranean"])
llm_model = st.selectbox("Choose LLM Model:", ["GPT-4", "Llama-2", "Claude-3", "DeepSeek R1"])
meal_type = st.selectbox("Select Meal Type:", ["Breakfast", "Lunch", "Dinner", "Snack"])
calorie_limit = st.number_input("Enter Calorie Limit (Optional):", min_value=0, value=500, step=50)
api_url = st.text_input("Enter API URL:", "http://localhost:5000")

if st.button("Generate Recipe"):
    if not ingredients.strip():
        st.error("Please enter at least one ingredient.")
    else:
        with st.spinner("Fetching recipes..."):
            try:
                response = requests.post(f"{api_url}/api/get-recipe", json={
                    "ingredients": ingredients, 
                    "dietType": diet_type, 
                    "mealType": meal_type,
                    "calorieLimit": calorie_limit,
                    "model": llm_model
                })
                response.raise_for_status()
                data = response.json()
                
                if "recipes" not in data or not isinstance(data["recipes"], list):
                    raise ValueError("Invalid recipe data received")
                
                for recipe in data["recipes"]:
                    st.subheader(recipe["name"])
                    st.write(recipe["instructions"])
                    
                    # Fetch nutrition data
                    nutrition_response = requests.post(f"{api_url}/api/get-nutrition", json={
                        "recipeName": recipe["name"], 
                        "model": llm_model
                    })
                    nutrition_response.raise_for_status()
                    nutrition_data = nutrition_response.json()
                    
                    st.write(f"Calories: {nutrition_data.get('calories', 'N/A')} kcal")
                    st.write(f"Protein: {nutrition_data.get('protein', 'N/A')}g")
                    st.write(f"Carbs: {nutrition_data.get('carbs', 'N/A')}g")
                    st.write(f"Fats: {nutrition_data.get('fats', 'N/A')}g")
                    st.markdown("---")
            except requests.exceptions.ConnectionError:
                st.error("Failed to connect to the API. Please check the API URL and ensure the server is running.")
            except requests.exceptions.RequestException as e:
                st.error(f"Error fetching recipes: {e}")
