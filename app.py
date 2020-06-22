import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle



solution, existing_numbers ,sudoku , cropped_sudoku = 0,0,0,0
raw_img_count=0
raw_img_path=r"static\img\sudoku\raw_sudoku_{count}.jpg".format(count=str(raw_img_count))
crop_img_path=r"static\img\sudoku\cropped_sudoku_{count}.jpg".format(count=str(raw_img_count))
img_count = 0
img_name = "solved_cropped{no}_sudoku_{count}.jpg".format(no=raw_img_count, count=img_count)
img_path = r"static\img\sudoku\{}".format(img_name)
active_num=""
def sudoku_ready():
    global solution , existing_numbers , sudoku ,cropped_sudoku ,raw_img_count , img_count , active_num
    solution , existing_numbers , sudoku ,cropped_sudoku = sudoku_crop_solve_save(raw_img_count , required_num_in_sol="0")
    print(sudoku)
    if sudoku :
        img_count=0
        active_num=""
        print("sudoku_ready")
        return True
    else :
        return False

def sudoku_filter_sol(req_num):
    if (req_num=="All"):
        req_num="123456789"
    global img_count , img_path , img_name
    img_count=req_num
    img_name = "solved_cropped{no}_sudoku_{count}.jpg".format(no=raw_img_count, count=img_count)
    img_path = r"static\img\sudoku\{}".format(img_name)

    cropped_sudoku_copy = cropped_sudoku.copy() 
    sudoku.write_solution(cropped_sudoku_copy, solution, ignore=existing_numbers ,required_num_in_sol =req_num)
    cropped_sudoku_copy = cv2.resize(cropped_sudoku_copy , (450,450))
    cv2.imwrite( img_path, cropped_sudoku_copy )
    return True


app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    int_features = [int(x) for x in request.form.values()]
    final_features = [np.array(int_features)]
    prediction = model.predict(final_features)

    output = round(prediction[0], 2)

    return render_template('index.html', prediction_text='Employee Salary should be $ {}'.format(output))


if __name__ == "__main__":
    app.run(debug=True)
