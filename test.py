from starlette.testclient import TestClient

from api import qumata_technical_test

client = TestClient(qumata_technical_test)

def test_github_orgs():
    result = ["Animikii Inc.","Caring.com Dev Team","Coder (moved to @coder)","Collective Idea","EdgeCase","Engine Yard, Inc.","entryway","Galaxy Cats","GumGum","IPVM","Lincoln Loop","Merb","Ministry Centered Technologies","Moneyspyder","Netguru","Notch8","nventive inc","OGC","Railsdog","Railslove","Revelation","Sauspiel GmbH","Sevenwire","Sproutit/SproutCore","Standout AB","Trabian","Unto This Last","Wesabe","Wrench Labs"]
    response = client.get("/github_orgs")
    assert response.status_code == 200
    assert response.json() == result

    result = ["Lincoln Loop"]
    response = client.get("/github_orgs")
    assert response.status_code == 200
    assert response.json() == result
    assert response  == result

    # by the third try, it should exceed rate limits for non-authorized users
    result = False
    response = client.get("/github_orgs")
    assert response.status_code == 200
    assert response == result

