import google.generativeai as genai
import PIL.Image
import os

# আপনার API Key এখানে বসান
genai.configure(api_key="YOUR_API_KEY_HERE")

def analyze_image(image_path, user_query="এই ছবিটি বিস্তারিত বর্ণনা করো"):
    model = genai.GenerativeModel('gemini-1.5-flash')
    img = PIL.Image.open(image_path)
    
    # প্রম্পটটি বাংলায় সেট করা যাতে উত্তর বাংলায় আসে
    prompt = f"উত্তরটি বাংলায় দাও। প্রশ্ন: {user_query}"
    
    response = model.generate_content([prompt, img])
    return response.text