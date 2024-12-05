from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Inisialisasi Flask dan konfigurasi database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Model untuk tabel pengeluaran
class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False)  # Tanggal disimpan dalam format Date

@app.route('/')
def index():
    """Halaman utama untuk menampilkan daftar pengeluaran"""
    expenses = Expense.query.all()
    total = sum(expense.amount for expense in expenses)
    return render_template('index.html', expenses=expenses, total=total)

@app.route('/add', methods=['POST'])
def add_expense():
    """Menambahkan pengeluaran baru"""
    try:
        name = request.form['name']
        category = request.form['category']
        amount = float(request.form['amount'])
        date = datetime.strptime(request.form['date'], '%Y-%m-%d').date()  # Format tanggal: YYYY-MM-DD

        if not name or not category or amount <= 0:
            return "Invalid input. Please fill all fields correctly.", 400

        new_expense = Expense(name=name, category=category, amount=amount, date=date)
        db.session.add(new_expense)
        db.session.commit()
        return redirect(url_for('index'))
    except Exception as e:
        return f"Error: {str(e)}", 500

@app.route('/delete/<int:id>')
def delete_expense(id):
    """Menghapus pengeluaran berdasarkan ID"""
    expense = Expense.query.get_or_404(id)
    db.session.delete(expense)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Membuat tabel database jika belum ada
    with app.app_context():
        db.create_all()

    # Jalankan aplikasi pada port 8081
    app.run(host='0.0.0.0', port=8081, debug=True)
