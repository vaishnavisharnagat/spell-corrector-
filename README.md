# 📝 AI-Based Spell Corrector

A **Python-based Spell Corrector** with a modern graphical user interface that detects and corrects spelling mistakes. The application provides intelligent suggestions, custom dictionaries, spelling statistics, multilingual support, and online dictionary integration.

## ✨ Features

* 🧠 **AI-Based Spelling Correction**
* 👤 **Large Personal-Name Database**
* 🌍 **Multiple Language Support**
* 📖 **Online Dictionary Integration**
* 🖱️ **Right-Click Spelling Suggestions**
* 🎨 **Modern GUI**
* 📊 **Spelling Statistics**
* 🔐 **User-Specific Custom Dictionary**
* 🔍 Automatic spelling-error detection
* 💡 Multiple correction suggestions
* 📋 Easy text editing
* ⚡ Fast and lightweight

## 🛠️ Technologies Used

* **Python 3**
* **Tkinter** – Graphical User Interface
* **PySpellChecker** – Spell checking
* **NLTK** – Natural Language Processing
* **Requests** – Online dictionary/API integration
* **JSON** – Custom dictionary and user data storage

## 📂 Project Structure

```text
Spell-Corrector/
│
├── spell_corrector.py
├── custom_dictionary.json
├── names_database.json
├── requirements.txt
├── README.md
└── screenshots/
    └── spell_corrector.png
```

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone [https://github.com/yourusername/spell-corrector](https://github.com/vaishnavisharnagat/spell-corrector-.git)
```

### 2. Open the Project Folder

```bash
cd spell-corrector
```

### 3. Install Required Libraries

```bash
pip install -r requirements.txt
```

Or install the libraries individually:

```bash
pip install pyspellchecker nltk requests
```

### 4. Run the Application

```bash
python spell_corrector.py
```

## 📖 How It Works

1. Enter or paste text into the text editor.
2. The application identifies possible spelling mistakes.
3. Incorrect words are highlighted.
4. Right-click on an incorrect word to view suggestions.
5. Select the required suggestion.
6. The application replaces the incorrect word automatically.
7. Spelling statistics are updated automatically.

## 🧠 AI-Based Correction

The spell corrector analyzes incorrect words and generates possible corrections based on:

* Word similarity
* Dictionary vocabulary
* Word frequency
* Context
* Personal dictionary
* Name database

This helps provide more accurate spelling suggestions than simple dictionary matching.

## 👤 Personal Name Database

The application includes support for commonly used personal names.

For example:

```text
Vaishnavi
Rahul
Aarav
Priya
Sneha
```

Names can be added to the personal-name database so that valid names are not incorrectly marked as spelling mistakes.

## 🌍 Multiple Language Support

The application can be extended to support multiple languages such as:

* 🇬🇧 English
* 🇮🇳 Hindi
* 🇫🇷 French
* 🇩🇪 German
* 🇪🇸 Spanish

Language dictionaries can be added depending on the requirements of the project.

## 📖 Online Dictionary

The project can use an online dictionary API to retrieve additional word information.

Possible information includes:

* Word definition
* Meaning
* Example sentence
* Pronunciation
* Synonyms

An internet connection is required for online dictionary features.

## 🖱️ Right-Click Suggestions

When a spelling mistake is detected:

```text
Right Click → Suggestions → Select Correct Word
```

Example:

```text
Wrong:  recieve

Suggestions:
✓ receive
✓ receiver
```

## 📊 Spelling Statistics

The application can display statistics such as:

```text
Total Words       : 150
Correct Words     : 143
Misspelled Words  : 7
Corrections Made  : 6
Accuracy          : 95.33%
```

This helps users track their writing accuracy.

## 🔐 Custom Dictionary

Users can add their own words to a personal dictionary.

For example:

```text
Add Word → Vaishnavi
Add Word → Sinhgad
Add Word → CodSoft
```

Custom words are stored and can be reused when the application is started again.

## 🖥️ User Interface

The application provides an easy-to-use interface containing:

* Text editor
* Check Spelling button
* Correct All button
* Language selection
* Statistics section
* Custom Dictionary option
* Right-click suggestions

## 📦 Requirements

Create a `requirements.txt` file:

```text
pyspellchecker
nltk
requests
```

Install everything using:

```bash
pip install -r requirements.txt
```

## 🚀 Future Improvements

* 🤖 Advanced AI/ML-based context correction
* 🗣️ Voice-based spelling correction
* 📱 Mobile application
* 🌐 More language support
* ✍️ Grammar correction
* 🔊 Text-to-speech
* 📚 Larger vocabulary database
* ☁️ Cloud synchronization
* 👥 Multiple user profiles

## 🎯 Use Cases

This project can be useful for:

* Students
* Content writers
* Bloggers
* Developers
* Teachers
* Office users
* English learners

## 🔒 Privacy

The basic spell-checking functionality can work locally without sending text to an external service. Online dictionary functionality may send individual words to a third-party API when enabled.


## 📄 License

This project is open-source and available under the **MIT License**.

## 👩‍💻 Author

**Vaishnavi Sharnagat**

B.E. Information Technology Student

## ⭐ Support

If you found this project useful, please consider giving the repository a ⭐ **Star** on GitHub!

```text
⭐ Star the repository
🍴 Fork the project
🐛 Report issues
💡 Suggest improvements
```
