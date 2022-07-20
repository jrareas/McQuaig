import unittest
import requests
import os

BASE_URL = os.environ.get("BASE_URL", "http://localhost:5001")


def order(name, email):
    body = {"name": name, "email": email}
    return requests.post(f"{BASE_URL}/order", json=body)


def get_order(token):
    return requests.get(f"{BASE_URL}/order/{token}")


def delete_order(token):
    return requests.delete(f"{BASE_URL}/order/{token}")


class TestOrder(unittest.TestCase):
    def test_can_order_assessment(self):
        name = "Žiga"
        email = "ziga@example.com"

        resp = order(name, email)
        resp.raise_for_status()
        json = resp.json()

        requests.post(json["assessment_url"]).raise_for_status()

        resp = get_order(json["id"])
        resp.raise_for_status()
        json = resp.json()
        assert json["status"] == "Completed"
        assert json["name"] == name
        assert json["email"] == email

    def test_cant_complete_assessment_twice(self):
        name = "Peter"
        email = "peter@example.com"

        resp = order(name, email)
        resp.raise_for_status()
        json = resp.json()

        requests.post(json["assessment_url"]).raise_for_status()

        resp = requests.post(json["assessment_url"])
        assert resp.status_code == 410
        assert resp.text == "Already Completed"

    def test_cant_get_deleted_assessment(self):
        name = "Miša"
        email = "misa@example.com"

        resp = order(name, email)
        resp.raise_for_status()
        json = resp.json()

        delete_order(json["id"]).raise_for_status()

        resp = get_order(json["id"])
        assert resp.status_code == 404

    def test_deleted_assessments_are_redacted(self):
        name = "Dejan"
        email = "dejan@example.com"

        resp = order(name, email)
        resp.raise_for_status()
        json = resp.json()

        delete_order(json["id"]).raise_for_status()

        resp = requests.post(json["assessment_url"])
        assert resp.status_code == 410
        assert resp.text == "Redacted"

    def test_can_delete_after_completion(self):
        name = "Anja"
        email = "anja@example.com"

        resp = order(name, email)
        resp.raise_for_status()
        json = resp.json()

        requests.post(json["assessment_url"]).raise_for_status()
        delete_order(json["id"]).raise_for_status()

        resp = requests.post(json["assessment_url"])
        assert resp.status_code == 410
        assert resp.text == "Already Completed"


if __name__ == "__main__":
    unittest.main()
