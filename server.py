from flask import Flask, request
from model import train_model, preprocess, predict

dt = train_model()
app = Flask(__name__)


@app.route('/')
def index():
    return '''Server Works!<hr>
<form action="/processing" method="POST" enctype="multipart/form-data">
<input type="file" name="image">
<button>OK</button>
</form>    
'''


@app.route('/predict', methods=['POST'])
def process():
    if request.method == 'POST':
        input_data = request.form.get('input_data')
        processed_entry = preprocess(input_data)
        result = predict(dt, processed_entry)
        return str(result)


if __name__ == '__main__':
    app.run(debug=True)
