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
    data_file = open(datafile, 'w', encoding='utf-8', newline='')
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
    print(f"{len(games)} added!")


def create_dataset(game_limit='300', datafile='game_genres.csv'):
    valid_genre_data = requester(['genres',
                                  'fields name; limit 100;'])
    valid_genres = {}
    headers = ["Name Of The Game"]
    for vgd in valid_genre_data:
        valid_genres[vgd['id']] = vgd['name']
        headers.append(vgd['name'])
    games = []
    iterations = int(int(game_limit) / 500)
    offset = int(game_limit) % 500
    print(iterations)
    print(offset)
    it = 1
    # if iterations > 0:
    #     print(it)
    #     for i in range(0, iterations):
    limit = int(game_limit)
    if limit < 501:
        game_data = requester(['games',
                               'fields name, genres; where genres != null; sort rating desc; where rating != null; limit '
                               f'{500};'])
        for gd in game_data:
            if 'genres' in gd and len(gd['genres']) > 2:
                games.append(gd)
    while limit - 500 > 0:
        game_data = requester(['games',
                               'fields name, genres; where genres != null; sort rating desc; where rating != null; limit '
                               f'{500}; offset {500 * it};'])
        for gd in game_data:
            if 'genres' in gd and len(gd['genres']) > 2:
                games.append(gd)
        it += 1
        if limit - 500 > 0:
            limit = limit - 500
        else:
            break
    if limit > 0:
        game_data = requester(['games',
                               'fields name, genres; where genres != null; sort rating desc; where rating != null; limit '
                               f'{limit}; offset {500 * it};'])
        for gd in game_data:
            if 'genres' in gd and len(gd['genres']) > 2:
                games.append(gd)
    write_to_csv(headers, valid_genres, games, datafile=datafile)


if __name__ == '__main__':
    create_dataset(game_limit="5000",  datafile='game_genres_extended1.csv')
    # create_dataset(datafile='new_dataset.csv')
    # print(int(600/500))
    # print(int(400/500))
