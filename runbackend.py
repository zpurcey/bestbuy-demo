from backend import app

if __name__ == '__main__':
    app.run('0.0.0.0',port=8080, threaded=True, debug=True)
