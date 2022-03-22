from flask import Flask, redirect, render_template, request, url_for


app = Flask(__name__)


@app.route('/')
def index():
    context = {
        'name': request.args.get('name'),
        'message': request.args.get('message')
    }

    if context['name'] is None and context['message'] is None:
        return redirect(url_for('default', name = 'Rekruto', message = 'Давай дружить!'))
    
    return render_template('index.html', context=context)


@app.route('/')
def default(name, message):
    context = {
        'name': name,
        'message': message
    }
    return render_template('index.html', context=context)


if __name__ == '__main__':
    app.run(debug=True)