from flask import Flask, render_template, Response, jsonify,request, send_file
from opencsv_video import generate_frames, get_license_plate_data, delete_license_plate_data, delete_license_plate_row
from io import BytesIO
import pandas as pd
import zipfile
import os
import copy

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html') 

# to show the live video
@app.route('/video')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# to get the license plate data
@app.route('/get_license_plate_data', methods=['GET'])
def get_license_plate_data_route():
    plates = get_license_plate_data()
    return jsonify(plates)

# to delete all license plate data
@app.route('/delete_license_plate_data', methods=['POST'])
def delete_license_plate_data_route():
    delete_license_plate_data()
    print("rawr",get_license_plate_data())
    return jsonify({"message": "License plate data deleted successfully"})

# to delete a row from license plate data
@app.route('/delete_license_plate', methods=['POST'])
def delete_license_plate():
    data = request.get_json()
    license_plate = data.get('license_plate')

    if not license_plate:
        return jsonify({"error": "No license plate provided"}), 400

    if delete_license_plate_row(license_plate):
        return jsonify({"message": "License plate deleted successfully"}), 200
    
    return jsonify({"error": "OH NO!!!!"}), 400

# to download all license plate data
@app.route('/download_license_plate_data', methods=['GET'])
def download_license_plate_data():        
    zip_output = BytesIO()
    folder_path = 'static/plates'

    # create zip
    with zipfile.ZipFile(zip_output, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # add the images
        for foldername, subfolders, filenames in os.walk(folder_path):
            for filename in filenames:
                file_path = os.path.join(foldername, filename)
                arcname = os.path.relpath(file_path, folder_path)
                zipf.write(file_path, arcname)

        license_plate_data = copy.deepcopy(get_license_plate_data())
        
        for item in license_plate_data:
            if 'file_path' in item:
                item['file_path'] = item['file_path'].replace('static/plates/', '')
                
        df = pd.DataFrame(license_plate_data)

        # add the excel file
        excel_output = BytesIO()
        with pd.ExcelWriter(excel_output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='License Plates')
        excel_output.seek(0)

        zipf.writestr('license_plate_data.xlsx', excel_output.getvalue())

    zip_output.seek(0)
    
    return send_file(
        zip_output,
        download_name="license_plate_data.zip",
        mimetype="application/zip", 
        as_attachment=True 
    )

if __name__ == '__main__':
    app.run(debug=True, threaded=True)
