import string
import random
import neuron

# Caracteres para reconhecimento
characters = string.digits + '-.'

# Configuração do perceptron
learning_rate = 0.01
bias = 1.0
num_epochs = 1000
num_examples = 100

# Função para gerar exemplos de treinamento
def generate_training_data(num_examples):
    training_set = []
    desired_set = []

    for _ in range(num_examples):
        number = ''.join(random.choices(characters, k=12))
        inputs = [1.0 if char == '-' else 0.0 for char in number]
        training_set.append(inputs)
        desired_set.append(1.0)

    return training_set, desired_set

# Gerar exemplos de treinamento
X, Y = generate_training_data(num_examples)

# Criar e treinar o perceptron
perceptron = neuron.Perceptron(X, Y, learning_rate, bias)
for _ in range(num_epochs):
    perceptron.learn()

# Solicitar número ao usuário
number = input("Digite um número: ")

# Converter número em vetor de entrada para o perceptron
inputs = [1.0 if char == '-' else 0.0 for char in number]

# Fazer previsão usando o perceptron
prediction = perceptron.compute_output(inputs)

# Exibir resultado da previsão
if prediction == 1.0:
    print("O número é um número real.")
else:
    print("O número não é um número real.")
