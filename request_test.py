import requests
from my_tools import restart_all_seq, deleteAll, select

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

    print(select(kwargs.get('route').split('/')[0]))

    return response, response.text

if __name__ == "__main__":
    ''' --------POST---------- '''
    # print(send_request(route='teacher', request_type='post', params={
    #     'username': 'smthNew',
    #     'email': 'someemasis2l@gmasil.com',
    #     'firstName': 'someeeName',
    #     'lastName': 'nsaame',
    #     'password': 'somepass', 'phone': '0998788423'
    # }))
    #
    # print(send_request(route='student', request_type='post',
    #                    params={
    #                        'username': 'TestUsername',
    #                        'email': 'TestEmail@gmail.com',
    #                        'firstName': 'TestName',
    #                        'lastName': 'TestName',
    #                        'password': 'testPass', 'phone': '0998286423'
    #                    }))
    # print(send_request(route='student', request_type='post',
    #                    params={
    #                        'username': 'AnotherUsername',
    #                        'email': 'AnotherEmail@gmail.com',
    #                        'firstName': 'AnotherName',
    #                        'lastName': 'AnotherName',
    #                        'password': 'testPass', 'phone': '0997286423'
    #                    }))
    #
    # print(send_request(route='subject', request_type='post',
    #                    params={
    #                        'name': 'math'
    #                    }))
    # print(send_request(route='score', request_type='post', params={
    #                        'studentId': 1,
    #                        'teacherId': 1,
    #                        'subjectId': 1,
    #                         'score': 5
    # }))
    # print(send_request(route='score', request_type='post', params={
    #                        'studentId': 2,
    #                        'teacherId': 1,
    #                        'subjectId': 1
    # }))



    ''' --------DELETE---------- '''
    # print(send_request(route='student', request_type='delete', params={
    #     'id': 1
    # }))

    ''' --------GET---------- '''
    # print(send_request(route='score/1', request_type='get'))
    # print(send_request(route='score/rating/1', request_type='get'))
    # print(send_request(route='teacher/100', request_type='get'))

    ''' --------PUT---------- '''
    # print(send_request(route='score', request_type='put', params={
    #     'id': 2,
    #     'score':
    # }))


    # print(send_request())


    # deleteAll()
    # restart_all_seq()

