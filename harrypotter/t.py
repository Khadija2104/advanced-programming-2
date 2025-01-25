from io import BytesIO
import requests
import tkinter as tk
from tkinter import messagebox
import pygame
from PIL import Image, ImageTk
pygame.mixer.init()

# Load and play the background music
pygame.mixer.music.load("game-music.mp3")
pygame.mixer.music.play(-1)

# Initial setup - hide content_frame and result_frame initially
def search_harry_potter():
    category = search_option.get().lower()
    search_name = search_entry.get().strip().lower()

    if not search_name:
        messagebox.showinfo("Error", "Please enter a search term.")
        return

    try:
        # Construct URL based on the category (spells or potions)
        if category == "characters":
            api_url = f"https://api.potterdb.com/v1/characters/{search_name.replace(' ', '-')}"
        elif category == "spells":
            api_url = f"https://api.potterdb.com/v1/spells/{search_name.replace(' ', '-')}"
        elif category == "potions":
            api_url = f"https://api.potterdb.com/v1/potions/{search_name.replace(' ', '-')}"
        else:
            raise ValueError("Unknown category.")

        response = requests.get(api_url)
        data = response.json()

        if "data" not in data or not data["data"]:
            messagebox.showinfo("Error", f"{category.capitalize()} not found.")
        else:
            result = data["data"]

            # Debugging the response to check data
            print(f"API Response: {data}")  # Debug print for the full API response

            # Extracting attributes based on the category
            if category == "characters":
                name = result.get('attributes', {}).get('name', 'N/A')
                alias_names = result.get('attributes', {}).get('alias_names', [])
                image_url = result.get('attributes', {}).get("image", None)
                description_text = "\n".join(alias_names) if alias_names else "No alias names available"
                type_text = "Character"
            elif category == "spells":
                name = result.get('attributes', {}).get('name', 'N/A')
                category = result.get('attributes', {}).get('category', 'N/A')
                effect = result.get('attributes', {}).get('effect', 'N/A')
                image_url = result.get('attributes', {}).get("image", None)
                wiki_url = result.get('attributes', {}).get("wiki", None)
                description_text = f"Effect: {effect}\nWiki: {wiki_url}" if wiki_url else f"Effect: {effect}"
                type_text = "Spell"
            elif category == "potions":
                name = result.get('attributes', {}).get('name', 'N/A')
                characteristics = result.get('attributes', {}).get('characteristics', 'N/A')
                effect = result.get('attributes', {}).get('effect', 'N/A')
                ingredients = result.get('attributes', {}).get('ingredients', 'N/A')
                side_effects = result.get('attributes', {}).get('side_effects', 'N/A')
                image_url = result.get('attributes', {}).get("image", None)
                wiki_url = result.get('attributes', {}).get("wiki", None)
                description_text = f"Effect: {effect}\nIngredients: {ingredients}\nSide Effects: {side_effects}\nWiki: {wiki_url}" if wiki_url else f"Effect: {effect}\nIngredients: {ingredients}\nSide Effects: {side_effects}"
                type_text = "Potion"

            # Update UI with results
            title_label.config(text=f"Name: {name}")
            type_label.config(text=f"Type: {type_text}")

            description_label.config(text=f"Details:\n{description_text}")

            # Update the result box with the description
            result_box.delete(1.0, tk.END)
            result_box.insert(tk.END, description_text)

            # Load and display the image if available
            if image_url:
                try:
                    image_data = requests.get(image_url, timeout=10).content
                    image = Image.open(BytesIO(image_data))
                    image.thumbnail((300, 450))
                    poster_photo = ImageTk.PhotoImage(image)
                    poster_label.config(image=poster_photo, text="")  # Remove "No Image Available"
                    poster_label.image = poster_photo
                except Exception as e:
                    poster_label.config(text="Failed to load image", image="")
            else:
                poster_label.config(text="No Image Available", image="")

            # Show the content_frame and result_frame after results are fetched
            content_frame.pack(fill="x", padx=20, pady=20)
            result_frame.pack(fill="both", padx=20, pady=10)

    except Exception as e:
        messagebox.showinfo("Error", "An error occurred while fetching the data.")
        print(e)

