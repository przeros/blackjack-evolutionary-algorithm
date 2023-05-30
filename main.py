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
    # krupier dobiera 2 karty, jedna jest widoczna dla gracza, jedna nie
    visible_card = deck.pop(randint(0, len(deck) - 1))
    non_visible_card = deck.pop(randint(0, len(deck) - 1))
    return deck, visible_card, non_visible_card

def player_init(deck: list):
    # gracz dobiera 2 karty
    card1 = deck.pop(randint(0, len(deck) - 1))
    card2 = deck.pop(randint(0, len(deck) - 1))
    return deck, card1, card2

def draw_card(deck: list):
    # dobranie karty przez gracza lub krupiera
    card = deck.pop(randint(0, len(deck) - 1))
    return deck, card

def init_population(n):
    # inicjalizacja populacji
    population = []

    for x in range(n):
        # suma liczby punktów na ręku gracza (od 4 do 19)
        individual = []
        for i in range(16):
            # średnia liczba punktów kart, których nie ma już w talii = ręka gracza + widoczna karta krupiera (od 2 do 10)
            temp = [randint(0, 1) for _ in range(9)]
            individual.append(temp)
        population.append(individual)
        # for raw in individual:
        #     print(raw)
        # print()
    return population

def draw_or_not(player_hand_sum, total_hand_avg, genotype):
    if genotype[player_hand_sum - 4][total_hand_avg - 2] == 1:
        return True
    else:
        return False

def bank_draw_or_not(bank_hand_sum, player_hand_sum):
    if bank_hand_sum < player_hand_sum:
        return True
    elif bank_hand_sum == player_hand_sum:
        if bank_hand_sum < 17:
            return True
        else:
            return False
    else:
        return False

def select_best_x_percent(population_scores, percent):
    # Wyznacz indeksy najlepszych x% osobników
    num_indexes = int(len(population_scores) * percent)
    return np.argsort(population_scores)[-num_indexes:]

def training_game(genotype) -> int:
    # funkcja zwraca: 1 - gdy gracz wygra, -1 - gdy krupier wygra, 0 - gdy jest remis
    deck = init_deck()
    bank_hand = []
    player_hand = []

    # gracz dobiera 2 karty
    deck, card1, card2 = player_init(deck)
    player_hand.append(card1)
    player_hand.append(card2)

    # krupier dobiera 2 karty
    deck, visible_card, non_visible_card = bank_init(deck)
    bank_hand.append(visible_card)
    bank_hand.append(non_visible_card)

    while (sum(player_hand) < 20):
        # gracz dobiera karty zgodnie z heurystyką algorytmu
        total_hand_avg = int(round((sum(player_hand) + visible_card) / (len(player_hand) + 1), 0))
        should_draw_card = draw_or_not(sum(player_hand), total_hand_avg, genotype)
        if should_draw_card:
            deck, card = draw_card(deck)
            player_hand.append(card)
        else:
            break

    if sum(player_hand) == 21:
        return 1
    if sum(player_hand) > 21:
        return -1
    else:
        while (sum(bank_hand) < 20):
            # krupier dobiera karty dopóki nie przebije gracz lub nie spali
            bank_should_draw_card = bank_draw_or_not(sum(bank_hand), sum(player_hand))
            if bank_should_draw_card:
                deck, card = draw_card(deck)
                bank_hand.append(card)
            else:
                break
        if sum(bank_hand) > 21:
            return 1
        else:
            if sum(player_hand) > sum(bank_hand):
                return 1
            elif sum(player_hand) == sum(bank_hand):
                return 0
            else:
                return -1

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
            for j in range(9):
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
            for j in range(9):
                if random() < mutation_prob:
                    population[x][i][j] = 1 if population[x][i][j] == 0 else 0
    return population

if __name__ == '__main__':
    population = init_population(2000)
    games = 3000
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
            draws = 0
            for j in range(games):
                result = training_game(population[i])
                if result == 1:
                    wins += 1
                elif result == 0:
                    draws += 1
            accuracy = wins / (games - draws)
            population_scores.append(accuracy)
        percent = 0.01
        selected_indexes = select_best_x_percent(population_scores, percent)

        selected_scores = []
        print("Selected Scores:")
        for i in selected_indexes:
            selected_scores.append(population_scores[i])
        print(selected_scores)
        avg_population_score = mean(population_scores)
        avg_selected_score = mean(selected_scores)
        print(f'Average Population Score = {avg_population_score}')
        print(f'Average Selected Individuals Score = {avg_selected_score}')
        print(f'Best Individual Score = {selected_scores[-1]}')
        print(f'Best Individual:')
        for raw in population[selected_indexes[-1]]:
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

        crossing_ratio = 0.7
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