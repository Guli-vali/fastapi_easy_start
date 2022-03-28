import pytest

pytestmark = pytest.mark.asyncio

async def test_ping(json_client, app):
    response = await json_client.get(app.url_path_for('core:healthcheck'))
    assert response.status_code == 200
    assert response.json() == {"ping": "pong"}

async def test_get_all_events(authorized_json_client, app):
    response = await authorized_json_client.get(app.url_path_for('events:list'))
    assert response.status_code == 200

async def test_can_not_access_events_without_authentication(json_client, app):
    response = await json_client.get(app.url_path_for('events:list'))
    assert response.status_code == 401

async def test_can_not_create_events_without_authentication(json_client,  app):
    response = await json_client.post(app.url_path_for('events:create'))
    assert response.status_code == 401

async def test_create_and_select_event(authorized_json_client, app):
    response_create = await authorized_json_client.post(app.url_path_for('events:create'), json={"title": "Business lunch for startupers", "location": "God damn Chickago!"})
    response_select = await authorized_json_client.get(app.url_path_for('events:get-one', object_id=response_create.json().get('id')))

    assert response_create.status_code == 200
    assert response_select.status_code == 200
    assert response_create.json() == response_select.json()

async def test_can_not_access_events_upate_without_authentication(json_client, authorized_json_client, app):
    create_json_data = {"title": "Business lunch for startupers", "location": "God damn Chickago!"}
    update_json_data = {"title": "Business lunch for startupers. NEW AND UPDATED!", "location": "God damn Chickago! WITH NEW TASTE!"}
    
    response_create = await authorized_json_client.post(app.url_path_for('events:create'), json=create_json_data)
    response_update = await json_client.put(app.url_path_for('events:update', object_id=response_create.json().get('id')), json=update_json_data)

    assert response_update.status_code == 401

async def test_create_and_update_event(authorized_json_client, app):
    create_json_data = {"title": "Business lunch for startupers", "location": "God damn Chickago!"}
    update_json_data = {"title": "Business lunch for startupers. NEW AND UPDATED!", "location": "God damn Chickago! WITH NEW TASTE!"}
    
    response_create = await authorized_json_client.post(app.url_path_for('events:create'), json=create_json_data)
    response_update = await authorized_json_client.put(app.url_path_for('events:update', object_id=response_create.json().get('id')), json=update_json_data)

    response_update_json = response_update.json()

    assert response_create.json() != response_update_json
    response_update_json.pop('id')
    assert response_update_json == update_json_data


async def test_can_not_access_events_delete_without_authentication(json_client, authorized_json_client, app):
    create_json_data = {"title": "Business lunch for startupers", "location": "God damn Chickago!"}
    
    response_create = await authorized_json_client.post(app.url_path_for('events:create'), json=create_json_data)
    response_delete = await json_client.delete(app.url_path_for('events:delete', object_id=response_create.json().get('id')))

    assert response_delete.status_code == 401

async def test_create_and_delete_event(authorized_json_client, app):
    create_json_data = {"title": "Business lunch for startupers", "location": "God damn Chickago!"}
    
    response_create = await authorized_json_client.post(app.url_path_for('events:create'), json=create_json_data)
    response_delete = await authorized_json_client.delete(app.url_path_for('events:delete', object_id=response_create.json().get('id')))

    assert response_delete.status_code == 200
