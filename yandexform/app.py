from yandexform import create_app

app = create_app()

if __name__ == '__main__':
    print("Зарегистрированные URL:")
    print(app.url_map)
    app.run(debug=True)
