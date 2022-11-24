import unittest
from app import app, custom_response
from my_tools import *
from flask import Flask

class MyAppTest(unittest.TestCase):

    client = app.test_client()

    def create_app(self):
        app.config['TESTING'] = True
        return app

class MyTest(unittest.TestCase):
    client = app.test_client()
    student_params = {
        'username': 'student_1',
        'firstName': 'John',
        'lastName': 'nothing',
        'email': 'student_1@gmail.com',
        'phone': '380888505',
        'password': '123'
    }
    teacher_params = {
        'username': 'some_t2',
        'firstName': 'Karl2',
        'lastName': 'nothing',
        'email': 'some_t2@gmail.com',
        'password': '123',
        'phone': '380888505'
    }

    def test_hello(self):
        r = self.client.get('/')
        self.assertEqual(r.status_code, 200)

    def test_labfunc(self):
        r = self.client.get('/api/v1/hello-world-27')
        self.assertEqual(r.status_code, 200)

    def test_teacher(self):
        r = self.client.get('/teacher/1')
        self.assertEqual(r.status_code, 200)

    def test_noteacher(self):
        r = self.client.get('/teacher/20000')
        self.assertEqual(r.status_code, 404)

    def test_student(self):
        r = self.client.get('/student/1')
        self.assertEqual(r.status_code, 200)

    def test_nostudent(self):
        r = self.client.get('/student/20000')
        self.assertEqual(r.status_code, 404)

    def test_main(self):
        r = self.client.get('/')
        self.assertEqual(r.status_code, 200)

    def test_lab(self):
        r = self.client.get('/api/v1/hello-world-27')
        self.assertEqual(r.status_code, 200)

    def test_studentp_403(self):
        r = self.client.post('/student', json=self.student_params)
        self.assertEqual(r.status_code, 403)

    def test_studentp_200(self):
        r2 = getBy(Student, username='new_one_username')[0].id
        r3 = deleteById(Student, r2)
        self.assertEqual(1, r3)
        r = self.client.post('/student', query_string={'username': 'new_one_username',
                                                       'firstName': 'I know',
                                                       'lastName': self.student_params['lastName'],
                                                       'phone': self.student_params['phone'],
                                                       'password': self.student_params['password'],
                                                       'email': 'new_email@gmail.com'},
                             auth=('some_t2', '123'))
        self.assertEqual(r.status_code, 200)


    def test_studentp_405(self):
        r = self.client.post('/student', json=self.student_params, auth=('some_t2', '123'))
        self.assertEqual(r.status_code, 405)

    def test_studentpt_403(self):
        r = self.client.put('/student', query_string={'id': 5, 'firstName': 'NewName'}, auth=('1_student', '123'))
        self.assertEqual(r.status_code, 403)

    def test_studentpt_405(self):
        r = self.client.put('/student', query_string={'firstName': 'NewName'}, auth=('1_student', '123'))
        self.assertEqual(r.status_code, 405)

    def test_studentd_403(self):
        r = self.client.delete('/student', query_string={'id': 2}, auth=('some_t2', '123'))
        self.assertEqual(r.status_code, 403)

    def test_studentd_500(self):
        r1 = self.client.delete('/student', query_string={"smth": "2"}, auth=('admin', 'admin123'))
        self.assertEqual(r1.status_code, 500)


    def test_teacherp_403(self):
        r = self.client.post('/teacher', json=self.student_params)
        self.assertEqual(r.status_code, 403)

    def test_teacherp_405(self):
        r = self.client.post('/teacher', query_string=self.teacher_params, auth=('admin', 'admin123'))
        self.assertEqual(r.status_code, 405)


    def test_teacherpt_403(self):
        r = self.client.put('/teacher', json={'id': 5, 'firstName': 'NewName'})
        self.assertEqual(r.status_code, 403)

    def test_teacherpt_500(self):
        r = self.client.put('/teacher', json={'firstName': 'NewName'}, auth=('some_t2', '123'))
        self.assertEqual(r.status_code, 500)

    # def test_teacherpt_

    def test_teacherd_500(self):
        r = self.client.delete('/teacher', json={'id': 2}, auth=('some_t2', '123'))
        self.assertEqual(r.status_code, 500)

    def test_teacherd_403(self):
        r = self.client.delete('/teacher', query_string={'id': 2}, auth=('some_t', '123'))
        self.assertEqual(r.status_code, 403)


    def test_score(self):
        r = self.client.get('/score/1')
        self.assertEqual(r.status_code, 200)

    def test_noscore(self):
        r = self.client.get('/score/200')
        self.assertEqual(r.status_code, 404)

    def test_scorep_403(self):
        r = self.client.post('/score')
        self.assertEqual(r.status_code, 403)

    def test_scorep_500(self):
        r = self.client.post('/score', query_string={'studentId': 1, 'teacherId': 2, 'subjectId': 2, 'score': -5},
                             auth=('some_t', '123'))
        self.assertEqual(r.status_code, 500)

    def test_scorept_500(self):
        r = self.client.put('/score', query_string={'id': 1, 'score': -5},
                             auth=('some_t', '123'))
        self.assertEqual(r.status_code, 500)

    def test_scorept_404(self):
        r = self.client.put('/score', query_string={'id': 100, 'score': 5},
                             auth=('some_t', '123'))
        self.assertEqual(r.status_code, 404)

    def test_scored_404(self):
        r = self.client.put('/score', query_string={'id': 100, 'score': 5},
                             auth=('some_t', '123'))
        self.assertEqual(r.status_code, 404)

    def test_scored_403(self):
        r = self.client.put('/score', query_string={'id': 100, 'score': 5})
        self.assertEqual(r.status_code, 403)

    def test_scored_500(self):
        r = self.client.put('/score',
                            auth=('some_t', '123'))
        self.assertEqual(r.status_code, 500)

    def test_subject_404(self):
        r = self.client.get('/subject/200')
        self.assertEqual(r.status_code, 404)

    def test_subject_200(self):
        r = self.client.get('/subject/1')
        self.assertEqual(r.status_code, 200)

    def test_subjectp_403(self):
        r = self.client.post('/subject')
        self.assertEqual(r.status_code, 403)

    def test_subjectp_500(self):
        r = self.client.post('/subject', auth=('some_t2', '123'))
        self.assertEqual(r.status_code, 500)

    def test_subjectp_404(self):
        r = self.client.post('/subject', query_string={'name': 'math'}, auth=('some_t', '123'))
        self.assertEqual(r.status_code, 404)

    def test_subjectd_403(self):
        r = self.client.delete('/subject', query_string={'id': 1})
        self.assertEqual(r.status_code, 403)

    def test_subjectd_500(self):
        r = self.client.delete('/subject', query_string={'id': 1}, auth=('some_t', '123'))
        self.assertEqual(r.status_code, 500)

    def test_subjectd_404(self):
        r = self.client.delete('/subject', query_string={'id': 5}, auth=('some_t', '123'))
        self.assertEqual(r.status_code, 404)

    def test_getnrating(self):
        r = self.client.get('/score/rating/2')
        self.assertEqual(r.status_code, 200)

    def test_scoreBySID_200(self):
        r = self.client.get('/score/1')
        self.assertEqual(r.status_code, 200)

    def test_scoreBySID_404(self):
        r = self.client.get('/score/100')
        self.assertEqual(r.status_code, 404)



    def test_functions(self):
        r1 = custom_response(200, 'ok')
        self.assertEqual(r1.status_code, 200)
        r2 = getAllStudents()
        self.assertEqual(type(r2), list)
        r3 = checkEveryoneBy(id=2)
        self.assertEqual(type(r3), tuple)
        r4 = getBy(Student, id=1)
        self.assertEqual(type(r4), list)

