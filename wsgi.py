"""App entry point."""
from music import create_app

app = create_app()
# if app.debug == True:
    # print(app.debug)    # app.run(debug=True)
# app.debug = True
if __name__ == "__main__":
    app.run(host='localhost', port=5000, threaded=False)
