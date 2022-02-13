from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

ListOfMessages = []

UPLOAD_FOLDER = './upload'

app = Flask(__name__)
cors = CORS(app)
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['POST'])
def upload():
    for fname in request.files:
        f = request.files.get(fname)
        print(f)
        # f.save('./upload/%s' % secure_filename(fname))
        f.save('./static/image.png')
        from LSBSteg import LSBSteg
        import cv2
        #encoding
        steg = LSBSteg(cv2.imread("./static/image.png"))
        str1=""
        msg= ListOfMessages[-1]
        str1=msg['MessageText']
        # str1="This is a secret HADGEHOG!!!"
        print(str1)
        img_encoded = steg.encode_text(str1)
        cv2.imwrite("stego.png", img_encoded)
        # image.show()
        return "http://localhost:5000/static/stego.png", 200
    return "wrong request", 200

# получение зашифрованного сообщения
@app.route("/stego")
def GetStego():
    from LSBSteg import LSBSteg
    import cv2
    #decoding
    im = cv2.imread("stego.png")
    steg = LSBSteg(im)
    str1=""
    str1=steg.decode_text()
    print("Text value:",str1)
    return str1, 200


@app.route('/')
def dafault_route():
    return 'Messenger Flask server is running! ' \
            f'<br> Count of Messages {len(ListOfMessages)}'\
            '<br> <a href="/status">Check status</a>'

# отправка сообщений
@app.route("/mes", methods=['POST'])
def SendMessage():
    msg=""
    msg = request.json
    print(msg)
    # messages.append({ "UserName":"RusAl","MessageText":"Privet na sto let!!!","TimeStamp":"2021-03-05T18:23:10.932973Z"})
    ListOfMessages.append(msg)
    print(msg)
    msgtext = f"{msg['UserName']} <{msg['TimeStamp']}>: {msg['MessageText']}"
    print(f"Всего сообщений: {len(ListOfMessages)} Посланное сообщение: {msgtext}")
    return f"Сообщение отослано успшно. Всего сообщений: {len(ListOfMessages)} ", 200

# получение сообщений
@app.route("/mes/<int:id>")
def GetMessage(id):
    print(id)
    if id >= 0 and id < len(ListOfMessages):
        print(ListOfMessages[id])
        return ListOfMessages[id], 200
    else:
        return "Not found", 400

@app.route('/status')
def status():
    allmessages = ""
    for msg in ListOfMessages:
        allmessages += "<br> " + f"{msg['UserName']} <{msg['TimeStamp']}>: {msg['MessageText']}"
    allmessages +=f'<br> Count of Messages {len(ListOfMessages)}'
    return allmessages

if __name__ == '__main__':
    app.run()