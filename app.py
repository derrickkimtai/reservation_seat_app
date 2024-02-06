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

@app.route('/cancel-reservation/<int:seat_number>', methods=['POST'])
def cancel_reservation(seat_number):
    if seat_number <= total_seats and seat_number > 0 and seats[str(seat_number)]:
        seats[str(seat_number)] = False
        return jsonify({'message': f'Reservation for seat {seat_number} has been canceled.'}), 200
    else:
        return jsonify({'error': 'Seat is not reserved or does not exist.'}), 400

@app.route('/check-seat/<int:seat_number>')
def check_seat_availability(seat_number):
    if seat_number <= total_seats and seat_number > 0:
        return jsonify({'seat_number': seat_number, 'available': not seats[str(seat_number)]}), 200
    else:
        return jsonify({'error': 'Invalid seat number.'}), 400

@app.route('/seats')
def list_seats():
    return jsonify(seats), 200

@app.route('/reservation-summary/<name>')
def reservation_summary(name):
    reserved_seats = [seat for seat, reserved in seats.items() if reserved]
    return render_template('reservation_summary.html', name=name, reserved_seats=reserved_seats)

@app.route('/error')
def error():
    return render_template('error.html')

if __name__ == '__main__':
    app.run(debug=True)

