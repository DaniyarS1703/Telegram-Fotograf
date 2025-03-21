from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Photographer(db.Model):
    __tablename__ = 'photographers'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    telegram_id = db.Column(db.String(50))  # Поле для хранения Telegram ID фотографа
    avatar = db.Column(db.Text)
    avatar_public_id = db.Column(db.Text)  # Поле для хранения public_id из Cloudinary
    description = db.Column(db.Text)
    rating = db.Column(db.Numeric(2, 1), default=0.0)
    portfolio = db.Column(db.Text)  # Хранение портфолио как JSON-строка
    city = db.Column(db.Text)

    def get_portfolio(self):
        import json
        if self.portfolio:
            try:
                return json.loads(self.portfolio)
            except Exception:
                return []
        return []


class Client(db.Model):
    __tablename__ = 'clients'
    
    id = db.Column(db.Integer, primary_key=True)
    telegram_id = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(50))
    description = db.Column(db.Text)
    city = db.Column(db.Text)
    country = db.Column(db.Text)


# Модель Booking для бронирования
class Booking(db.Model):
    __tablename__ = 'bookings'
    
    id = db.Column(db.Integer, primary_key=True)
    photographer_id = db.Column(db.Integer, db.ForeignKey('photographers.id'), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    booking_date = db.Column(db.Date, nullable=False)  # Дата бронирования
    booking_time = db.Column(db.Time, nullable=True)   # Время бронирования (опционально)
    status = db.Column(db.String(50), default='pending') # Статус бронирования (например, pending, confirmed, canceled)

    # Устанавливаем связи
    photographer = db.relationship('Photographer', backref=db.backref('bookings', lazy=True))
    client = db.relationship('Client', backref=db.backref('bookings', lazy=True))


# Модель UnavailableDate для управления недоступными датами фотографа
class UnavailableDate(db.Model):
    __tablename__ = 'unavailable_dates'
    
    id = db.Column(db.Integer, primary_key=True)
    photographer_id = db.Column(db.Integer, db.ForeignKey('photographers.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)  # Дата, когда фотограф недоступен
    
    photographer = db.relationship('Photographer', backref=db.backref('unavailable_dates', lazy=True))
