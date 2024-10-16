from flask import Flask, render_template, request, redirect, url_for
import pymysql

app = Flask(__name__)

# Database connection setup (using MySQL)
def get_db_connection():
    return pymysql.connect(
        host='localhost',  
        user='root',       
        password='',       
        db='emails'     
    )

# Initialize database (Create table if not exists)
def init_db():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS emails (
            id INT AUTO_INCREMENT PRIMARY KEY,
            sender VARCHAR(255),
            subject VARCHAR(255),
            content TEXT,
            classification VARCHAR(255),
            sentiment VARCHAR(255),
            action VARCHAR(255)
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Route to display emails needing human attention
@app.route('/')
def inbox():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM emails WHERE action="escalate_to_human"')
    emails = c.fetchall()
    conn.close()
    return render_template('inbox.html', emails=emails)

# Route to view a specific email
@app.route('/email/<int:email_id>')
def view_email(email_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM emails WHERE id=%s', (email_id,))
    email = c.fetchone()
    conn.close()
    return render_template('view_email.html', email=email)

# Route to process actions on the email
@app.route('/email/<int:email_id>/action', methods=['POST'])
def email_action(email_id):
    action = request.form['action']
    # Update the email action in the database
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('UPDATE emails SET action=%s WHERE id=%s', (action, email_id))
    conn.commit()
    conn.close()
    # For now, just redirect back to inbox
    return redirect(url_for('inbox'))
@app.route('/email/<int:email_id>/feedback', methods=['POST'])
def provide_feedback(email_id):
    feedback = request.form['feedback']
    # Store feedback in the database
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('UPDATE emails SET feedback=%s WHERE id=%s', (feedback, email_id))
    conn.commit()
    conn.close()
    # Redirect back to email view
    return redirect(url_for('view_email', email_id=email_id))

if __name__ == '__main__':
    app.run(debug=True)
