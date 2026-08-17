import tkinter as tk
from tkinter import ttk, messagebox
from spellchecker import SpellChecker
import requests
import language_tool_python
import pyttsx3
import re
import os
import json


# ============================================================
# USER SETTINGS
# ============================================================

USERS_FILE = "users.json"
DICTIONARY_FOLDER = "user_dictionaries"

os.makedirs(DICTIONARY_FOLDER, exist_ok=True)


# ============================================================
# USER MANAGEMENT
# ============================================================

def load_users():
    if not os.path.exists(USERS_FILE):
        return []

    try:
        with open(USERS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except:
        return []


def save_users(users):
    with open(USERS_FILE, "w", encoding="utf-8") as file:
        json.dump(users, file, indent=4)


users = load_users()
current_user = None


# ============================================================
# LARGE NAME DATABASE
# ============================================================

PERSON_NAMES = {
    "aarav", "aadhya", "aanya", "aisha", "akshay",
    "amit", "amita", "ananya", "anika", "anjali",
    "anil", "ankit", "arjun", "arya", "ashish",
    "ayush", "deepak", "deepika", "diya", "gaurav",
    "harsh", "isha", "ishita", "jai", "karan",
    "kavya", "khushi", "meera", "neha", "nikhil",
    "nisha", "pooja", "pranav", "priya", "rahul",
    "raj", "rajesh", "ravi", "riya", "rohan",
    "rohit", "sahil", "sameer", "sana", "sanjay",
    "shreya", "simran", "sneha", "sonam", "tanvi",
    "vaishnavi", "sharnagat", "varun", "vijay",
    "vikas", "yash", "zoya"
}


# ============================================================
# GLOBAL VARIABLES
# ============================================================

spell = SpellChecker(language="en")
language_tool = None
engine = pyttsx3.init()

misspelled_words = []
current_word = None


# ============================================================
# LOAD USER DICTIONARY
# ============================================================

def get_dictionary_file():
    if not current_user:
        return None

    safe_name = re.sub(r"[^A-Za-z0-9_-]", "_", current_user)

    return os.path.join(
        DICTIONARY_FOLDER,
        safe_name + ".txt"
    )


def load_user_dictionary():

    global spell

    spell = SpellChecker(language="en")

    # Add names
    for name in PERSON_NAMES:
        spell.word_frequency.add(name)

    filename = get_dictionary_file()

    if filename and os.path.exists(filename):

        try:
            with open(
                filename,
                "r",
                encoding="utf-8"
            ) as file:

                for word in file:

                    word = word.strip().lower()

                    if word:
                        spell.word_frequency.add(word)

        except Exception as error:
            print("Dictionary error:", error)


# ============================================================
# LOGIN / USER CREATION
# ============================================================

def login():

    global current_user

    username = username_entry.get().strip()

    if not username:
        messagebox.showwarning(
            "Username",
            "Enter a username."
        )
        return

    current_user = username

    if username not in users:
        users.append(username)
        save_users(users)

    load_user_dictionary()

    login_window.destroy()

    create_main_window()


# ============================================================
# ADD CUSTOM WORD
# ============================================================

def add_custom_word():

    word = custom_word_entry.get().strip()

    if not word:
        return

    word = word.lower()

    spell.word_frequency.add(word)

    filename = get_dictionary_file()

    if filename:

        with open(
            filename,
            "a",
            encoding="utf-8"
        ) as file:

            file.write(word + "\n")

    custom_word_entry.delete(0, tk.END)

    messagebox.showinfo(
        "Dictionary",
        f"'{word}' added to your personal dictionary."
    )


# ============================================================
# LANGUAGE TOOL
# ============================================================

def create_language_tool(language_code):

    global language_tool

    try:

        language_tool = language_tool_python.LanguageTool(
            language_code
        )

    except Exception as error:

        language_tool = None

        messagebox.showwarning(
            "LanguageTool",
            f"AI spelling engine could not start.\n\n{error}"
        )


# ============================================================
# CHECK SPELLING
# ============================================================

def check_spelling():

    global misspelled_words

    text = input_text.get(
        "1.0",
        tk.END
    ).strip()

    if not text:

        messagebox.showwarning(
            "Warning",
            "Enter some text first."
        )

        return

    clear_highlights()

    misspelled_words = []

    # --------------------------------------------------------
    # Dictionary check
    # --------------------------------------------------------

    words = re.finditer(
        r"\b[A-Za-z]+\b",
        text
    )

    for match in words:

        word = match.group()

        if word.lower() not in spell:

            if word.lower() not in PERSON_NAMES:

                misspelled_words.append(word)

                start = f"1.0+{match.start()}c"
                end = f"1.0+{match.end()}c"

                input_text.tag_add(
                    "misspelled",
                    start,
                    end
                )

    # --------------------------------------------------------
    # AI / LanguageTool check
    # --------------------------------------------------------

    if language_tool:

        try:

            matches = language_tool.check(text)

            for match in matches:

                if match.rule_id in [
                    "MORFOLOGIK_RULE_EN_US",
                    "SPELLING"
                ]:

                    start = f"1.0+{match.offset}c"
                    end = (
                        f"1.0+"
                        f"{match.offset + match.errorLength}c"
                    )

                    input_text.tag_add(
                        "misspelled",
                        start,
                        end
                    )

                    word = text[
                        match.offset:
                        match.offset + match.errorLength
                    ]

                    if word not in misspelled_words:

                        misspelled_words.append(word)

        except Exception as error:
            print("LanguageTool error:", error)

    # --------------------------------------------------------
    # Suggestions
    # --------------------------------------------------------

    suggestion_list.delete(
        0,
        tk.END
    )

    for word in misspelled_words:

        suggestions = spell.candidates(
            word.lower()
        )

        if suggestions:

            for suggestion in list(
                suggestions
            )[:5]:

                suggestion_list.insert(
                    tk.END,
                    f"{word}  →  {suggestion}"
                )

    # --------------------------------------------------------
    # Statistics
    # --------------------------------------------------------

    total_words = len(
        re.findall(
            r"\b[A-Za-z]+\b",
            text
        )
    )

    errors = len(
        set(
            misspelled_words
        )
    )

    if total_words > 0:

        accuracy = (
            (total_words - errors)
            / total_words
        ) * 100

    else:
        accuracy = 100

    total_label.config(
        text=f"Total Words: {total_words}"
    )

    error_label.config(
        text=f"Spelling Errors: {errors}"
    )

    accuracy_label.config(
        text=f"Accuracy: {accuracy:.1f}%"
    )


# ============================================================
# AUTO CORRECT
# ============================================================

def auto_correct():

    text = input_text.get(
        "1.0",
        tk.END
    ).strip()

    if not text:
        return

    if language_tool:

        try:

            corrected = language_tool.correct(
                text
            )

            input_text.delete(
                "1.0",
                tk.END
            )

            input_text.insert(
                tk.END,
                corrected
            )

        except:
            dictionary_correction()

    else:

        dictionary_correction()

    check_spelling()


def dictionary_correction():

    text = input_text.get(
        "1.0",
        tk.END
    ).strip()

    words = text.split()

    corrected_words = []

    for word in words:

        match = re.match(
            r"^([^A-Za-z]*)([A-Za-z]+)([^A-Za-z]*)$",
            word
        )

        if not match:

            corrected_words.append(word)

            continue

        prefix = match.group(1)
        clean_word = match.group(2)
        suffix = match.group(3)

        if clean_word.lower() in spell:

            corrected_words.append(word)

        else:

            correction = spell.correction(
                clean_word.lower()
            )

            if correction:

                if clean_word[0].isupper():

                    correction = correction.capitalize()

                corrected_words.append(
                    prefix +
                    correction +
                    suffix
                )

            else:

                corrected_words.append(word)

    input_text.delete(
        "1.0",
        tk.END
    )

    input_text.insert(
        tk.END,
        " ".join(corrected_words)
    )


# ============================================================
# RIGHT CLICK SUGGESTIONS
# ============================================================

def show_context_menu(event):

    global current_word

    try:

        index = input_text.index(
            f"@{event.x},{event.y}"
        )

        start = input_text.index(
            f"{index} wordstart"
        )

        end = input_text.index(
            f"{index} wordend"
        )

        current_word = input_text.get(
            start,
            end
        )

        menu.delete(
            0,
            tk.END
        )

        suggestions = spell.candidates(
            current_word.lower()
        )

        if suggestions:

            for suggestion in list(
                suggestions
            )[:5]:

                menu.add_command(
                    label=suggestion,
                    command=lambda s=suggestion,
                    st=start,
                    en=end:
                    replace_word(
                        st,
                        en,
                        s
                    )
                )

        else:

            menu.add_command(
                label="No suggestions",
                state="disabled"
            )

        menu.add_separator()

        menu.add_command(
            label="Add to Dictionary",
            command=lambda:
            add_word_from_context(
                current_word
            )
        )

        menu.tk_popup(
            event.x_root,
            event.y_root
        )

    except:
        pass


def replace_word(
    start,
    end,
    replacement
):

    input_text.delete(
        start,
        end
    )

    input_text.insert(
        start,
        replacement
    )

    check_spelling()


def add_word_from_context(word):

    spell.word_frequency.add(
        word.lower()
    )

    filename = get_dictionary_file()

    if filename:

        with open(
            filename,
            "a",
            encoding="utf-8"
        ) as file:

            file.write(
                word.lower() + "\n"
            )

    check_spelling()


# ============================================================
# ONLINE DICTIONARY
# ============================================================

def online_dictionary():

    word = online_word_entry.get().strip()

    if not word:

        return

    try:

        url = (
            "https://api.dictionaryapi.dev/"
            "api/v2/entries/en/"
            + word
        )

        response = requests.get(
            url,
            timeout=10
        )

        if response.status_code != 200:

            online_result.delete(
                "1.0",
                tk.END
            )

            online_result.insert(
                tk.END,
                "Word not found."
            )

            return

        data = response.json()

        result = ""

        for entry in data:

            meanings = entry.get(
                "meanings",
                []
            )

            for meaning in meanings:

                part = meaning.get(
                    "partOfSpeech",
                    ""
                )

                result += (
                    f"Part of Speech: {part}\n"
                )

                definitions = meaning.get(
                    "definitions",
                    []
                )

                for definition in definitions[:3]:

                    result += (
                        "• "
                        + definition.get(
                            "definition",
                            ""
                        )
                        + "\n"
                    )

                result += "\n"

        online_result.delete(
            "1.0",
            tk.END
        )

        online_result.insert(
            tk.END,
            result
        )

    except Exception as error:

        messagebox.showerror(
            "Online Dictionary",
            str(error)
        )


# ============================================================
# COPY / PASTE
# ============================================================

def copy_text():

    text = input_text.get(
        "1.0",
        tk.END
    )

    root.clipboard_clear()

    root.clipboard_append(
        text
    )


def paste_text():

    try:

        text = root.clipboard_get()

        input_text.insert(
            tk.INSERT,
            text
        )

    except:

        messagebox.showwarning(
            "Paste",
            "Clipboard is empty."
        )


# ============================================================
# TEXT TO SPEECH
# ============================================================

def speak_text():

    text = input_text.get(
        "1.0",
        tk.END
    ).strip()

    if text:

        engine.say(text)

        engine.runAndWait()


# ============================================================
# CLEAR
# ============================================================

def clear_text():

    input_text.delete(
        "1.0",
        tk.END
    )

    suggestion_list.delete(
        0,
        tk.END
    )

    clear_highlights()


def clear_highlights():

    input_text.tag_remove(
        "misspelled",
        "1.0",
        tk.END
    )


# ============================================================
# LANGUAGE CHANGE
# ============================================================

def change_language(event=None):

    languages = {

        "English": "en-US",
        "Spanish": "es",
        "French": "fr",
        "German": "de",
        "Italian": "it",
        "Portuguese": "pt",
        "Russian": "ru"
    }

    selected = language_combo.get()

    code = languages.get(
        selected,
        "en-US"
    )

    # SpellChecker language
    try:

        global spell

        spell = SpellChecker(
            language=code.split("-")[0]
        )

        for name in PERSON_NAMES:

            spell.word_frequency.add(
                name
            )

        load_user_dictionary()

    except Exception as error:

        print(error)

    # LanguageTool
    create_language_tool(
        code
    )


# ============================================================
# MAIN GUI
# ============================================================

def create_main_window():

    global root
    global input_text
    global result_text
    global suggestion_list
    global language_combo
    global custom_word_entry
    global online_word_entry
    global online_result
    global total_label
    global error_label
    global accuracy_label
    global menu

    root = tk.Tk()

    root.title(
        f"AI Spell Checker - {current_user}"
    )

    root.geometry(
        "1000x850"
    )

    root.minsize(
        850,
        700
    )

    # --------------------------------------------------------
    # STYLE
    # --------------------------------------------------------

    style = ttk.Style()

    try:
        style.theme_use(
            "clam"
        )
    except:
        pass

    # --------------------------------------------------------
    # TITLE
    # --------------------------------------------------------

    title = ttk.Label(
        root,
        text="🧠 AI Dictionary Spell Checker",
        font=(
            "Segoe UI",
            24,
            "bold"
        )
    )

    title.pack(
        pady=15
    )

    user_label = ttk.Label(
        root,
        text=f"👤 User: {current_user}",
        font=(
            "Segoe UI",
            10
        )
    )

    user_label.pack()

    # --------------------------------------------------------
    # LANGUAGE
    # --------------------------------------------------------

    language_frame = ttk.Frame(
        root
    )

    language_frame.pack(
        pady=10
    )

    ttk.Label(
        language_frame,
        text="🌍 Language:"
    ).pack(
        side=tk.LEFT,
        padx=5
    )

    language_combo = ttk.Combobox(
        language_frame,
        values=[
            "English",
            "Spanish",
            "French",
            "German",
            "Italian",
            "Portuguese",
            "Russian"
        ],
        state="readonly",
        width=15
    )

    language_combo.set(
        "English"
    )

    language_combo.pack(
        side=tk.LEFT
    )

    language_combo.bind(
        "<<ComboboxSelected>>",
        change_language
    )

    # --------------------------------------------------------
    # INPUT
    # --------------------------------------------------------

    ttk.Label(
        root,
        text="Enter Text",
        font=(
            "Segoe UI",
            12,
            "bold"
        )
    ).pack(
        anchor="w",
        padx=30
    )

    input_text = tk.Text(
        root,
        height=10,
        font=(
            "Segoe UI",
            12
        ),
        wrap=tk.WORD
    )

    input_text.pack(
        fill=tk.X,
        padx=30,
        pady=8
    )

    input_text.tag_config(
        "misspelled",
        foreground="red",
        underline=True
    )

    # Right click
    input_text.bind(
        "<Button-3>",
        show_context_menu
    )

    # Context menu
    menu = tk.Menu(
        root,
        tearoff=0
    )

    # --------------------------------------------------------
    # BUTTONS
    # --------------------------------------------------------

    button_frame = ttk.Frame(
        root
    )

    button_frame.pack(
        pady=10
    )

    ttk.Button(
        button_frame,
        text="🔍 Check",
        command=check_spelling
    ).grid(
        row=0,
        column=0,
        padx=5
    )

    ttk.Button(
        button_frame,
        text="✨ Auto Correct",
        command=auto_correct
    ).grid(
        row=0,
        column=1,
        padx=5
    )

    ttk.Button(
        button_frame,
        text="📋 Copy",
        command=copy_text
    ).grid(
        row=0,
        column=2,
        padx=5
    )

    ttk.Button(
        button_frame,
        text="📋 Paste",
        command=paste_text
    ).grid(
        row=0,
        column=3,
        padx=5
    )

    ttk.Button(
        button_frame,
        text="🔊 Speak",
        command=speak_text
    ).grid(
        row=0,
        column=4,
        padx=5
    )

    ttk.Button(
        button_frame,
        text="🧹 Clear",
        command=clear_text
    ).grid(
        row=0,
        column=5,
        padx=5
    )

    # --------------------------------------------------------
    # SUGGESTIONS
    # --------------------------------------------------------

    ttk.Label(
        root,
        text="💡 Spelling Suggestions",
        font=(
            "Segoe UI",
            12,
            "bold"
        )
    ).pack(
        anchor="w",
        padx=30
    )

    suggestion_list = tk.Listbox(
        root,
        height=6,
        font=(
            "Segoe UI",
            11
        )
    )

    suggestion_list.pack(
        fill=tk.X,
        padx=30,
        pady=5
    )

    # --------------------------------------------------------
    # STATISTICS
    # --------------------------------------------------------

    statistics_frame = ttk.LabelFrame(
        root,
        text="📊 Spelling Statistics"
    )

    statistics_frame.pack(
        fill=tk.X,
        padx=30,
        pady=10
    )

    total_label = ttk.Label(
        statistics_frame,
        text="Total Words: 0"
    )

    total_label.pack(
        side=tk.LEFT,
        padx=20,
        pady=10
    )

    error_label = ttk.Label(
        statistics_frame,
        text="Spelling Errors: 0"
    )

    error_label.pack(
        side=tk.LEFT,
        padx=20
    )

    accuracy_label = ttk.Label(
        statistics_frame,
        text="Accuracy: 100%"
    )

    accuracy_label.pack(
        side=tk.LEFT,
        padx=20
    )

    # --------------------------------------------------------
    # CUSTOM DICTIONARY
    # --------------------------------------------------------

    custom_frame = ttk.LabelFrame(
        root,
        text="🔐 Personal Dictionary"
    )

    custom_frame.pack(
        fill=tk.X,
        padx=30,
        pady=8
    )

    custom_word_entry = ttk.Entry(
        custom_frame,
        width=30
    )

    custom_word_entry.pack(
        side=tk.LEFT,
        padx=10,
        pady=10
    )

    ttk.Button(
        custom_frame,
        text="Add Custom Word / Name",
        command=add_custom_word
    ).pack(
        side=tk.LEFT
    )

    # --------------------------------------------------------
    # ONLINE DICTIONARY
    # --------------------------------------------------------

    online_frame = ttk.LabelFrame(
        root,
        text="📖 Online Dictionary"
    )

    online_frame.pack(
        fill=tk.X,
        padx=30,
        pady=8
    )

    online_word_entry = ttk.Entry(
        online_frame,
        width=25
    )

    online_word_entry.pack(
        side=tk.LEFT,
        padx=10,
        pady=10
    )

    ttk.Button(
        online_frame,
        text="Search",
        command=online_dictionary
    ).pack(
        side=tk.LEFT,
        padx=5
    )

    online_result = tk.Text(
        online_frame,
        height=4,
        font=(
            "Segoe UI",
            10
        )
    )

    online_result.pack(
        fill=tk.X,
        padx=10,
        pady=5
    )

    root.mainloop()


# ============================================================
# LOGIN WINDOW
# ============================================================

login_window = tk.Tk()

login_window.title(
    "Spell Checker Login"
)

login_window.geometry(
    "400x250"
)

login_window.resizable(
    False,
    False
)

tk.Label(
    login_window,
    text="🧠 Spell Checker",
    font=(
        "Segoe UI",
        22,
        "bold"
    )
).pack(
    pady=25
)

tk.Label(
    login_window,
    text="Enter your username"
).pack()

username_entry = tk.Entry(
    login_window,
    width=30,
    font=(
        "Segoe UI",
        12
    )
)

username_entry.pack(
    pady=10
)

tk.Button(
    login_window,
    text="Login / Create User",
    command=login,
    font=(
        "Segoe UI",
        11,
        "bold"
    ),
    padx=15,
    pady=7
).pack(
    pady=10
)

login_window.mainloop()