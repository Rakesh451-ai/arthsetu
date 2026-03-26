import random

# Knowledge Base - Indian Financial Concepts
knowledge_base = {
    "fd": {
        "english": "Fixed Deposit (FD) is like keeping your money in a safe locker that grows slowly. Banks give you 6-7% interest. Your money is safe and guaranteed.",
        "hindi": "फिक्स्ड डिपॉजिट (FD) पैसे को सुरक्षित तिजोरी में रखने जैसा है जो धीरे-धीरे बढ़ता है। बैंक आपको 6-7% ब्याज देते हैं। आपका पैसा पूरी तरह सुरक्षित है।"
    },
    "sip": {
        "english": "SIP (Systematic Investment Plan) is like planting a money tree. You invest a small amount (₹500) every month in mutual funds. Over time, it grows through compounding.",
        "hindi": "SIP (सिस्टमैटिक इन्वेस्टमेंट प्लान) पैसे का पेड़ लगाने जैसा है। आप हर महीने म्यूचुअल फंड में छोटी रकम (₹500) निवेश करते हैं। समय के साथ यह कंपाउंडिंग से बढ़ता है।"
    },
    "mutual fund": {
        "english": "Mutual funds pool money from many people to invest in stocks, bonds, etc. It's like a kitchen garden where experts grow your money. Returns can be 10-12% but can go up and down.",
        "hindi": "म्यूचुअल फंड कई लोगों का पैसा इकट्ठा करके शेयरों, बॉन्ड आदि में निवेश करता है। यह एक किचन गार्डन जैसा है जहां एक्सपर्ट आपका पैसा बढ़ाते हैं। रिटर्न 10-12% हो सकता है लेकिन उतार-चढ़ाव होता है।"
    },
    "ppf": {
        "english": "PPF (Public Provident Fund) is a government savings scheme. You invest for 15 years, get around 7-8% interest, and pay NO tax on returns. Perfect for long-term goals like retirement.",
        "hindi": "PPF (पब्लिक प्रोविडेंट फंड) सरकारी बचत योजना है। आप 15 साल के लिए निवेश करते हैं, 7-8% ब्याज मिलता है, और रिटर्न पर कोई टैक्स नहीं लगता। रिटायरमेंट जैसे लंबे लक्ष्यों के लिए बेहतरीन है।"
    },
    "tax saving": {
        "english": "Save tax under Section 80C by investing in: PPF (up to ₹1.5L), ELSS mutual funds, Life Insurance, or National Savings Certificate. You can save up to ₹46,800 in taxes!",
        "hindi": "सेक्शन 80C के तहत टैक्स बचाएं: PPF (₹1.5L तक), ELSS म्यूचुअल फंड, लाइफ इंश्योरेंस, या नेशनल सेविंग्स सर्टिफिकेट में निवेश करें। आप ₹46,800 तक टैक्स बचा सकते हैं!"
    },
    "credit card": {
        "english": "Credit card is like borrowing money for 30-50 days without interest. Use wisely: pay FULL bill on time, never withdraw cash, and enjoy rewards. Defaulting hurts your credit score!",
        "hindi": "क्रेडिट कार्ड 30-50 दिन के लिए बिना ब्याज के पैसा उधार लेने जैसा है। समझदारी से use करें: पूरा बिल समय पर भरें, कभी कैश न निकालें, रिवॉर्ड्स का मज़ा लें। चूक से आपका क्रेडिट स्कोर खराब होता है!"
    }
}

# Simple responses for other questions
greetings = ["namaste", "hello", "hi", "hey", "नमस्ते"]
thank_you = ["thanks", "thank you", "dhanyavaad", "शुक्रिया"]

def get_response(question, language="English"):
    """
    Simple AI response function
    """
    question_lower = question.lower()
    
    # Check for greetings
    if any(word in question_lower for word in greetings):
        responses = {
            "English": "Namaste! I'm Arthsetu, your financial guide. Ask me anything about money, investments, or savings!",
            "Hindi": "नमस्ते! मैं अर्थसेतु हूं, आपका वित्तीय मार्गदर्शक। मुझसे पैसे, निवेश या बचत के बारे में कुछ भी पूछिए!",
            "Hinglish": "Namaste! Main Arthsetu hoon, aapka financial guide. Mujhse paise, investment ya savings ke baare mein kuch bhi poochiye!"
        }
        return responses.get(language, responses["English"])
    
    # Check for thank you
    if any(word in question_lower for word in thank_you):
        responses = {
            "English": "You're welcome! Keep learning and growing your money. Anything else I can help with?",
            "Hindi": "आपका स्वागत है! सीखते रहें और अपना पैसा बढ़ाते रहें। क्या और मदद चाहिए?",
            "Hinglish": "Aapka swagat hai! Seekhte raho aur apna paisa badhate raho. Aur kya madad chahiye?"
        }
        return responses.get(language, responses["English"])
    
    # Check knowledge base
    for key, value in knowledge_base.items():
        if key in question_lower:
            return value.get(language.lower(), value["english"])
    
    # Default response for unknown questions
    default_responses = {
        "English": f"I'm learning about that! For now, remember: Start small, be consistent, and always invest in what you understand. Want to know about FD, SIP, PPF, or Tax Saving?",
        "Hindi": f"मैं इसके बारे में सीख रहा हूँ! अभी के लिए याद रखें: छोटी शुरुआत करें, नियमित रहें, और हमेशा वही निवेश करें जो आप समझते हैं। FD, SIP, PPF, या Tax Saving के बारे में जानना चाहेंगे?",
        "Hinglish": f"Main iske baare mein seekh raha hoon! Abhi ke liye yaad rakho: chhoti shuruaat karo, regular raho, aur hamesha wahi invest karo jo tum samjhte ho. FD, SIP, PPF, ya Tax Saving ke baare mein janna chahoge?"
    }
    return default_responses.get(language, default_responses["English"])