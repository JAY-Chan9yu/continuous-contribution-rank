from task.crawling_git import say_hello


def test_say_hello():
    assert "hello !" == say_hello()

