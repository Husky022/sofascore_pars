import requests

from settings import disciplines

from database.manager import DBManager

from datetime import date

from pprint import pprint


class ApiParser:
    def __init__(self):
        self.db = DBManager()
        self.targets = disciplines

    @staticmethod
    def get_response(url):
        response = requests.get(url)
        return response.json()

    def download_data(self):
        tournament_id = 1
        tournaments_to_db = []
        events_to_db = []
        motor_category_id = 1
        motor_categories = []
        motorsports = []
        for target in self.targets:
            if target == 'motorsport':
                try:
                    response = self.get_response('https://api.sofascore.com/api/v1/sport/motorsport/categories')
                    for item in response['categories']:
                        category = {
                            'name': item['name']
                        }
                        motor_categories.append(category)

                except KeyError:
                    print(f'{target} - ERROR! - ошибка ключа')
            else:
                pass
            try:
                response = self.get_response(f'https://api.sofascore.com/api/v1/sport/{target}/scheduled-events/'
                                             f'{date.today()}')
                tournaments_to_db.append({'name': target})
                for item in response['events']:
                    event = {
                        'home_player': item['homeTeam']['name'],
                        'away_player': item['awayTeam']['name'],
                        'home_score': item['homeScore'].get('current', None),
                        'away_score': item['awayScore'].get('current', None),
                        'type': item['status']['type'],
                        'date': date.today(),
                        'league_id': tournament_id,
                    }
                    events_to_db.append(event)
                print(f'{target} - DONE')
            except KeyError:
                print(f'{target} - ERROR! - ошибка ключа')
            tournament_id += 1
        self.db.record_tournaments(tournaments_to_db)
        self.db.record_events(events_to_db)
        self.db.record_motor_categories(motor_categories)
        self.db.record_events(events_to_db)


    def run(self):
        self.download_data()


if __name__ == "__main__":
    parser = ApiParser()
    parser.run()
