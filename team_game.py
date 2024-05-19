import random
import requests
from PIL import Image
from pathlib import Path
from io import BytesIO
from rich.console import Console
from rich.panel import Panel

def random_pokemon(count=1):
    pokemon_list = []
    for _ in range(count):
        pokemon_number = random.randint(1, 151)
        url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_number}/'
        response = requests.get(url)
        pokemon = response.json()
        num_moves = len(pokemon['moves'])
        pokemon_list.append({
            'name': pokemon['name'],
            'id': pokemon['id'],
            'height': pokemon['height'],
            'weight': pokemon['weight'],
            'moves': num_moves,
            'img': pokemon["sprites"]["front_default"],
        })
    return pokemon_list[0] if len(pokemon_list) == 1 else pokemon_list

wins = {
    "player": 0,
    "opponent": 0
}
stats = ["name", "id", "height", "weight", "moves"]

def update_scoresheet():
    player1_curr_high_score = wins["player"]
    player2_curr_high_score = wins["opponent"]

    if Path("./scoresheet.txt").exists():
        with open("./scoresheet.txt", "r") as scoresheet:
            high_score_player1 = int(scoresheet.readline().split(":")[1])
            high_score_player2 = int(scoresheet.readline().split(":")[1])
            print(f"high score1: {high_score_player1}")
            print(f"high score2: {high_score_player2}")

            if player1_curr_high_score < high_score_player1:
                player1_curr_high_score = high_score_player1
            if player2_curr_high_score < high_score_player2:
                player2_curr_high_score = high_score_player2

    with open("./scoresheet.txt", "w") as scoresheet:
        scoresheet.write("player:" + str(player1_curr_high_score))
        scoresheet.write("\nopponent:" + str(player2_curr_high_score))

def fetch_and_display_image(url):
    try:
        # Fetch the image from the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Open the image from the fetched content
        img = Image.open(BytesIO(response.content))

        # Convert the image to RGB mode (if not already in RGB)
        img = img.convert("RGB")

        # Save the image to a temporary file in a supported format
        temp_image_path = "temp_image.jpg"  # Save as JPEG
        img.save(temp_image_path)

        # Display the image using the default image viewer
        img_viewer_command = f"start {temp_image_path}"  # For Windows
        import os
        os.system(img_viewer_command)

    except requests.exceptions.RequestException as e:
        print(f"Error fetching the image: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

def run():
    while True:
        list_or_random = input("Choose from a list or get one random pokemon (list/random)?")
        if list_or_random == "list":
            pokemon_list = random_pokemon(10)
            for index, pokemon in enumerate(pokemon_list):
                print(f" {index}. {pokemon['name']}(ID: {pokemon['id']})")
            user_list_choice = input("Choose pokemon by index:")
            my_pokemon = pokemon_list[int(user_list_choice)]

        elif list_or_random == "random":
            my_pokemon = random_pokemon()

        print(f'You were given {my_pokemon["name"].capitalize()}')

        print(my_pokemon["img"])
        fetch_and_display_image(my_pokemon["img"])

        stat_choice = input('Which stat do you want to use (id, height, weight, moves)?  Or let the opponent choose (opponent). ')

        if stat_choice == "opponent":
            stat_choice = random.choice(stats)
        elif stat_choice not in stats:
            continue

        print(f'{stat_choice.capitalize()}: {my_pokemon[stat_choice]}')

        opponent_pokemon = random_pokemon()
        print(f'The opponent chose {opponent_pokemon["name"].capitalize()}')
        print(f'{stat_choice.capitalize()}: {opponent_pokemon[stat_choice]}')

        my_stat = my_pokemon[stat_choice]
        opponent_stat = opponent_pokemon[stat_choice]

        if my_stat > opponent_stat:
            print('You Win this round!')
            wins["player"] += 1
        elif my_stat < opponent_stat:
            print('You Lose this round!')
            wins["opponent"] += 1
        else:
            print('Draw!')

        play_again = input('Do you want to play again? (yes/no)').lower()
        if play_again == 'yes':
            continue
        else:
            print('Game over!')
            print(f'You won {wins["player"]} rounds')
            print(f'The opponent won {wins["opponent"]} rounds')

            update_scoresheet()

            if wins["player"] > wins["opponent"]:
                print('Congratulations! You win the game!')
            elif wins["player"] < wins["opponent"]:
                print('Sorry! You lost the game!')
            else:
                print('It\'s a tie!')
            break

run()
