import os
import json 
from openai import OpenAI
from queries.ai_movie_queries import MovieQueries
from collections import Counter

from sentence_transformers import SentenceTransformer, util

from queries.ai_movie_queries import MovieQueries


class ChatAgent: 
    '''
    A movie assisteant that supports continuous conversation
    '''
    def __init__(self):
        # set up the connection to deepseek
        self.client = OpenAI(
            api_key = os.getenv('DEEPSEEK_API_KEY'),
            base_url = 'https://api.deepseek.com'
        )
        # converation history to stored on self os it persists across turns. 
        self.messages = [{'role':'system', 'content': 'You are a friendly movie assistent, you are going to answer all of the questions realte to the movie, you can serach for the database if you need'}]
        self.movies = MovieQueries()
        self.chunks = []

        

    def random_chat(self, user_input):
        """Take one user message, return the AI's reply, and record history. just for chat, it won't read for the databse,the response may unaccurate """
        # 1.add the user's meesage to the history
        self.messages.append({'role':'user', 'content':user_input})
        # 2.send the whole history to deepseek f
        response = self.client.chat.completions.create(
        model = 'deepseek-chat', 
        messages = self.messages,
        temperature = 0.1 
        )
        reply = response.choices[0].message.content
        # 3.add the AI's reply to the history as well. 
        self.messages.append({'role': 'assistant', 'content': reply })

        return reply
    
    # task1:

    def understand_intent(self, user_input): 
        """
        Ask Deepseek what the user wants and extract parameters. Returns a dict.
        """
        system_prompt = """
        You are a query parser for a movie database. Read the user's question and decide which query to run.
        Avaible queries: 
        -'movie_by_cast' : user asks what movies an actor appeared in
        - 'none;: the question does not match any query 
        Return Only a Json object in this extract format: 
        {'query': 'movie_by_cast', 'cast_name': 'the actors name'} 

        If no query matches, return: {"query": "none"}
        """
        response = self.client.chat.completions.create(
            model = 'deepseek-chat', 
            messages = [
                {"role": "system", "content": system_prompt},
                {"role":"user" , "content": user_input}
                        ],
            temperature = 0.1,
            response_format = {"type": "json_object"}
        )
        dict_results = json.loads(response.choices[0].message.content)
        # {"query": "movies_by_actor", "name": "the actor's name"}
        # we have defined in the system_prompt
        return dict_results 
    
    # task2 : 

    def search_movie(self, user_input): 
        """
        Full workflow: 
        1. understand the question, then generate the dict for the specific format
        2. query the database 
        3. format the answer
        """
        # step1: understnad what the users whats
        intent = self.understand_intent(user_input)

        # if not matching query, let deepseek answer normally 
        if intent.get("query") == 'none':
            return self.chat(user_input)
        # step2 : query the database
        if intent.get('query') == 'movie_by_cast': 
            data = self.movies.movie_by_cast(intent['cast_name'])
        
        # step3 : format the answer 
        system_prompt = "You are a movie assistent. Answer the user based on the data."
        user_prompt = f"""
        User asked : {user_input}   
        Database results {json.dumps(data, ensure_ascii = False, default = str)}
        Please answer in a natural and friendly way.
        """
        response = self.client.chat.completions.create(
            model = 'deepseek-chat', 
            messages = [
                {'role': 'system', 'content': system_prompt}, 
                {'role': 'user', 'content': user_prompt}
            ],
            temperature = 0.1
        )
        return response.choices[0].message.content
    
    # task3: 
    
    def split_into_chunks(self, text, chunk_size=5000):
        """
        Split a long text into smaller chunks.
        """
        
        for i in range(0, len(text), chunk_size):
            self.chunks.append(text[i : i+chunk_size])
        return self.chunks


    def analyze_themes(self, limit = None):
        """
        Analyze the most common themes across movie overviews.
        """
        # 1. get overviews from the database
        movies = self.movies.get_all_overviews(limit)
        # 2. combine all overviews into 1 big text
        all_text = ''
        for m in movies: 
            all_text += m['overview'] + '\n'
        
        # 3. split the big text into chunkcs
        chunks = self.split_into_chunks(all_text)
        print(f'Split into {len(chunks)} chunks')

        # 4. extract themes from each chunk, count them
        counter = Counter()
        for i, chunk in enumerate(chunks):
        
            print(
                f"Processing chunk {i + 1}/{len(chunks)} "
                f"- {len(chunk)} characters"
            )

            system_prompt = """
            You are a movie analyst.
            Read the movie plot summaries.
            Identify the main themes/topics.

            Return ONLY JSON:
            {"themes": ["love", "war", "revenge"]}
            """

            response = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": chunk}
                ],
                temperature=0.1,
                response_format={"type": "json_object"}
            )

            content = response.choices[0].message.content

            try:
                result = json.loads(content)

                for theme in result.get("themes", []):
                    counter[theme.lower()] += 1

            except json.JSONDecodeError as e:
                print(f"JSON error in chunk {i + 1}: {e}")
                print("DeepSeek response:")
                print(content)
                continue
        return counter.most_common(10)