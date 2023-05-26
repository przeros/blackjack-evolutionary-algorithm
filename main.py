from random import randint, random
import numpy as np
from statistics import mean

def init_deck():
    return [2, 2, 2, 2,
        2, 2, 2, 2,
        3, 3, 3, 3,
        3, 3, 3, 3,
        4, 4, 4, 4,
        4, 4, 4, 4,
        5, 5, 5, 5,
        6, 6, 6, 6,
        7, 7, 7, 7,
        8, 8, 8, 8,
        9, 9, 9, 9,
        10, 10, 10, 10,
        11, 11, 11, 11]

def bank_init(deck: list):
    visible_card = deck.pop(randint(0, len(deck) - 1))
    non_visible_card = deck.pop(randint(0, len(deck) - 1))
    return deck, visible_card, non_visible_card

def player_init(deck: list):
    card1 = deck.pop(randint(0, len(deck) - 1))
    card2 = deck.pop(randint(0, len(deck) - 1))
    return deck, card1, card2

def draw_card(deck: list):
    card = deck.pop(randint(0, len(deck) - 1))
    return deck, card

def init_population(n):
    population = []

    for x in range(n):
        # od 4 do 19
        individual = []
        for i in range(16):
            # od 2 do 11
            temp = [randint(0, 1) for _ in range(10)]
            individual.append(temp)
        population.append(individual)
        # for raw in individual:
        #     print(raw)
        # print()
    return population

def draw_or_not(player_hand_sum, visible_card, genotype):
    if genotype[player_hand_sum - 4][visible_card - 2] == 1:
        return True
    else:
        return False

def bank_draw_or_not(bank_hand_sum, player_hand_sum):
    if bank_hand_sum < player_hand_sum:
        return True
    else:
        return False

def select_best_x_percent(population_scores, percent):
    # Calculate the number of indexes for the top x%
    num_indexes = int(len(population_scores) * percent)
    # Get the indexes of the top values
    return np.argsort(population_scores)[-num_indexes:]

def training_game(genotype):
    deck = init_deck()
    bank_hand = []
    player_hand = []

    # player draws 2 cards
    deck, card1, card2 = player_init(deck)
    player_hand.append(card1)
    player_hand.append(card2)

    # bank draws 2 cards
    deck, visible_card, non_visible_card = bank_init(deck)
    bank_hand.append(visible_card)
    bank_hand.append(non_visible_card)

    while (sum(player_hand) < 20):
        should_draw_card = draw_or_not(sum(player_hand), visible_card, genotype)
        if should_draw_card:
            deck, card = draw_card(deck)
            player_hand.append(card)
        else:
            break

    if sum(player_hand) == 21:
        return True
    if sum(player_hand) > 21:
        return False
    else:
        while (sum(bank_hand) < 20):
            bank_should_draw_card = bank_draw_or_not(sum(bank_hand), sum(player_hand))
            if bank_should_draw_card:
                deck, card = draw_card(deck)
                bank_hand.append(card)
            else:
                break
        if sum(bank_hand) > 21:
            return True
        else:
            if sum(player_hand) > sum(bank_hand):
                return True
            else:
                return False

def crossing(population, selected_indexes: list, ratio):
    parents = []
    for i in selected_indexes:
        parents.append(population[i])

    childs = []
    for x in range(len(population) - len(selected_indexes)):
        child = []
        parent1 = parents[randint(0, len(selected_indexes) - 1)]
        parent2 = parents[randint(0, len(selected_indexes) - 1)]
        for i in range(16):
            temp = []
            for j in range(10):
                if random() < ratio:
                    temp.append(parent1[i][j])
                else:
                    temp.append(parent2[i][j])
            child.append(temp)
        childs.append(child)
    return parents + childs

def mutation(population, mutation_prob):
    for x in range(len(population)):
        for i in range(16):
            for j in range(10):
                if random() < mutation_prob:
                    population[x][i][j] = 1 if population[x][i][j] == 0 else 0
    return population

if __name__ == '__main__':
    population = init_population(1000)
    games = 5000
    epochs = 100

    best_population = population
    best_population_accuracy = 0
    best_individual = []
    best_individual_accuracy = 0
    early_stop = 0
    for e in range(epochs):
        print(f'--- Epoch {e + 1} ---')
        population_scores = []
        for i in range(len(population)):
            wins = 0
            for j in range(games):
                if training_game(population[i]):
                    wins += 1
            accuracy = wins / games
            population_scores.append(accuracy)
        percent = 0.1
        selected_indexes = select_best_x_percent(population_scores, percent)

        selected_scores = []
        print("Selected Scores:")
        for i in selected_indexes:
            selected_scores.append(population_scores[i])
        print(selected_scores)
        avg_population_score = mean(selected_scores)
        print(f'Average Population Score = {avg_population_score}')
        print(f'Best Individual:')
        for raw in best_individual:
            print(raw)
        print()
        if avg_population_score > best_population_accuracy:
            best_population = population
            best_population_accuracy = avg_population_score
            early_stop = 0
        else:
            early_stop += 1

        if selected_scores[-1] > best_individual_accuracy:
            best_individual = population[selected_indexes[-1]]
            best_individual_accuracy = selected_scores[-1]

        crossing_ratio = 0.9
        population = crossing(population, selected_indexes, crossing_ratio)
        mutation_prob = 0.01
        population = mutation(population, mutation_prob)

        if early_stop > 5:
            break

    print(f'Best Average Population Score = {best_population_accuracy}')
    print(f'Best Individual Score = {best_individual_accuracy}')
    print(f'Best Individual:')
    for raw in best_individual:
        print(raw)