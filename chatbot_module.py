import nltk
from nltk.stem import WordNetLemmatizer
import pickle
import numpy as np
from keras.models import load_model
import json
import random
import pyttsx3

# Load the NLP model and data
try:
    model = load_model('Batch2.h5')
    intents = json.loads(open('first_aid.json').read())
    words = pickle.load(open('words1.pkl', 'rb'))
    classes = pickle.load(open('classes1.pkl', 'rb'))
except Exception as e:
    raise RuntimeError(f"Failed to load model or data files: {str(e)}")

lemmatizer = WordNetLemmatizer()

def clean_up_sentence(sentence, lemmatizer):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

def bow(sentence, words, show_details=True):
    sentence_words = clean_up_sentence(sentence, lemmatizer)
    bag = [0]*len(words)
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s:
                bag[i] = 1
                if show_details:
                    print("found in bag: %s" % w)
    return np.array(bag)

def predict_class(sentence, model):
    p = bow(sentence, words, show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(i['tag']== tag):
            result = random.choice(i['responses'])
            break
    return result

def extract_link(response):
    if '<a' in response and 'href="' in response:
        start_index = response.find('href="') + 6
        end_index = response.find('">', start_index)
        return response[start_index:end_index]
    return None

# Initialize text-to-speech engine
try:
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)  # Speed of speech
except Exception as e:
    print(f"Warning: Could not initialize text-to-speech engine: {str(e)}")
    engine = None

def speak_text(text):
    if engine:
        try:
            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            print(f"Error in text-to-speech: {str(e)}")

def chatbot_response(msg, is_voice_input=False):
    try:
        if is_voice_input:
            speak_text("I received your voice input. Processing your request...")
        
        ints = predict_class(msg, model)
        res = getResponse(ints, intents)

        # Process links in response
        link = extract_link(res)
        if link:
            response_text = res.replace(link, 'click here')
        else:
            response_text = res

        if is_voice_input and engine:
            speak_text(response_text)

        return response_text
    except Exception as e:
        error_msg = f"Sorry, I encountered an error processing your request: {str(e)}"
        if is_voice_input and engine:
            speak_text("Sorry, I encountered an error processing your request.")
        return error_msg