from igdb.wrapper import IGDBWrapper
import secret
import json
import csv

CLIENT_ID = secret.CLIENT_ID
ACCESS_TOKEN = secret.ACCESS_TOKEN
wrapper = IGDBWrapper(CLIENT_ID, ACCESS_TOKEN)


def requester(params: list):
    genres_byte_array = wrapper.api_request(
        params[0], params[1]
    )
    genre_json = genres_byte_array.decode('utf-8').replace("'", '"')
    return json.loads(genre_json)


def write_to_csv(header_row: list, genres: dict, games: list, datafile='data_file.csv'):
    data_file = open(datafile, 'w', encoding='utf-8')
    csv_writer = csv.writer(data_file)
    csv_writer.writerow(header_row)

    for game in games:
        row = [game['name']]
        for genre in genres:
            if genre in game['genres']:
                row.append(1)
            else:
                row.append(0)

        csv_writer.writerow(row)
    print("DONE")


def create_dataset(game_limit='100', datafile='data_file.csv'):
    valid_genre_data = requester(['genres',
                                  'fields name; limit 100;'])
    valid_genres = {}
    headers = ["Name Of The Game"]
    for vgd in valid_genre_data:
        valid_genres[vgd['id']] = vgd['name']
        headers.append(vgd['name'])
    games = []
    game_data = requester(['games',
                           'fields name, genres; where genres != null; sort rating desc; where rating != null; limit '
                           f'{game_limit};'])
    for gd in game_data:
        if 'genres' in gd and len(gd['genres']) > 2:
            games.append(gd)
    write_to_csv(headers, valid_genres, games, datafile=datafile)


if __name__ == '__main__':
    create_dataset()
    # create_dataset(datafile='new_dataset.csv')
