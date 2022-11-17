import logging
import traceback

import flask
from flask import redirect
from replit import db

app = flask.Flask(__name__)

@app.errorhandler(500)
def internal_server_error(e: str):
    return flask.jsonify(error=str(e)), 500


@app.route('/', methods=['GET', 'POST'])
def cadastroContatos():
  try:
    contatos = db.get('contatos', {});     
    if flask.request.method == "POST":      
      contatos[flask.request.form['email']] = {'nome': flask.request.form['nome'],
                                              'telefone': flask.request.form['telefone'],
                                              'assunto': flask.request.form['assunto'],
                                              'mensagem': flask.request.form['mensagem'],
                                              'resposta': flask.request.form['resposta']}
    db['contatos'] = contatos
    return flask.render_template('contatos.html', contatos=contatos)
  except Exception as e:
    logging.exception('failed to database')
    flask.abort(500, description=str(e) + ': ' + traceback.format_exc())

@app.route('/limparBanco', methods=['POST'])
def limparBanco():
  try:
    del db["contatos"];
    return flask.render_template('contatos.html')
  except Exception as e:
    logging.exception(e)
    return flask.render_template('contatos.html')

@app.route('/delete/<email>', methods=['POST'])
def delete(email):
    try:      
      contatos = db.get('contatos', {});  
      del contatos[email];
      db['contatos'] = contatos;
      return redirect('/');
    except Exception as e:
      logging.exception(e)
      return flask.render_template('contatos.html')

@app.route('/get/<email>', methods=['POST'])
def get(email):
    try:    
      if flask.request.method == "POST": 
        contatos = db.get('contatos', {});  
        contato={};
        contato={'email' : email,
               'nome' : contatos[email]['nome'],
               'telefone' : contatos[email]['telefone'],
               'assunto' : contatos[email]['assunto'],
               'mensagem' : contatos[email]['mensagem'],
               'resposta' : contatos[email]['resposta']};
        print(contato);
      return flask.render_template('update.html', contato=contato);
    except Exception as e:
      logging.exception(e)
      return flask.render_template('contatos.html')

@app.route('/update', methods=['POST'])
def update():
    try:      
      contatos = db.get('contatos', {});     
      contatos[flask.request.form['email']] = {'nome': flask.request.form['nome'],
                                              'telefone': flask.request.form['telefone'],
                                              'assunto': flask.request.form['assunto'],
                                              'mensagem': flask.request.form['mensagem'],
                                              'resposta': flask.request.form['resposta']}
      db['contatos'] = contatos
      return flask.render_template('contatos.html', contatos=contatos);
    except Exception as e:
      logging.exception('failed to database')
      flask.abort(500, description=str(e) + ': ' + traceback.format_exc())
 
app.run('0.0.0.0')