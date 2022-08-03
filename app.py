from flask import Flask, request, render_template
import pickle
from ann_v2 import *
import telebot


bot = telebot.TeleBot("5068495886:AAEJRCENj1Sc_EDnqrkljHAungsGQg8JOog")

app = Flask(__name__)

model_file = open('model.pkl', 'rb')
model = pickle.load(model_file, encoding='bytes')

@app.route('/')
def index():
    return render_template('index.html', insurance_cost=0)

@app.route('/predict', methods=['POST'])
def predict():
    '''
    Predict the insurance cost based on user inputs
    and render the result to the html page
    '''
    CPU_LOAD, MEMORY_LOAD, DELAY, ERROR_1000, ERROR_1001, ERROR_1002, ERROR_1003, ERROR_1004, ERROR_1005, ERROR_1006  = [x for x in request.form.values()]

    print(CPU_LOAD, MEMORY_LOAD, DELAY, ERROR_1000, ERROR_1001, ERROR_1002, ERROR_1003,ERROR_1004,ERROR_1005,ERROR_1006)

    

    dummy = pandas.DataFrame({'CPU_LOAD': [int(CPU_LOAD)],
                    'MEMORY_LOAD': [int(MEMORY_LOAD)],
                    'DELAY': [int(DELAY)],
                    'ERROR_1000':[int(ERROR_1000)],
                    'ERROR_1001 ':[int(ERROR_1001)],
                    'ERROR_1002 ':[int(ERROR_1002)],
                    'ERROR_1003 ':[int(ERROR_1003)],
                    'ERROR_1004 ':[int(ERROR_1004)],
                    'ERROR_1005 ':[int(ERROR_1005)],
                    'ERROR_1006 ':[int(ERROR_1006)]})


    print(dummy)
    output = calculate(dummy)[0]
    akur = float("{:.4f}".format(calculate(dummy)[1]))*100
    print(akur)
    if output == 0:
        result = 'Database Issue'
        output = '0, Database Issue'
    if output == 1:
        result = 'Memory Issue'
        output = '1, Memory Issue'
    if output == 2:
        result = 'Network Delay' 
        output = '2, Network Delay' 




    final_result = "Terjadi Issue pada sistem saat ini, kemungkinan issue terdapat di " + result + " dengan tingkat akurasi: " + str(akur)
    bot.send_message(chat_id='680419925', text=final_result)

    
#     Note :
# DATABASE_ISSUE : 0
# MEMORY : 1
# NETWORK_DELAY : 2
    


    return render_template('index.html', insurance_cost=output ,akur=akur, CPU_LOAD=CPU_LOAD, MEMORY_LOAD=MEMORY_LOAD, 
        DELAY=DELAY,  ERROR_1000=ERROR_1000, ERROR_1001=ERROR_1001, ERROR_1002=ERROR_1002, ERROR_1003=ERROR_1003, ERROR_1004=ERROR_1004 ,ERROR_1005=ERROR_1005, ERROR_1006=ERROR_1006)


if __name__ == '__main__':
    app.run(debug=True)