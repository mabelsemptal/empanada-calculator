
import streamlit as st

# --- Auth ---
def check_login(username, password):
    return username == "mabel" and password == "Mabelita1967"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("Empanada Calculator - Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if check_login(username, password):
            st.session_state.logged_in = True
            st.experimental_rerun()
        else:
            st.error("Invalid credentials.")
    st.stop()

# --- App ---
st.title("Empanada Ingredient Calculator")
st.markdown("_Bienvenida, Mabel 😊_")

language = st.radio("Language / Idioma", ["English", "Spanish"], horizontal=True)

labels = {
    "English": {
        "Beef": "Beef", "Chicken": "Chicken", "Spicy Beef": "Spicy Beef", "Spinach": "Spinach",
        "Amount": "Amount of meat/spinach (grams)",
        "Calculate": "Calculate",
        "Ingredients": "Ingredients for",
        "units": "units", "grams": "grams"
    },
    "Spanish": {
        "Beef": "Carne", "Chicken": "Pollo", "Spicy Beef": "Carne Picante", "Spinach": "Espinaca",
        "Amount": "Cantidad de carne/espinaca (gramos)",
        "Calculate": "Calcular",
        "Ingredients": "Ingredientes para",
        "units": "unidades", "grams": "gramos"
    }
}

lang = labels[language]

empanada_type = st.selectbox(lang["Ingredients"], [lang["Beef"], lang["Chicken"], lang["Spicy Beef"], lang["Spinach"]])
amount = st.number_input(lang["Amount"], min_value=0)

def get_ingredients(emp_type, grams):
    if emp_type == lang["Beef"]:
        multiplier = grams / 2268
        return {
            "Onion": 1400,
            "Red Pepper": 475,
            "Oil": 360,
            "Salt (Onion)": 7,
            "Salt (Meat)": 17,
            "Paprika": 16,
            "Brown Sugar": 17,
            "Eggs": 9,
            "Olives": 300
        }, multiplier

    elif emp_type == lang["Spicy Beef"]:
        multiplier = grams / 2268
        return {
            "Onion": 1400,
            "Red Pepper": 475,
            "Oil": 360,
            "Salt (Onion)": 7,
            "Salt (Meat)": 17,
            "Cayenne Pepper": 16,
            "Brown Sugar": 17,
            "Eggs": 9,
            "Olives": 300
        }, multiplier

    elif emp_type == lang["Chicken"]:
        multiplier = grams / 1500
        return {
            "Onion": 750,
            "Oil": 240,
            "Salt (Onion)": 6,
            "Salt (Meat)": 11,
            "Brown Sugar": 13,
            "Paprika": 12,
            "Eggs": 6
        }, multiplier

    elif emp_type == lang["Spinach"]:
        multiplier = grams / 1250
        return {
            "Oil": 245,
            "Onion": 1300,
            "Red Pepper": 500,
            "Brown Sugar": 12,
            "Paprika (in onion)": 5,
            "Paprika (at end)": 11,
            "Nutmeg": 50,
            "Eggs": 8
        }, multiplier

    return {}, 1

if st.button(lang["Calculate"]):
    ingredients, factor = get_ingredients(empanada_type, amount)
    st.subheader(f"{lang['Ingredients']} {int(amount)}g {empanada_type.lower()}:")
    output = ""
    for item, qty in ingredients.items():
        unit = "units" if item == "Eggs" else "grams"
        total = round(qty * factor, 2)
        unit_out = lang["units"] if unit == "units" else lang["grams"]
        output += f"- {item}: {total} {unit_out}\n"
    st.text_area("Result", value=output.strip(), height=250)
    st.download_button("📥 Download as text", output, file_name="empanada_ingredients.txt")
