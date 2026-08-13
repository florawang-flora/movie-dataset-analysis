from tools.utils import Utils
from cli.run_ai_menu import MovieCLI
from pipeline.data_analytics import data_analytics
def run():
    movie_assistant = MovieCLI()
    tools = Utils()
    print('\nWelcome to the Movie Data and AI System! ')
    while True: 
        print('\n=== Main Menu ===')
        print("1. Run data analytics and load data into PostgramSQL")
        print("2. Open the AI System")
        print("Type 'quit' to exit ")
        choice = input("> ").strip().lower()
        if choice == 'quit': 
            return tools.exit_program()
        if choice == '1': 
            return data_analytics()
        elif choice =='2':
            return movie_assistant.run_ai_menu()
        else: 
            print("Please enter 1,2 or 'quit'")

if __name__ == '__main__':
    run()
        