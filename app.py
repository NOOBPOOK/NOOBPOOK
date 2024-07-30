from flask import Flask, jsonify, make_response, request
from Services.gmail import Gmail
import json

app = Flask(__name__)

@app.route("/")
def hello_from_root():
    return jsonify(message='Hello from root!')

@app.route("/hello")
def hello():
    return jsonify(message='Hello from path!')

"""
This endpoint is used for sending email message
Its a Post request
{
"message": "Hello, how are you?",
"receiver": "reciever@gmail.com",
"subject": "Testing"
}
"""
@app.route("/email", methods=['POST'])
def send_email():
    data = request.get_json()
    gmail_obj = Gmail()
    try:
        message = data['message']
        sender_email = data['receiver']
        subject = data['subject']
    except Exception as e:
        return jsonify(message = "Required details missing"),404
    try:
        sent_msg_id = gmail_obj.send_message(
            message = message,
            to = sender_email,
            subject = subject,
        )
        return jsonify(message_id = f'{sent_msg_id}'),200
    except Exception as e:
        return jsonify(message = "An Internal Server Error Occured",
                       error = str(e)), 500

@app.errorhandler(404)
def resource_not_found(e):
    return make_response(jsonify(error='Not found!'), 404)
