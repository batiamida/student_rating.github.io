import requests
from my_tools import restart_all_seq, deleteAll


if __name__ == "__main__":
    responses = [
        # requests.post('http://127.0.0.1:5000//teacher', params={'username': 'SomeUsername', 'email': 'someemail',
        #                                                     'password': 'somepass', 'phone': '3341'}),
        #
        #                                                         'password': 'somepass', 'phone': '3341'}),

        # requests.put('http://127.0.0.1:5000//teacher', params={'id': 2, 'username': 'NewUsername',
        #                                                        'firstName': 'shos'}),

        # requests.post('http://127.0.0.1:5000//teacher', params={'username': 'SomeUsername',
        #                                                         'email': 'someemail@gmail.com',
        #                                                         'firstName': 'someName',
        #                                                         'lastName': 'name',
        #                                                         'password': 'somepass', 'phone': '3341'}),



        # requests.delete('http://127.0.0.1:5000//teacher', params={'id': 2}),

        # requests.post('http://127.0.0.1:5000//student', params={'username': 'SomeStudent',
        #                                                     'email': 'someStudent@gmail.com',
        #                                                     'password': 'somepass', 'phone': '3341'}),
        # requests.post('http://127.0.0.1:5000//subject', params={'name': 'math'}),
        # requests.post('http://127.0.0.1:5000//score', params={'studentId': 1, 'teacherId': 1, 'subjectId': 1,
        #                                                       'score': 10}),
        requests.get('http://127.0.0.1:5000//teacher/1'),
        # requests.delete('http://127.0.0.1:5000//score', params={'id': 1}),
        # requests.delete('http://127.0.0.1:5000//student', params={'id': 1}),
        # requests.delete('http://127.0.0.1:5000//teacher', params={'id': 1}),
        # requests.delete('http://127.0.0.1:5000//subject', params={'id': 1}),

    ]



    for response in responses:
        print(response)
        print(response.json())
    # deleteAll()
    # restart_all_seq()