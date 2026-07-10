from twitter_transcribe.download import is_twitter_status_url


def test_accepts_x_and_twitter_hosts():
    assert is_twitter_status_url("https://x.com/jack/status/20")
    assert is_twitter_status_url("https://twitter.com/jack/status/20")
    assert is_twitter_status_url("https://mobile.twitter.com/jack/status/20")
    assert is_twitter_status_url("http://www.x.com/a_b/status/1234567890")


def test_rejects_non_status_urls():
    assert not is_twitter_status_url("https://x.com/jack")
    assert not is_twitter_status_url("https://youtube.com/watch?v=abc")
    assert not is_twitter_status_url("https://x.com.evil.com/a/status/1")
    assert not is_twitter_status_url("not a url")
    assert not is_twitter_status_url("")
