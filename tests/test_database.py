""" Test redis controller """
from database.controller import Controller


def test_redis_test():
    """Check that it's actually working on redis database."""
    redis_controller = Controller(host="redislabs/redismod")
    res = redis_controller.search_room_nodes("blah", "blah")
    assert res == []
