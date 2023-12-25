from flask import Flask
import scraper as sc
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, world'

@app.route('/update')
def update_database():
    res = sc.update_result_links()
    return 'Update kr diya hu bhai thk h aur ye bol rha\n' + res


if __name__ == "__main__":
    app.run()
