### Recommendation API Test Code

deep-learning based recommendation, user-recommendation, location-recommendation

```python
class UserTestCase(unittest.TestCase):
    def setUp(self):
        self.domain = 'http://localhost:5000/'
    
    def test_deeplearning(self):
        URL = self.domain + "map-recommend"
        response = requests.get(URL, data=json.dumps({"user": [{"latitude_0": 1, "longitude_0": 2},
                                                            {"latitude_1": 3, "longitude_1": 4},
                                                            {"latitude_2": 5, "longitude_2": 6}]}))
        self.assertEqual(response.status_code, 200)

    def test_user_recommend(self):
        URL = self.domain + "user-recommend"
        user_id = 381
        response = requests.get(URL, data=json.dumps({"user_id": user_id}))
        self.assertEqual(response.status_code, 200)

    def test_location_recommend(self):
        URL = self.domain + "location-recommend"
        location_id = 5315
        response = requests.get(URL, data=json.dumps({"location_id": location_id}))
        self.assertEqual(response.status_code, 200)
```