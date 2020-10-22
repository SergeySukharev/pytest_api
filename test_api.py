import pytest

POSTS_MAX = 200


@pytest.mark.parametrize('post_id', [1, POSTS_MAX])
def test_get_positive(session, base_url, post_id):
    res = session.get(url=f'{base_url}/{post_id}')

    assert res.status_code == 200
    assert res.json()['id'] == post_id


@pytest.mark.parametrize('post_id', [-1, 0, POSTS_MAX + 1])
def test_get_negative(session, base_url, post_id):
    res = session.get(url=f'{base_url}/{post_id}')

    assert res.status_code == 404
    assert res.json() == {}


def test_get_all(session, base_url):
    res = session.get(url=f'{base_url}')

    assert len(res.json()) == POSTS_MAX
    for elem in res.json():
        assert elem['id'] == 


def test_post(session, base_url):
    title = 'foo'
    body = 'bar'
    payload = {'title': title, 'body': body, 'userId': 1}
    res = session.post(url=base_url, json=payload)

    assert res.status_code == 201
    j = res.json()
    assert j['id'] == POSTS_MAX + 1
    assert j['userId'] == 1
    assert j['title'] == title
    assert j['body'] == body


def test_put_positive(session, base_url):
    post_id = 1
    title = 'foo'
    body = 'bar'
    payload = {'title': title, 'body': body, 'id': post_id, 'userId': 1}
    res = session.put(url=f'{base_url}/{post_id}', json=payload)

    assert res.status_code == 200
    res_json = res.json()
    assert res_json['title'] == title
    assert res_json['body'] == body


def test_put_negative(session, base_url):
    payload = 11232
    res = session.put(url=f'{base_url}/1', json=payload)

    assert res.status_code == 500


@pytest.mark.parametrize('data', [{"userId": '88'}, {"id": '66'}, {"title": "test title"}, {"completed": 'True'}])
def test_patch(session, base_url, data):
    res = session.patch(url=f'{base_url}/1', data=data)

    assert res.status_code == 200
    assert res.json()[list(data)[0]] == data[list(data)[0]]


def test_delete(session, base_url):
    res = session.delete(url=f'{base_url}/1')

    assert res.status_code == 200
    assert not res.json()


@pytest.mark.parametrize('params', [{"userId": 9}, {"id": 4}, {"title": "vel non beatae est"}, {"completed": True}])
def test_filter_positive(session, base_url, params):
    res = session.get(url=f'{base_url}', params=params)

    assert res.status_code == 200
    for elem in res.json():
        assert elem[list(params)[0]] == params[list(params)[0]]


@pytest.mark.parametrize('params', [{"userId": 'User'}, {"id": 5676}, {"title": "there is no such title"},
                                    {"completed": 'i don know'}])
def test_filter_negative(session, base_url, params):
    res = session.get(url=f'{base_url}', params=params)

    assert res.status_code == 200
    assert res.json() == []
