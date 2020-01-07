import json
import requests

print("GET HELLO")
response = requests.get("http://localhost:8084/hello")
hello = response.json()
print(hello)

print("Author gets ALL")
response = requests.get("http://localhost:8084/author")
author = response.json()
print(author)

print("Add author")

url = "http://localhost:8084/author/"
payload = {"name": "string2",
           "surname": "string2"}
headers = {'content-type': 'application/json'}
response = requests.post(url, data=json.dumps(payload), headers=headers)
pastebin_url = response.json()
print(pastebin_url)
print(response.status_code)


print("Delete author by ID")
url = "http://localhost:8084/author/1"

headers = {'content-type': 'application/json'}
response = requests.delete(url, headers=headers)
pastebin_url = response.json()
print(pastebin_url)
print(response.status_code)

print("Search author by id")
url = "http://localhost:8084/author/2"

headers = {'content-type': 'application/json'}
response = requests.get(url, headers=headers)
pastebin_url = response.json()
print(pastebin_url)
print(response.status_code)


print("Show all books")
url = "http://localhost:8084/book/list"
headers = {'content-type': 'application/json'}
response = requests.get(url, headers=headers)
pastebin_url = response.json()
print(pastebin_url)
print(response.status_code)


print("ADD books")
url = "http://localhost:8084/book/list"
data={
  "title": "Bieguni",
  "year": "2007",
  "author_id": 5
}
headers = {'content-type': 'application/json'}
response = requests.post(url, data=json.dumps(data), headers=headers)
pastebin_url = response.json()
print(pastebin_url)
print(response.status_code)

print("Delete book by id")
url = "http://localhost:8084/book/1"
headers = {'content-type': 'application/json'}
response = requests.delete(url, headers=headers)
pastebin_url = response.json()
print(pastebin_url)
print(response.status_code)


print("Search book by id")
url = "http://localhost:8084/book/1"

headers = {'content-type': 'application/json'}
response = requests.get(url, headers=headers)
pastebin_url = response.json()
print(pastebin_url)
print(response.status_code)


#url = "http://localhost:8084/file/1"



'''''
from flask import Flask, render_template
from flask import request
app = Flask(__name__)


@app.route('/',methods=['GET'])
def home():
    response = requests.get("http://localhost:8084/hello")
    hello = response.json()
    return render_template('hello.html',response=json.dumps(hello))


@app.route('/author/',methods=['GET','POST'])
def about():
    if request.method == 'GET':
        response = requests.get("http://localhost:8084/author")
        author = response.json()
        print(author)
        return render_template('hello.html',response=json.dumps(author))
    if request.method == 'POST':
        url = "http://localhost:8084/author/"
        payload = {"name": "Ivan",
                   "surname": "Prokopets"}
        headers = {'content-type': 'application/json'}
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        post = response.json()
        print(post)
        return render_template('about.html',response=json.dumps(post))


if __name__ == '__main__':
    app.run(debug=True)
'''''


