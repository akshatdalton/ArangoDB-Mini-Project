from arango import ArangoClient
import os
from time import sleep
import sys

client = ArangoClient()

db = client.db('Movies', username='root', password='user@1234')

if not db.has_graph('movies_element'):
    db.create_graph('movies_element')

movies_element = db.graph('movies_element')

elements = ['actors', 'movies', 'directors']

for i in elements:
    if not movies_element.has_vertex_collection(i):
        movies_element.create_vertex_collection(i)

actors = movies_element.vertex_collection('actors')
movies = movies_element.vertex_collection('movies')
directors = movies_element.vertex_collection('directors')

actors_list = ['Aamir', 'Anushka', 'Sushant', 'Salmaan']
movies_list = ['PK', '3Idiots', 'Lagaan', 'Dangal', 'Sultan', 'MSDhoni']
directors_list = ['Hirani', 'Nitesh', 'Abbas', 'Neeraj']

for i in actors_list:
    if not actors.has(i):
        actors.insert({
            '_key' : f"{i}",
            'name' : i
        })

for i in movies_list:
    if not movies.has(i):
        movies.insert({
            '_key' : i,
            'name' : i
        })

for i in directors_list:
    if not directors.has(i):
        directors.insert({
            '_key' : i,
            'name' : i
        })

if not movies_element.has_edge_definition('actor_movies'):
    movies_element.create_edge_definition(
        edge_collection='actor_movies',
        from_vertex_collections=['actors'],
        to_vertex_collections=['movies']
    )

actor_movies = movies_element.edge_collection('actor_movies')


if not actor_movies.has('Aamir-PK'):
    actor_movies.insert({
        '_key' : 'Aamir-PK',
        '_from' : 'actors/Aamir',
        '_to' : 'movies/PK',
        'movie' : 'PK',
        'directors' : 'Hirani'
    })
    actor_movies.insert({
        '_key' : 'Aamir-3Idiots',
        '_from' : 'actors/Aamir',
        '_to' : 'movies/3Idiots',
        'movie' : '3Idiots',
        'directors' : 'Hirani'
    })
    actor_movies.insert({
        '_key' : 'Aamir-Lagaan',
        '_from' : 'actors/Aamir',
        '_to' : 'movies/Lagaan',
        'movie' : 'Lagaan',
        'directors' : 'Ashutosh'
    })
    actor_movies.insert({
        '_key' : 'Aamir-Dangal',
        '_from' : 'actors/Aamir',
        '_to' : 'movies/Dangal',
        'movie' : 'Dangal',
        'directors' : 'Nitesh'
    })
    actor_movies.insert({
        '_key' : 'Anushka-PK',
        '_from' : 'actors/Anushka',
        '_to' : 'movies/PK',
        'movie' : 'PK',
        'directors' : 'Hirani'
    })
    actor_movies.insert({
        '_key' : 'Anushka-Sultan',
        '_from' : 'actors/Anushka',
        '_to' : 'movies/Sultan',
        'movie' : 'Sultan',
        'directors' : 'Abbas'
    })
    actor_movies.insert({
        '_key' : 'Sushant-MSDhoni',
        '_from' : 'actors/Sushant',
        '_to' : 'movies/MSDhoni',
        'movie' : 'MSDhoni', 
        'directors' : 'Neeraj'
    })
    actor_movies.insert({
        '_key' : 'Salmaan-Sultan',
        '_from' : 'actors/Salmaan',
        '_to' : 'movies/Sultan',
        'movie' : 'Sultan',
        'directors' : 'Abbas'
    })

if not movies_element.has_edge_definition('director_movies'):
    movies_element.create_edge_definition(
        edge_collection='director_movies',
        from_vertex_collections=['directors'],
        to_vertex_collections=['movies']
    )

director_movies = movies_element.edge_collection('director_movies')

if not director_movies.has('Hirani-PK'):
    director_movies.insert({
        '_key' : 'Hirani-PK',
        '_from' : 'directors/Hirani',
        '_to' : 'movies/PK',
        'movie' : 'PK'
    })
    director_movies.insert({
        '_key' : 'Hirani-3Idiots',
        '_from' : 'directors/Hirani',
        '_to' : 'movies/3Idiots',
        'movie' : '3Idiots'
    })
    director_movies.insert({
        '_key' : 'Nitesh-Dangal',
        '_from' : 'directors/Nitesh',
        '_to' : 'movies/Dangal',
        'movie' : 'Dangal'
    })
    director_movies.insert({
        '_key' : 'Abbas-Sultan',
        '_from' : 'directors/Abbas',
        '_to' : 'movies/Sultan',
        'movie' : 'Sultan'
    })
    director_movies.insert({
        '_key' : 'Neeraj-MSDhoni',
        '_from' : 'directors/Neeraj',
        '_to' : 'movies/MSDhoni',
        'movie' : 'MSDhoni'
    })

def actors_movie_list(actor):
    edge_list = actor_movies.edges(f'actors/{actor}', direction='out')['edges']
    movie_list = [i['movie'] for i in edge_list]
    
    return movie_list

def actors_common_list(actor1, actor2):
    list1 = actors_movie_list(actor1)
    list2 = actors_movie_list(actor2)

    common_list = []

    for i in list1:
        for j in list2:
            if i == j:
                common_list.append(i)

    for i in common_list:
        print(i)

def actor_director_list(actor, director):
    edge_list = actor_movies.edges(f'actors/{actor}', direction='out')['edges']
    movie_list = [i['movie'] for i in edge_list if i['directors'] == director]

    for i in movie_list:
        print(i)

def director_list(actor):
    edge_list = actor_movies.edges(f'actors/{actor}', direction='out')['edges']
    
    list = []

    for i in edge_list:
        if not list.count(i['directors']):
            list.append(i['directors'])

    for i in list:
        print(i)

def main():

    while(True):
        print('1. actors movie list.')
        print('2. movie list of given 2 actors.')
        print('3. movies list of given actor, director.')
        print('4. list of directors the actor done movies with.')
        choice = input('Enter Your Choice Number or press any other key to exit\n> ')
        if choice == '1':
            actor = input('Enter the name of the actor\n')
            list = actors_movie_list(actor)
            for i in list:
                print(i)
        elif choice == '2':
            actor1, actor2 = input('Enter the name of 2 actors\n').split()
            actors_common_list(actor1, actor2)
        elif choice == '3':
            actor, director = input('Enter the name of a actor and a director\n').split()
            actor_director_list(actor, director)
        elif choice == '4':
            actor = input('Enter the name of actor to know the list of directors he/she done movies with\n')
            director_list(actor)
        else:
            sys.exit(0)
        
        sleep(2)
        os.system('clear')

if __name__ == "__main__":
    main()
