
import nltk
from nltk.stem import WordNetLemmatizer
import json
import numpy as np
from tensorflow import keras
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import SGD
lemmatizer = WordNetLemmatizer()

words = []
classes = []
documents = []
ignore_chars = ['?', '.', '!']
# carica il file JSON con i dati di addestramento
with open('dataset.json') as file:
        data = json.load(file)

def trainModel():
    global words, classes, documents, ignore_chars
    # crea le liste di parole, le classi e i documenti di addestramento
    for intent in data['intents']:
        for pattern in intent['patterns']:
            # tokenizza ogni parola nella frase
            tokens = nltk.word_tokenize(pattern)
            words.extend(tokens)
            # aggiunge il documento alla lista dei documenti
            documents.append((tokens, intent['tag']))
            # aggiunge la classe alla lista delle classi
            if intent['tag'] not in classes:
                classes.append(intent['tag'])

    # lemmatizza le parole e rimuove i duplicati
    words = [lemmatizer.lemmatize(word.lower()) for word in words if word not in ignore_chars]
    words = sorted(list(set(words)))
    classes = sorted(list(set(classes)))

    # crea il training set
    training_data = []
    output_empty = [0] * len(classes)

    for document in documents:
        bag = []
        word_patterns = document[0]
        # lemmatizza le parole del pattern
        word_patterns = [lemmatizer.lemmatize(word.lower()) for word in word_patterns]
        # crea la matrice di parole
        for word in words:
            bag.append(1) if word in word_patterns else bag.append(0)
        # crea l'output
        output_row = list(output_empty)
        output_row[classes.index(document[1])] = 1
        training_data.append([bag, output_row])

    # mescola il training set
    np.random.shuffle(training_data)
    training_data = np.array(training_data)

    # definisce il modello di rete neurale
    model = keras.Sequential([
        Dense(128, input_shape=(len(words),), activation='relu'),
        Dropout(0.5),
        Dense(64, activation='relu'),
        Dropout(0.5),
        Dense(len(classes), activation='softmax')
    ])

    # compila il modello
    sgd = SGD(learning_rate=0.01, momentum=0.9, nesterov=True)
    model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

    # addestra il modello
    history = model.fit(training_data[:,0].tolist(), training_data[:,1].tolist(), epochs=1000, batch_size=50, verbose=1)

    # salva il modello
    model.save('chatbot_model')


# definisce la funzione per processare l'input dell'utente e restituire una risposta
def process_input(input_text):
    global words, classes, documents, ignore_chars
    # carica il modello
    model = keras.models.load_model('chatbot_model')
    # tokenizza l'input
    input_words = nltk.word_tokenize(input_text)
    # lemmatizza le parole
    input_words = [lemmatizer.lemmatize(word.lower()) for word in input_words if word not in ignore_chars]
    # crea la matrice di parole
    bag = [0] * len(words)
    for word in input_words:
        for i, w in enumerate(words):
            if w == word:
                bag[i] = 1
    # predice la classe
    prediction = model.predict(np.array([bag]))[0]
    # ottiene la classe con la probabilità più alta
    highest_probability = max(prediction)
    print(highest_probability)
    if highest_probability > 0.80:
        print("I'm sure")
        result = classes[np.argmax(prediction)]
    else:
        result = 'I don\'t understand'
    return result

def save_undefined_question(question):
    # se il file questions.json non esiste, lo crea e lo inizializza, altrimenti lo carica
    try:
        with open('questions.json') as file:
            questions = json.load(file)
    except:
        questions = []
    # aggiunge la domanda alla lista
    questions.append(question)
    # salva la lista nel file
    with open('questions.json', 'w') as file:
        json.dump(questions, file)



# definisce la funzione per rispondere all'input dell'utente
def process_response(input_text):
    # ottiene la risposta
    response = process_input(input_text)
    print(response)
    # cerca la risposta nel file JSON
    for intent in data['intents']:
        if intent['tag'] == response:
            # sceglie una risposta casuale
            return np.random.choice(intent['responses'])
       
    # salva la domanda
    save_undefined_question(input_text)
    return "non ho capito"
