from flask import Flask, render_template, jsonify, request
from flask_bootstrap import Bootstrap

app = Flask(__name__, template_folder='templates')
bootstrap = Bootstrap(app)

# Dummy data for seats
total_seats = 20
seats = {str(i): False for i in range(1, total_seats + 1)}

# Register error handler for 400 errors
@app.errorhandler(400)
def bad_request(error):
    return render_template('error.html'), 400

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/reserve-seat', methods=['GET', 'POST'])
def reserve_seat():
    if request.method == 'POST':
        name = request.form.get('name')
        seat_number = request.form.get('seatNumber')

        if seat_number.isdigit() and 1 <= int(seat_number) <= total_seats:
            seat_number = int(seat_number)
            if not seats[str(seat_number)]:
                seats[str(seat_number)] = True
                return jsonify({'success': True, 'message': f'Seat {seat_number} has been reserved for {name}.'}), 200
            else:
                return jsonify({'success': False, 'error': 'Seat is already reserved.'}), 400
        else:
            return jsonify({'success': False, 'error': 'Invalid seat number.'}), 400
    return render_template('reserve_seat.html', total_seats=total_seats)


if __name__ == '__main__':
    app.run(debug=True)

