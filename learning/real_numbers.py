import random
import string
import numpy as np
import neuron

# Caracteres para reconhecimento
characters = string.digits + '-.'

# Função para gerar exemplos de treinamento
def generate_training_data(num_examples):
    training_set = []
    desired_set = []

    for _ in range(num_examples):
        number = ''.join(random.choices(characters, k=12))
        inputs = [1.0 if char == '-' else 0.0 for char in number]
        training_set.append(inputs)
        desired_set.append(1.0 if '.' in number else 0.0)

    return training_set, desired_set

# Configuração do perceptron
learning_rate = 0.01
bias = 1.0
num_epochs = 1000
num_examples = 100

# Gerar exemplos de treinamento
X, Y = generate_training_data(num_examples)

# Criar e treinar o perceptron
perceptron = neuron.Perceptron(X, Y, learning_rate, bias)
for _ in range(num_epochs):
    perceptron.learn()

# Testar o perceptron
test_examples = ['123', '-456', '7.89', '-0.12']
for example in test_examples:
    inputs = [1.0 if char == '-' else 0.0 for char in example]
    prediction = perceptron.compute_output(inputs)
    print(f"Input: {example}, Prediction: {prediction}")
