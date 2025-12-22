# Project 10: Word Counter 📊

Welcome to Project 10! This app counts words, characters, sentences, and paragraphs in text!

## What is This Project? 🤔

**Word Counter** = An app that analyzes text and counts various statistics!

**Think of it like:**
- **Text Analysis** = Understanding your text
- **Statistics** = Numbers about your text
- **Counting** = How many words, characters, etc.

**Counter = Analyzes and counts text!**

## What You'll Learn 📚

✅ String manipulation
✅ Text processing
✅ List operations
✅ String methods (split, strip, replace)
✅ Conditional logic
✅ Text analysis
✅ Statistics calculation

## What This App Does 🎯

1. **Enter Text** - User enters or pastes text
2. **Count Words** - Counts number of words
3. **Count Characters** - Counts with/without spaces
4. **Count Sentences** - Counts sentences
5. **Count Paragraphs** - Counts paragraphs
6. **Display Statistics** - Shows all counts

**Features:**
- 📝 Word count
- 🔤 Character count (with/without spaces)
- 📄 Sentence count
- 📑 Paragraph count
- 📊 Beautiful statistics display

## Step-by-Step Explanation 📖

### Step 1: Count Words
```python
def count_words(text):
    words = text.split()
    return len(words)
```
**What this does:**
- Splits text by spaces
- Counts number of words
- Returns word count

**Simple explanation:**
- Split = Break into words
- Count = How many words!

### Step 2: Count Characters
```python
def count_characters(text, include_spaces=True):
    if include_spaces:
        return len(text)
    else:
        return len(text.replace(' ', ''))
```
**What this does:**
- Counts all characters
- Option to include/exclude spaces
- Returns character count

**Simple explanation:**
- Characters = All letters, numbers, symbols
- With spaces = Includes spaces
- Without spaces = Excludes spaces!

### Step 3: Count Sentences
```python
def count_sentences(text):
    sentence_endings = ['.', '!', '?']
    count = 0
    for char in text:
        if char in sentence_endings:
            count += 1
    return count
```
**What this does:**
- Looks for sentence endings
- Counts periods, exclamation marks, question marks
- Returns sentence count

**Simple explanation:**
- Sentence = Ends with . ! or ?
- Count = How many sentences!

### Step 4: Count Paragraphs
```python
def count_paragraphs(text):
    paragraphs = text.split('\n\n')
    return len(paragraphs)
```
**What this does:**
- Splits by double newlines
- Counts paragraphs
- Returns paragraph count

**Simple explanation:**
- Paragraph = Separated by blank line
- Count = How many paragraphs!

## Key Concepts 🎓

### 1. String Methods

**split():**
```python
text.split()  # Split by spaces
text.split('\n\n')  # Split by double newlines
```
- Breaks string into list
- Separates by delimiter

**strip():**
```python
text.strip()  # Remove whitespace
```
- Removes spaces from ends
- Cleans text

**replace():**
```python
text.replace(' ', '')  # Remove spaces
```
- Replaces characters
- Can remove characters

### 2. List Comprehensions

**What are they?**
- Compact way to create lists
- Filter and transform data

**Example:**
```python
words = [word for word in words if word.strip()]
```
- Loops through list
- Filters out empty strings
- Creates new list

### 3. Text Analysis

**What is it?**
- Processing text data
- Extracting information
- Counting elements

**Simple explanation:**
- Analysis = Understanding text
- Counting = Getting numbers!

## How to Run 🚀

### Step 1: Install Flask
```bash
pip install -r requirements.txt
```

### Step 2: Run the App
```bash
python app.py
```

### Step 3: Open in Browser
Visit: `http://127.0.0.1:5000`

**How to use:**
1. Enter or paste text in textarea
2. Click "Count Words" button
3. View detailed statistics!

## Files in This Project 📁

```
10-word-counter/
├── app.py              # Main Flask application
├── requirements.txt     # Dependencies
├── templates/           # HTML templates
│   └── index.html      # Word counter form and results
├── static/              # CSS stylesheet
│   └── style.css       # Stylesheet
└── README.md           # This file
```

## Next Steps 🎯

After completing this project:

1. ✅ Try different texts
2. ✅ Compare statistics
3. ✅ Test with long texts
4. ✅ You've completed 10 beginner projects! 🎉

---

**Congratulations! You've completed 10 beginner projects! 🎉**

