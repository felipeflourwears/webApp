from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/back', methods=['POST'])
def back():
    # Aquí puedes procesar los datos del formulario si es necesario
    # Luego redireccionar a back.py
    return redirect(url_for('back'))

if __name__ == '__main__':
    app.run(debug=True)