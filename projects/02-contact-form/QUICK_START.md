# Quick Start Guide 🚀

## Get Your Contact Form Running in 3 Steps!

### Step 1: Install Flask

Open your terminal and run:
```bash
pip install flask
```

**That's it! Flask is installed!**

### Step 2: Run Your Application

Navigate to the project folder:
```bash
cd projects/02-contact-form
```

Run the app:
```bash
python app.py
```

**You should see:**
```
 * Running on http://127.0.0.1:5000
```

### Step 3: Open in Browser

Open your web browser and go to:
```
http://localhost:5000
```

**Your contact form is live! 🎉**

## What You Can Do

1. **Fill out the form** - Enter your name, email, and message
2. **Upload a file** - Attach a file (optional)
3. **Submit** - Send your message
4. **View messages** - Click "Messages" to see all received messages

## Testing the Form

1. Go to `http://localhost:5000/contact`
2. Fill out the form:
   - Name: Your name
   - Email: your.email@example.com
   - Message: Test message
   - File: (optional) Upload any allowed file
3. Click "Send Message"
4. You should see a success message!
5. Click "Messages" to see your message

## File Upload Test

Try uploading different file types:
- ✅ Allowed: txt, pdf, png, jpg, jpeg, gif, doc, docx
- ❌ Not allowed: exe, zip, etc.

## Next Steps

1. **Read PROJECT_GUIDE.md** - Learn how everything works
2. **Customize** - Change form fields and styling
3. **Add validation** - More form checks
4. **Deploy** - Put it online!

## Troubleshooting

### "ModuleNotFoundError: No module named 'flask'"
**Solution:** Run `pip install flask` again

### "Port already in use"
**Solution:** Close other Flask apps or change port:
```python
app.run(debug=True, port=5001)
```

### File upload not working
**Solution:** Make sure `static/uploads/` folder exists (it's created automatically)

### Messages not showing
**Solution:** Make sure `data/messages.json` exists (it's created automatically)

---

**Have fun with your contact form! 📧**