my_test = MyTest()
for func in [test for test in dir(MyTest) if test.startswith('test')]:
    assert lambda: eval(f'my_test.{func}')() == None
my_test = MyAppTest()
for func in [test for test in dir(MyTest) if test.startswith('test')]:
    assert lambda: eval(f'my_test.{func}')() == None

# import requests
# from my_tools import restart_all_seq, deleteAll, select, create_admin
#
# def send_request(base_link='http://127.0.0.1', port=5000, **kwargs):
#     r_type = kwargs.get('request_type')
#     params = kwargs.get('params')
#     r = f'{base_link}:{port}//{kwargs.get("route")}'
#     response = None
#
#     if r_type == 'get':
#         response = requests.get(r, params=params)
#
#     elif r_type == 'post':
#         response = requests.post(r, params=params)
#
#     elif r_type == 'delete':
#         response = requests.delete(r, params=params)
#
#     elif r_type == 'put':
#         response = requests.put(r, params=params)
#
#     print(select(kwargs.get('route').split('/')[0]))
#
#     return response, response.text
#
# if __name__ == "__main__":
#     ''' --------POST---------- '''
#     # print(send_request(route='teacher', request_type='post', params={
#     #     'username': 'smthNew',
#     #     'email': 'someemasis2l@gmasil.com',
#     #     'firstName': 'someeeName',
#     #     'lastName': 'nsaame',
#     #     'password': 'somepass', 'phone': '0998788423'
#     # }))
#     #
#     # print(send_request(route='student', request_type='post',
#     #                    params={
#     #                        'username': 'TestUsername',
#     #                        'email': 'TestEmail@gmail.com',
#     #                        'firstName': 'TestName',
#     #                        'lastName': 'TestName',
#     #                        'password': 'testPass', 'phone': '0998286423'
#     #                    }))
#     # print(send_request(route='student', request_type='post',
#     #                    params={
#     #                        'username': 'AnotherUsername',
#     #                        'email': 'AnotherEmail@gmail.com',
#     #                        'firstName': 'AnotherName',
#     #                        'lastName': 'AnotherName',
#     #                        'password': 'testPass', 'phone': '0997286423'
#     #                    }))
#     #
#     # print(send_request(route='subject', request_type='post',
#     #                    params={
#     #                        'name': 'math'
#     #                    }))
#     # print(send_request(route='score', request_type='post', params={
#     #                        'studentId': 1,
#     #                        'teacherId': 1,
#     #                        'subjectId': 1,
#     #                         'score': 5
#     # }))
#     # print(send_request(route='score', request_type='post', params={
#     #                        'studentId': 2,
#     #                        'teacherId': 1,
#     #                        'subjectId': 1
#     # }))
#
#
#
#     ''' --------DELETE---------- '''
#     # print(send_request(route='student', request_type='delete', params={
#     #     'id': 1
#     # }))
#
#     ''' --------GET---------- '''
#     # print(send_request(route='score/1', request_type='get'))
#     # print(send_request(route='score/rating/1', request_type='get'))
#     # print(send_request(route='teacher/100', request_type='get'))
#
#     ''' --------PUT---------- '''
#     # print(send_request(route='score', request_type='put', params={
#     #     'id': 2,
#     #     'score':
#     # }))
#
#
#     # print(send_request())
#
#
#     # deleteAll()
#     # restart_all_seq()
#
#     create_admin()
