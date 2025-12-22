# Quick Start Guide 🚀

Get your Multi-language Support app running in 4 steps!

## Step 1: Install Dependencies 📦

```bash
pip install -r requirements.txt
```

## Step 2: Compile Translations 🔧

```bash
pybabel compile -d translations
```

**Note:** This compiles .po files to .mo files (binary format) that Flask-Babel can use.

## Step 3: Run the App ▶️

```bash
python app.py
```

## Step 4: Open in Browser 🌐

Visit: `http://127.0.0.1:5000`

**How to use:**
1. Select a language from the dropdown (English, Spanish, French, German)
2. See content update in selected language
3. View localized date/time formatting
4. Your language preference is saved in the session!

---

**That's it! You've built a multi-language app! 🎉**

