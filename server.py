from flask import Flask, request
from model import train_model_classifier, preprocess, predict, train_model_regressor, read_csv, format_output
import flask

df = read_csv()
dt = train_model_classifier(df)
dtr = train_model_regressor(df)
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
        result_dt = predict(dt, processed_entry)
        result_dtr = predict(dtr, processed_entry)
        result = format_output(result_dt, result_dtr)
        res = flask.jsonify({"predictions": str(result)})
        res.headers.add('Access-Control-Allow-Origin', '*'),
        return res

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=False)
