from app import app, views

app.add_url_rule("/", view_func=views.index)

if __name__ == '__main__':
    app.run(debug=True)