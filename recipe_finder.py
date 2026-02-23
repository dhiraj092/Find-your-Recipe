import streamlit as st
from openai import OpenAI
from typing import List, Optional, Dict, Tuple

def initialize_openai() -> Optional[OpenAI]:
    try:
        return OpenAI(api_key=st.secrets['api_key'])
    except Exception as e:
        st.error(f"Failed to initialize OpenAI client: {str(e)}")
        return None

def get_available_basics(cols: tuple) -> List[str]:
    ingredients = {
        'Salt': True, 'Pepper': True, 'Cooking Oil': True, 'Garlic': True,
        'Onion': False, 'Butter': False, 'Common Herbs': False, 'Stock/Broth': False
    }
    
    col1, col2 = cols
    checkboxes = {}
    
    with col1:
        for item in list(ingredients.keys())[:4]:
            checkboxes[item] = st.checkbox(item, value=ingredients[item])
    with col2:
        for item in list(ingredients.keys())[4:]:
            checkboxes[item] = st.checkbox(item, value=ingredients[item])
            
    return [k.lower() for k, v in checkboxes.items() if v]

def get_possible_cuisines(client: OpenAI, ingredients: str, basics: List[str]) -> List[str]:
    try:
        prompt = f"""
        Main ingredients: {ingredients}
        Basic ingredients: {', '.join(basics)}
        
        List 5 different cuisines that could make dishes with these ingredients.
        Format: cuisine1|cuisine2|cuisine3|cuisine4|cuisine5
        """
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a culinary expert who analyzes ingredients and suggests possible cuisines."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        
        cuisines = response.choices[0].message.content.strip().split('|')
        return [cuisine.strip() for cuisine in cuisines]
    except Exception as e:
        st.error(f"Error getting cuisines: {str(e)}")
        return []

def create_recipe_prompt(main_ingredients: str, available_basics: List[str], cuisine: str) -> str:
    return f"""
    Main ingredients: {main_ingredients}
    Basic ingredients: {', '.join(available_basics)}
    Requested cuisine: {cuisine}

    Create a {cuisine} recipe that:
    1. Uses the main ingredients
    2. Only uses the basic ingredients listed
    3. Suggests substitutes for missing ingredients
    
    Format as:
    RECIPE NAME:
    COOKING TIME:
    DIFFICULTY:
    
    INGREDIENTS:
    (list with quantities)
    
    POSSIBLE SUBSTITUTIONS:
    (if needed)
    
    INSTRUCTIONS:
    (numbered steps)
    """

def get_video_search_terms(client: OpenAI, recipe_name: str, cuisine: str) -> List[str]:
    try:
        prompt = f"""
        For the recipe "{recipe_name}" from {cuisine} cuisine, provide 3 different YouTube search terms that would help find relevant cooking videos.
        Format them as: term1|term2|term3
        Make them specific but varied, including both the dish name and some alternatives.
        """
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a cooking content expert who knows how to find the best cooking videos."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        
        search_terms = response.choices[0].message.content.strip().split('|')
        return [term.strip() for term in search_terms]
    except Exception as e:
        st.error(f"Error generating video search terms: {str(e)}")
        return []

def generate_recipe(client: OpenAI, prompt: str) -> Tuple[Optional[str], Optional[str]]:
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a creative chef specializing in the requested cuisine."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=800
        )
        recipe_text = response.choices[0].message.content
        
        # Extract recipe name from the generated text
        recipe_name = ""
        for line in recipe_text.split('\n'):
            if line.startswith("RECIPE NAME:"):
                recipe_name = line.replace("RECIPE NAME:", "").strip()
                break
                
        return recipe_text, recipe_name
    except Exception as e:
        st.error(f"Error generating recipe: {str(e)}")
        return None, None

def display_video_suggestions(search_terms: List[str]):
    st.subheader("📺 Suggested Cooking Videos")
    st.write("Search for these terms on YouTube to find helpful cooking videos:")
    
    for i, term in enumerate(search_terms, 1):
        st.markdown(f"{i}. `{term}`")
        video_url = f"https://www.youtube.com/results?search_query={term.replace(' ', '+')}"
        st.markdown(f"[🎥 Watch videos for: {term}]({video_url})")

def main():
    st.set_page_config(page_title="AI Recipe Finder", layout="wide")
    
    st.markdown("""
        <style>
        .stButton>button { width: 100%; margin-top: 20px; }
        </style>
    """, unsafe_allow_html=True)
    
    st.title("🧑‍🍳 AI Recipe Finder")
    st.write("Enter ingredients to discover recipes from different cuisines!")
    
    client = initialize_openai()
    if not client:
        st.stop()
    
    main_ingredients = st.text_input(
        "What main ingredients do you have?",
        placeholder="e.g., chicken, pasta, tomatoes"
    )
    
    st.subheader("Common Pantry Items")
    cols = st.columns(2)
    available_basics = get_available_basics(cols)
    
    if 'cuisines' not in st.session_state:
        st.session_state.cuisines = None
    
    if st.button("🔍 Find Possible Cuisines"):
        if not main_ingredients.strip():
            st.warning("⚠️ Please enter main ingredients first!")
            st.stop()
        
        with st.spinner("👨‍🍳 Analyzing possible cuisines..."):
            st.session_state.cuisines = get_possible_cuisines(client, main_ingredients, available_basics)
    
    if st.session_state.cuisines:
        selected_cuisine = st.selectbox(
            "Select a cuisine type:",
            options=st.session_state.cuisines
        )
        
        if st.button("📝 Generate Recipe"):
            with st.spinner("Creating your recipe..."):
                prompt = create_recipe_prompt(main_ingredients, available_basics, selected_cuisine)
                recipe, recipe_name = generate_recipe(client, prompt)
                
                if recipe and recipe_name:
                    st.success(f"✨ Here's your {selected_cuisine} recipe!")
                    st.markdown(recipe)
                    
                    # Get and display video suggestions
                    with st.spinner("Finding video suggestions..."):
                        search_terms = get_video_search_terms(client, recipe_name, selected_cuisine)
                        if search_terms:
                            display_video_suggestions(search_terms)
                    
                    st.download_button(
                        label="📥 Download Recipe",
                        data=recipe,
                        file_name=f"{selected_cuisine}_recipe.txt",
                        mime="text/plain"
                    )

if __name__ == "__main__":
    main()