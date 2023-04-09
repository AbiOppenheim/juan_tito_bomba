from flask import Flask, request, render_template, redirect, url_for
import ast
from jinja2 import Environment
import itertools
env = Environment()
env.globals.update(len=len)

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        num_entries = int(request.form['num_musician'])
        people_data = []
        for i in range(num_entries):
            name = request.form['name{}'.format(i)]
            first_instrument = request.form['first_instrument{}'.format(i)]
            second_instrument = request.form['second_instrument{}'.format(i)]
            people_data.append((name, first_instrument, second_instrument))
        result = process_data(people_data)
        return redirect(url_for('result', results=str(result)))
    else:
        return render_template('index.html')

@app.route('/result')
def result():
    results_str = request.args.get('results')
    if results_str:
        results = ast.literal_eval(results_str)
    else:
        results = []
    return render_template('result.html', results=results)

def process_data(people_data):
    # Do some processing on the data
    results = []
    participants = {}
    for name, first_instrument, second_instrument in people_data:
        participants[name] = [first_instrument, second_instrument]
    instruments = set([item for sublist in participants.values() for item in sublist])
    

    instruments = set([item for sublist in participants.values() for item in sublist])
    n = len(participants) 
    best = min(len(instruments),n)

    # Generate all possible combinations of 0s and 1s for the binary list
    bit_list = [0, 1]
    combinations = list(itertools.product(bit_list, repeat=n))
    bits = [({list(participants.values())[i][b] for i,b in enumerate(t)},t) for t in combinations]
    bits = [t for t in bits if len(t[0])==best]
    if best == n:
        for i, option in enumerate(bits[:3]):
            result = []
            for name, bit in zip(participants, option[1]):
                print(f'{name} -> {participants[name][bit]}')
                result.append('{} -> {}'.format(name, participants[name][bit]))
            results.append(result)
    else:
        
        for opcion in range(len(bits)-1):
            ins = {}
            for name, bit in zip(participants, bits[opcion][1]):
                if participants[name][bit] not in ins:
                    ins[participants[name][bit]]=[name]
                else:
                    if bit:
                        ins[participants[name][bit]].append(name)
                    else:
                        ins[participants[name][bit]].insert(0, name)
            selected_participants = set()
            selected_instruments = set()
            result = []
            for instrument, names in ins.items():
                selected_participants.add(names[0])
                selected_instruments.add(instrument)
                print(f'{names[0]} -> {instrument}')
                result.append('{} -> {}'.format(names[0], instrument))
            result.append('Con los instrumentos que sobran: {}'.format(instruments-selected_instruments))
            result.append('Y personas sin asignar: {}'.format(participants.keys()-selected_participants))
            results.append(result)
    return results
if __name__ == '__main__':
    app.run(debug=True)
