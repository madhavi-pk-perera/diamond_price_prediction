from flask import Flask, render_template, request
import pickle
import numpy as np

app = Flask(__name__, template_folder='Templates')

def prediction(lst):
    filename = 'model/diamond_price_predictor.pickle'
    with open (filename, 'rb') as file:
        model = pickle.load (file)
    pred_value = model.predict([lst])
    return pred_value

@app.route('/', methods=['POST','GET'])
def index():
    pred_value = 0
    if request.method == 'POST':
        carat = request.form['carat']
        x = request.form['x']
        y= request.form['y']
        z= request.form['z']
        cut= request.form['cut']
        color=request.form['color']
        clarity= request.form['clarity']

        feature_list=[]
        feature_list.append(float(carat))
        feature_list.append(float(x))
        feature_list.append(float(y))
        feature_list.append(float(z))
       

        cut_list = ['Fair','Good', 'Very Good', 'Premium', 'Ideal']
        color_list = ['D','E','F','G','H','I','J']
        clarity_list= ['SI1','VS2','SI2','VS1','VVS2','VVS1','IF','I1']

        def traverse_list(lst,value):
            for item in lst:
                if item==value:
                    feature_list.append(1)
                else:
                    feature_list.append(0)
        
        traverse_list(cut_list, cut)
        traverse_list(color_list, color)
        traverse_list(clarity_list, clarity)
                    

        


        #print(feature_list)

        pred_value = prediction(feature_list)
        pred_value = np.round(pred_value[0],2)*353
    
    
    return render_template('index.html', pred_value=pred_value)



if __name__ == '__main__':
    app.run(debug= True)

