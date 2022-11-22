import requests

# res = requests.get("http://127.0.0.1:5000/user/")
# res = requests.put("http://127.0.0.1:5000/user/login", {"phoneNumber": "380984128532", "password": "32KMLKmlsfk@fwfew4"})
headers =  {'Content-Type': 'application/json; charset=utf-8'}

body1 = {
    "id": 2,
    "fullName": "vasya11",
    "address": "Symonenka 25",
    "idCity": 1,
    "phoneNumber": "380936653445",
    "password": "vasya123",
    "role": 0
}

# res = requests.post("http://127.0.0.1:5000/user", headers = headers, json = body1)

body2 = {
    "phoneNumber": "380971655945",
    "password": "legion"
}

# res = requests.get("http://127.0.0.1:5000/user/login", headers = headers, json = body2)
# res = requests.get("http://127.0.0.1:5000/protected", headers = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY2ODM0OTY5MSwianRpIjoiNmQwYTk0YWQtYzZjYi00MGYxLWE1MzEtNjM4Y2E2MmE0ZWFhIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MSwibmJmIjoxNjY4MzQ5NjkxLCJleHAiOjE2NjgzNTA1OTF9.ku_4Mnhk1ZJwswjwDAk2Ta2M1ZZD0g0Q_1LUkHZNSg0"})

# res = requests.post("http://127.0.0.1:5000/user", headers = headers, json = body)

t1 = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY2ODc2MTYxMiwianRpIjoiZmM3M2IyMmUtMjQ2Yi00ODRjLWE2MjAtODFhZmE2NDkyNjM5IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MSwibmJmIjoxNjY4NzYxNjEyLCJleHAiOjE2Njg3NjI1MTJ9.OIn8_MrNEV_N19nHkrH4YsakwJdiN92TKt5OnsrrMpk"
t2 = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY2ODc2MTU1OCwianRpIjoiNjJmODlkMzAtNTg2Zi00ZmE0LWEwOTQtMGQ4NmQyNjMwYWE3IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MiwibmJmIjoxNjY4NzYxNTU4LCJleHAiOjE2Njg3NjI0NTh9.97FlZC7lK_SU557VfU5N5gCHDV0Mn45bMFQcr7Ns2m8"

res = requests.delete("http://127.0.0.1:5000/user/2", headers = {"Authorization": "Bearer " + t1})

print(res.json())
