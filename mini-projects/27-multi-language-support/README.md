# Project 27: Multi-language Support 🌍

Welcome to Project 27! This app supports multiple languages using Flask-Babel!

## What is This Project? 🤔

**Multi-language Support** = An app that displays content in different languages!

**Think of it like:**
- **Languages** = Different translations
- **Switching** = Change language
- **Localization** = Adapt to language

**Multi-language = Support for many languages!**

## What You'll Learn 📚

✅ Internationalization (i18n)
✅ Localization (l10n)
✅ Flask-Babel
✅ Translation files
✅ Language detection
✅ Date/time formatting

## What This App Does 🎯

1. **Language Selection** - Choose from multiple languages
2. **Content Translation** - Display content in selected language
3. **Date/Time Formatting** - Format dates according to language
4. **Browser Detection** - Auto-detect browser language
5. **Session Storage** - Remember language preference

**Features:**
- 🌍 Multiple languages (English, Spanish, French, German)
- 🔄 Language switching
- 📅 Localized date/time formatting
- 🌐 Browser language detection
- 💾 Session-based language storage

## Step-by-Step Explanation 📖

### Step 1: Flask-Babel Setup
```python
from flask_babel import Babel, gettext as _
babel = Babel(app)
```
**What this does:**
- Initializes Babel
- Enables translation support
- Sets up i18n system

**Simple explanation:**
- Babel = Translation system
- Setup = Configure!

### Step 2: Language Selection
```python
@babel.localeselector
def get_locale():
    return session.get('language', 'en')
```
**What this does:**
- Determines current language
- Checks session
- Falls back to default

**Simple explanation:**
- Selector = Choose language
- Session = Remember choice!

### Step 3: Translation
```python
_('Welcome')
```
**What this does:**
- Translates text
- Uses current language
- Returns translated string

**Simple explanation:**
- Translate = Convert text
- Language = Current language!

## Key Concepts 🎓

### 1. Internationalization (i18n)

**What is i18n?**
- Making app support multiple languages
- Preparing for translation
- Using translation functions

**How it works:**
- Wrap text in translation functions
- Create translation files
- Babel handles the rest

### 2. Localization (l10n)

**What is l10n?**
- Adapting to specific language
- Date/time formatting
- Number formatting

**How it works:**
- Format dates according to locale
- Use locale-specific formats
- Adapt to cultural norms

### 3. Translation Files

**What are translation files?**
- .po files (Portable Object)
- Contain translations
- One file per language

**Structure:**
- msgid = Original text
- msgstr = Translated text

## How to Run 🚀

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Compile Translations
```bash
pybabel compile -d translations
```
**Note:** This compiles .po files to .mo files (binary format)

### Step 3: Run the App
```bash
python app.py
```

### Step 4: Open in Browser
Visit: `http://127.0.0.1:5000`

**How to use:**
1. Select language from dropdown
2. See content update
3. View localized date/time
4. Language preference is saved!

## Files in This Project 📁

```
27-multi-language-support/
├── app.py              # Main Flask application
├── requirements.txt     # Dependencies
├── templates/           # HTML templates
│   └── index.html      # Main page with translations
├── static/              # CSS stylesheet
│   └── style.css       # Stylesheet
├── translations/        # Translation files
│   ├── en/             # English translations
│   ├── es/             # Spanish translations
│   ├── fr/             # French translations
│   └── de/             # German translations
└── README.md           # This file
```

## Next Steps 🎯

After completing this project:

1. ✅ Test language switching
2. ✅ Understand translation files
3. ✅ Learn about i18n/l10n
4. ✅ Move to Project 28: API with JWT Authentication

---

**Ready for the next project? Try Project 28: API with JWT Authentication!**

