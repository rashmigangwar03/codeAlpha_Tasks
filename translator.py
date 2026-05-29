from tkinter import *
from tkinter import ttk
from deep_translator import GoogleTranslator

# Main Window
root = Tk()
root.title("Language Translator")
root.geometry("600x450")
root.config(bg="white")

# Languages
languages = {
    "English": "en",
    "Hindi": "hi",
    "French": "fr",
    "Spanish": "es",
    "German": "de"
}

# Translate Function
def translate_text():

    text = entry.get()

    source = languages[source_lang.get()]
    target = languages[target_lang.get()]

    translated = GoogleTranslator(
        source=source,
        target=target
    ).translate(text)

    output_label.config(text=translated)

# Copy Function
def copy_text():

    translated_text = output_label.cget("text")

    root.clipboard_clear()
    root.clipboard_append(translated_text)

# Heading
heading = Label(
    root,
    text="Language Translator",
    font=("Arial", 22, "bold"),
    bg="white"
)

heading.pack(pady=20)

# Input Box
entry = Entry(
    root,
    width=40,
    font=("Arial", 16)
)

entry.pack(pady=10)

# Source Language
source_lang = ttk.Combobox(
    root,
    values=list(languages.keys()),
    font=("Arial", 12)
)

source_lang.pack(pady=5)
source_lang.set("English")

# Target Language
target_lang = ttk.Combobox(
    root,
    values=list(languages.keys()),
    font=("Arial", 12)
)

target_lang.pack(pady=5)
target_lang.set("Hindi")

# Translate Button
translate_btn = Button(
    root,
    text="Translate",
    font=("Arial", 12),
    command=translate_text
)

translate_btn.pack(pady=15)

# Output Label
output_label = Label(
    root,
    text="Translation Appears Here",
    font=("Arial", 16),
    bg="white",
    wraplength=500
)

output_label.pack(pady=20)

# Copy Button
copy_btn = Button(
    root,
    text="Copy Text",
    font=("Arial", 12),
    command=copy_text
)

copy_btn.pack(pady=5)

root.mainloop()