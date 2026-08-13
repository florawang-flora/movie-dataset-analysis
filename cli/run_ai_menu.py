from cli.chat_agent import ChatAgent

class MovieCLI:
    def __init__(self):
        self.agent = ChatAgent()
 
    def exit_program(self): 
        print('Goodbye!')
        raise SystemExit

    def random_chat(self):
        print('\n=== AI Random Chat ===')
        print("Type 'back' to return to the AI menu.")
        print("Type 'quit' to exit.")
        while True: 
            user_input = input('You: ').strip()
            if user_input.lower() =='quit':
                self.exit_program()
            if user_input.lower() == "back": 
                return
            if not user_input: 
                continue
            try: 
                reply = self.agent.random_chat(user_input)
                print(f"AI: {reply}")
            except Exception as error: 
                print(f'AI chat failed: {error}')
    def serach_movies(self):
        print("\n=== Movie Search ===")
        print("Example: What movies did Tom Hanks appear in?")
        print("Type 'back' to return to the AI menu.")
        print("Type 'quit' to exit.")
        while True: 
            user_input = input('Search: ').strip()
            if user_input.lower() == 'quit':
                self.exit_program()
            if user_input.lower() == 'back': 
                return 
            if not user_input: 
                continue
            try: 
                result = self.agent.search_movie(user_input)
                print(f'AI: {result}')
            except Exception as error: 
                print(f'Movie search failed: {error}')
    
    def show_top_themes(self):
        print('Analysing movie themes... ')
        try:
            top_themes = self.agent.analyze_themes(limit = 4000)
            print("\n=== Top 10 theme  ===")
            for theme, count in top_themes:
                print(f"{theme}: {count}")
        except Exception as error: 
            print (f"Theme analysis failed: {error}")

    def run_ai_menu(self): 
        while True: 
            print('\n== AI System ==')
            print('1.Chat with the AI')
            print("2. Search for movie information")
            print("3. Analyse the Top 10 movie themes")
            print("4. Return to the main menu")
            print("Type 'quit' to exit")
            choice = input('> ').strip().lower()
            if choice == 'quit': 
                self.exit_program()
            if choice == '1': 
                self.random_chat()
            elif choice == '2': 
                self.serach_movies()
            elif choice == '3': 
                self.show_top_themes()
            elif choice == '4': 
                return 
            else: 
                print('Please enter 1,2,3,4 or "quit ."')

#if __name__ == '__main__':
#    moviecli = MovieCLI()
#    moviecli.run_ai_menu()
