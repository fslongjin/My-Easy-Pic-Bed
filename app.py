import os
from flask import Flask, flash, request, redirect, url_for, render_template, current_app
from werkzeug.utils import secure_filename
from flask import send_from_directory, jsonify
import random, time
import db
import getConfig as gcf
import json

from flask.cli import with_appcontext

cf = gcf.get_config()

allowed_extensions = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
upload_folder = os.path.join(os.getcwd(), 'pics')
print(upload_folder)
app = Flask(__name__, instance_relative_config=True)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions


@app.route('/', methods=['POST', 'GET'] )
def upload_file():
    if request.method == 'POST':
        # 检查post请求中是否有文件
        if 'file' not in request.files:
            flash('你没有上传文件！')
            return redirect(request.url)
        file = request.files['file']
        print(file)
        if file.filename == '':
            flash('你没有选择文件！')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = str(int(time.time())) + str(random.randint(1, 99999)) + secure_filename(str(random.randint(1, 7887)) + file.filename)
            try:
                file.save(os.path.join(upload_folder, filename))
                database = db.get_db()
                database.execute(
                    'INSERT INTO pics (filename)'
                    ' VALUES (?)',
                    (filename,)
                )
                database.commit()
                if app.config['running_port'] != 80:
                    flash(app.config['running_domain'] + ':' + str(app.config['running_port']) + url_for('uploaded_file', filename=filename))
                else:
                    flash(app.config['running_domain'] + url_for('uploaded_file', filename=filename))
            except Exception as e:
                flash('出现错误！')
                print(e.args)

            return redirect(url_for('upload_file'))
        else:
            flash('不被服务器支持的文件！')
            return redirect(url_for('upload_file'))
    database = db.get_db()
    pcnum = database.execute("SELECT Count(*) FROM pics").fetchone()[0]
    print(pcnum)

    return render_template('bs_index.html', pic_num=pcnum)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/uploadapi', methods=['POST', 'GET'] )
def upload_file_api():
    app.logger.info('this is url')
    if request.method == 'POST':
        # 检查post请求中是否有文件
        if 'file' not in request.files:
            flash('你没有上传文件！')
            return redirect(request.url)
        file = request.files['file']
        print(file)
        imgUrl = ''
        if file.filename == '':
            flash('你没有选择文件！')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = str(int(time.time())) + str(random.randint(1, 99999)) + secure_filename(str(random.randint(1, 7887)) + file.filename)
            try:
                file.save(os.path.join(upload_folder, filename))
                database = db.get_db()
                database.execute(
                    'INSERT INTO pics (filename)'
                    ' VALUES (?)',
                    (filename,)
                )
                database.commit()
                if app.config['running_port'] != 80:
                    imgUrl = app.config['running_domain'] + ':' + str(app.config['running_port']) + url_for('uploaded_file', filename=filename)
                    flash(imgUrl)
                else:
                    imgUrl = app.config['running_domain'] + url_for('uploaded_file', filename=filename)
                    flash(imgUrl)
            except Exception as e:
                flash('出现错误！')
                print(e.args)
 
            return jsonify({'data': 'http://'+imgUrl}),200
        else:
            flash('不被服务器支持的文件！')
            return redirect(url_for('upload_file'))
    database = db.get_db()
    pcnum = database.execute("SELECT Count(*) FROM pics").fetchone()[0]
    print(pcnum)
    # print('this is url')
    # print(json.dumps({'data': imgUrl}))
    # return jsonify({'data': imgUrl}),200

if __name__ == '__main__':

    app.config['UPLOAD_FOLDER'] = upload_folder
    app.config['running_domain'] = cf['running_domain']
    app.config['running_port'] = cf['port']
    app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * int(cf['max_length'])
    app.config.from_mapping(
        SECRET_KEY='dgvbv43@$ewedc',
        DATABASE=os.path.join(app.instance_path, 'my-easy-pic-bed.sqlite'),
    )
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    try:
        os.mkdir(upload_folder)
    except Exception as e:
        pass

    app.run(debug=False, host=app.config['running_domain'], port=app.config['running_port'])






