import openai

openai.api_key = ''

def analyze_sentiment(text, stars):
    try:
        prompt = f"""
        Analyze the tone and sentiment of the following review text with {stars}
        
        Text: {text}
        """
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        
        result = response.choices[0].message.content.strip()
        tone = result.split('\n')[0].split(': ')[1]
        sentiment = result.split('\n')[1].split(': ')[1]
        
        return tone, sentiment
    except Exception as e:
        return None, None
