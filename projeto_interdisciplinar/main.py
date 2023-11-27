from flask import Flask, render_template, request, redirect, url_for
import psycopg2
import logging

app = Flask(__name__)

conn = psycopg2.connect(
    host="localhost",
    database="desmatamento_amazonia",
    user="postgres",
    password="070204"
)
conn.autocommit = True

logging.basicConfig(level=logging.DEBUG)


@app.route('/')
def index():
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM dados_desmatamento;")
        dados_desmatamento = cursor.fetchall()

        cursor.execute("SELECT * FROM recuperar;")
        recuperacao = cursor.fetchall()
    return render_template('index.html', dados_desmatamento=dados_desmatamento, recuperacao=recuperacao)


@app.route('/adicionar_dados', methods=['GET', 'POST'])
def adicionar_dados():
    if request.method == 'POST':
        estado = request.form['estado']
        area_desmatada_km2 = float(request.form['area_desmatada_km2'])

        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO dados_desmatamento (estado, area_desmatada_km2) VALUES (%s, %s);",
                (estado, area_desmatada_km2)
            )

            conn.commit()

        return redirect(url_for('index'))

    return render_template('adicionar_dados.html')


if __name__ == '__main__':
    app.run(debug=True)