def open_category(category):
    search_option.set(category.lower())  
    search_entry.delete(0, tk.END) 

    # Add default static value based on category
    if category.lower() == "characters":
        search_entry.insert(0, "harry-potter")  # Example static search term for Characters
    elif category.lower() == "spells":
        search_entry.insert(0, "age-line")  # Example static search term for Spells
    elif category.lower() == "potions":
        search_entry.insert(0, "felix-felicis")  # Example static search term for Potions

    search_harry_potter()  # Trigger search after selecting category

# Main window setup
window = tk.Tk()
window.title("Harry Potter Searcher")
window.geometry("1200x800")

# Add a background image
background_url = "https://img.freepik.com/free-photo/education-day-scene-fantasy-style-aesthetic_23-2151040233.jpg?semt=ais_hybrid"
response = requests.get(background_url)
bg_image = ImageTk.PhotoImage(Image.open(BytesIO(response.content)).resize((1200, 800)))
background_label = tk.Label(window, image=bg_image)
background_label.place(relwidth=1, relheight=1)

# Sidebar
sidebar = tk.Frame(window, bg="#1c1c1c", width=200)
sidebar.pack(side="left", fill="y")

sidebar_label = tk.Label(sidebar, text="Categories", font=("Arial", 18, "bold"), bg="#1c1c1c", fg="white")
sidebar_label.pack(pady=20)

categories = ["Characters", "Spells", "Potions"]
for category in categories:
    button = tk.Button(
        sidebar,
        text=category,
        font=("Arial", 16),
        bg="#333333",
        fg="white",
        anchor="w",
        command=lambda c=category: open_category(c)
    )
    button.pack(fill="x", pady=5, padx=10)

# Search bar
search_frame = tk.Frame(window, bg="#ffe599")
search_frame.pack(pady=20)

search_option = tk.StringVar(value="characters")
search_label = tk.Label(search_frame, text="Search for:", font=("Arial", 16), bg="#ffe599")
search_label.pack(side="left", padx=10)

search_entry = tk.Entry(search_frame, font=("Arial", 16), width=30)
search_entry.pack(side="left", padx=10)

search_menu = tk.OptionMenu(search_frame, search_option, "characters", "spells", "potions")
search_menu.config(font=("Arial", 14), bg="#5a8dff", fg="white")
search_menu.pack(side="left", padx=10)

search_button = tk.Button(search_frame, text="Search", font=("Arial", 14), bg="#5a8dff", fg="white", command=search_harry_potter)
search_button.pack(side="left", padx=10)

# Content frame with further reduced height
content_frame = tk.Frame(window, bg="#ffe599", height=150)  # Further reduced height
content_frame.pack_forget()  # Hide it initially

# Poster on the left with much smaller height and width
poster_label = tk.Label(content_frame, bg="#ffe599", width=150, height=150)  # No initial text or image
poster_label.pack(side="left", padx=10)

# Details on the right with smaller font size
details_frame = tk.Frame(content_frame, bg="#ffe599")
details_frame.pack(side="left", fill="both", expand=True, padx=10)

# Further reduced font size for title, type, and description
title_label = tk.Label(details_frame, text="", font=("Arial", 12), bg="#ffe599", anchor="w")  # Further smaller font size
title_label.pack(fill="x", pady=3)

type_label = tk.Label(details_frame, text="", font=("Arial", 12), bg="#ffe599", anchor="w")  # Further smaller font size
type_label.pack(fill="x", pady=3)

description_label = tk.Label(details_frame, text="", font=("Arial", 12), bg="#ffe599", anchor="w")  # Further smaller font size
description_label.pack(fill="x", pady=3)

# Result box at the bottom with scrollbar
result_frame = tk.Frame(window)
result_frame.pack_forget()  # Hide it initially

result_box = tk.Text(result_frame, font=("Arial", 18), wrap="word", bg="white", height=8)
result_box.pack(side="left", fill="both", expand=True)

# Add scrollbar to the result box
scrollbar = tk.Scrollbar(result_frame, command=result_box.yview)
scrollbar.pack(side="right", fill="y")
result_box.config(yscrollcommand=scrollbar.set)

window.mainloop()
