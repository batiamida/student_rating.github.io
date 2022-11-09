import requests
from my_tools import restart_all_seq, deleteAll

def send_request(base_link='http://127.0.0.1', port=5000, **kwargs):
    r_type = kwargs.get('request_type')
    params = kwargs.get('params')
    r = f'{base_link}:{port}//{kwargs.get("route")}'
    response = None

    if r_type == 'get':
        response = requests.get(r, params=params)

    elif r_type == 'post':
        response = requests.post(r, params=params)

    elif r_type == 'delete':
        response = requests.delete(r, params=params)

    elif r_type == 'put':
        response = requests.put(r, params=params)

    return response, response.text

if __name__ == "__main__":
    pass
    # responses = [
    #     # requests.post('http://127.0.0.1:5000//teacher', params={'username': 'SomeUsername', 'email': 'someemail',
    #     #                                                     'password': 'somepass', 'phone': '3341'}),
    #     #
    #     #                                                         'password': 'somepass', 'phone': '3341'}),
    #
    #     # requests.put('http://127.0.0.1:5000//teacher', params={'id': 2, 'username': 'NewUsername',
    #     #                                                        'firstName': 'shos'}),
    #
    #     # requests.post('http://127.0.0.1:5000//teacher', params={'username': 'SomeUsername',
    #     #                                                         'email': 'someemail@gmail.com',
    #     #                                                         'firstName': 'someName',
    #     #                                                         'lastName': 'name',
    #     #                                                         'password': 'somepass', 'phone': '3341'}),
    #
    #
    #
    #     # requests.delete('http://127.0.0.1:5000//teacher', params={'id': 2}),
    #
    #     # requests.post('http://127.0.0.1:5000//student', params={'username': 'SomeStudent',
    #     #                                                     'email': 'someStudent@gmail.com',
    #     #                                                     'password': 'somepass', 'phone': '3341'}),
    #     # requests.post('http://127.0.0.1:5000//subject', params={'name': 'math'}),
    #     # requests.post('http://127.0.0.1:5000//score', params={'studentId': 1, 'teacherId': 1, 'subjectId': 1,
    #     #                                                       'score': 10}),
    #     requests.get('http://127.0.0.1:5000//teacher/1'),
    #     # requests.delete('http://127.0.0.1:5000//score', params={'id': 1}),
    #     # requests.delete('http://127.0.0.1:5000//student', params={'id': 1}),
    #     # requests.delete('http://127.0.0.1:5000//teacher', params={'id': 1}),
    #     # requests.delete('http://127.0.0.1:5000//subject', params={'id': 1}),
    #
    # ]

    # for response in responses:
    #     print(response)
    #     print(response.json())
    # # deleteAll()
    # # restart_all_seq()
    print(send_request(route='student', request_type='post', params={
        'username': 'SomeUsername',
        'email': 'someemassis2l@gmasil.com',
        'firstName': 'someeeName',
        'lastName': 'nsaame',
        'password': 'somepass', 'phone': '3341'
    }))
    # print(send_request(route='score', request_type='delete', params={
    #     'id': 1
    # }))
    # print(send_request(route='subject', request_type='post', params={
    #     'name': 'math'
    # }))
    print(send_request(route='score//get_nrating', request_type='get', params={'n': 2}))
    # print(send_request(route='score', request_type='post',
    #                    params={
    #                        'studentId': 2,
    #                        'teacherId': 1,
    #                        'subjectId': 1,
    #                    }))

    # while True:
    #     if input('continue (+ or -): ') == '-':
    #         break
    #
    #     route, request_type, params =

    # print(send_request(route='score', request_type='post'))
    # print(send_request(route='teacher/1', request_type='get'))
    # status_code, response = send_request(route='student/1', request_type='get')
    # print(response)
