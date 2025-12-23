from flask import Flask, render_template, session, request, redirect, url_for
from models import init_db
from routes.feedback import feedback_bp
from routes.admin import admin_bp
from routes.shop import shop_bp
from routes.api import api_bp
import bcrypt

app = Flask(__name__)
app.secret_key = 'super_secret_key'  

init_db()



app.register_blueprint(feedback_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(shop_bp)
app.register_blueprint(api_bp)




@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/shop')
def shop():
    menu_data = {
        "Піца": [
            {"name": "Маргарита", "price": "120 грн", "ingredients": "Томатний соус, сир моцарелла, базилік", "image": "static/img/pizza_1.png"},
            {"name": "Пеппероні", "price": "150 грн", "ingredients": "Томатний соус, сир моцарелла, пеппероні", "image": "static/img/pizza_2.png"},
            {"name": "Чотири Сира", "price": "170 грн", "ingredients": "Томатний соус, сир моцарелла, пармезан, горгонзола, фета", "image": "static/img/pizza_3.png"},
            {"name": "Гавайська", "price": "200 грн", "ingredients": "Томатний соус, сир моцарелла, ананас, шинка", "image": "static/img/pizza_4.png"},
            {"name": "Карбонара", "price": "140 грн", "ingredients": "Томатний соус, сир моцарелла, ананас", "image": "static/img/pizza_5.png"},
            {"name": "Сицилійська", "price": "140 грн", "ingredients": "Анчоуси, свіжі томати та сир пекорино", "image": "static/img/pizza_6.png"}
        ],
        "Напої безалкогольні": [
            {"name": "Живчик", "price": "30 грн", "ingredients": "Газована вода, цукор, ароматизатори", "image": "static/img/drink_1.png"},
            {"name": "Monster energy", "price": "60 грн", "ingredients": "Газована вода, кофеїн, цукор, ароматизатори", "image": "static/img/drink_2.png"},
            {"name": "Red Bull", "price": "40 грн", "ingredients": "Газована вода, цукор, ароматизатори", "image": "static/img/drink_3.png"},
            {"name": "Reign", "price": "55 грн", "ingredients": "Газована вода, цукор, ароматизатори", "image": "static/img/drink_4.png"},
            {"name": "Coca Cola", "price": "45 грн", "ingredients": "Газована вода, цукор, ароматизатори", "image": "static/img/drink_5.png"},
            {"name": "Fanta", "price": "45 грн", "ingredients": "Газована вода, цукор, ароматизатори", "image": "static/img/drink_6.png"}
        ],
        "Алкогольні напої": [
            {"name": "Пиво", "price": "50 грн", "ingredients": "Солод, вода, хміль, дріжджі", "image": "static/img/alcodrink_1.jpg"}
        ],
        "Новинки": [
            {"name": "Піца від бабусі Галі", "price": "200 грн", "ingredients": "Помідор, шинка, огірок, капуста, томатний соус", "image": "static/img/pizza_7.png"}
        ]
    }

    return render_template('shop.html', menu=menu_data)

@app.route('/feedback')
def feedback():
    return render_template('feedback.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/discount')
def discount():
    return render_template('discount.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    item_name = request.form.get('item_name') 
    item_price = int(request.form.get('item_price').split()[0])  
    item_image = request.form.get('item_image')  

    
    if 'cart' not in session:
        session['cart'] = {}

    cart = session['cart']

    
    if item_name in cart:
        cart[item_name]['quantity'] += 1
    else:
        
        cart[item_name] = {
            'name': item_name,
            'price': item_price,
            'quantity': 1,
            'image': item_image
        }

    session['cart'] = cart  
    session.modified = True  

    return redirect(url_for('shop'))

@app.route('/cart', methods=['GET'])
def cart():
    cart = session.get('cart', {})  
    total = sum(item['price'] * item['quantity'] for item in cart.values()) 
    return render_template('cart.html', cart=cart, total=total)

@app.route('/checkout', methods=['POST'])
def checkout():
    email = request.form.get('email')  
    address = request.form.get('address')  
    cart = session.get('cart', {})  

    if not cart:
        return redirect(url_for('cart'))  

   

    
    session.pop('cart', None)

    return render_template('order_success.html', email=email, address=address)

@app.route('/clear_cart', methods=['POST'])
def clear_cart():
    session.pop('cart', None)  
    return redirect(url_for('cart'))

if __name__ == '__main__':
    app.run(debug=True)

user_bp = Blueprint('user', name)

def validate_registration_data(username, email, password, confirm_password):
    if not username or not email or not password or not confirm_password:
        return "Всі поля є обов'язковими."
    if len(username) < 3:
        return "Ім'я користувача повинно бути не менше 3 символів."
    if not re.match(r'^[a-zA-Z0-9_.-]+$', username):
        return "Ім'я користувача може містити тільки букви, цифри, _, . або -."
    if not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
        return "Некоректний формат email."
    if len(password) < 8:
        return "Пароль повинен бути не менше 8 символів."
    if not re.search(r'[A-Za-z]', password) or not re.search(r'\d', password):
        return "Пароль повинен містити букви та цифри."
    if password != confirm_password:
        return "Паролі не співпадають."
    return None

def get_current_user():
    """
    Функція для отримання поточного користувача з сесії.
    Повертає дані користувача або None, якщо користувач не авторизований.
    """
    user_id = session.get('user_id')
    if user_id:
        conn = get_db_connection()
        try:
            cur = conn.cursor()
            user = cur.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
            return user
        finally:
            conn.close()  # Закрити з'єднання після завершення
    return None


@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        validation_error = validate_registration_data(username, email, password, confirm_password)
        print(validation_error)
        if validation_error:
            return redirect(url_for('user.register'))

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        conn = get_db_connection()  # Отримати нове з'єднання
        try:
            existing_user = conn.execute('SELECT * FROM users WHERE username = ? OR email = ?', (username, email)).fetchone()
            if existing_user:
                print("Користувач із таким ім'ям або email вже існує.") #перевірка на існуючий ім'я чи email
                return redirect(url_for('user.register'))

            conn.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)', 
                         (username, email, hashed_password))
            conn.commit()
            print('записанна в базу даних')
        finally:
            conn.close()  # Закрити з'єднання

        print("Реєстрація успішна! Ви можете увійти в систему.")
        return redirect(url_for('user.login'))

    return render_template('register.html')

@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        try:
            user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
            if user:
                stored_password = user['password'].encode('utf-8') if isinstance(user['password'], str) else user['password']
                if bcrypt.checkpw(password.encode('utf-8'), stored_password):
                    # Успішний вхід
                    session['user_id'] = user['id']
                    flash("Ви успішно увійшли.")
                    return redirect(url_for('home'))
            flash("Невірний email або пароль.")
        finally:
            conn.close()  # Закриваємо з'єднання
    return render_template('login.html')

@user_bp.route('/logout')
def logout():
    session.pop('user_id', None)  # Видаляємо user_id з сесії
    print("Ви вийшли з системи.")
    return redirect(url_for('home'))
#видає none якщо не найде юзера а так видає його id 
def auth():
    return session.get('user_id') is not None