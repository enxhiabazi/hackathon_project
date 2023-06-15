from datetime import datetime
import os
from flask_app import app
from flask_app.models.user import User
from flask_app.models.auto import Auto
from flask import render_template, redirect, session, request, flash

from .env import UPLOAD_FOLDER
from .env import ALLOWED_EXTENSIONS

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
from werkzeug.utils import secure_filename

#Check if the format is right
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.',1)[-1].lower() in ALLOWED_EXTENSIONS

@app.route('/sell/auto')
def sellAuto():
    if 'user_id' in session:
        data = {
            'user_id': session['user_id']
        }
        loggedUser = User.get_user_by_id(data)
        if loggedUser['isVerified'] == 0:
            return redirect('/verify/email')
        return render_template('sell.html', loggedUser = loggedUser)
    return redirect('/')

@app.route('/create/auto', methods = ['POST'])
def createAuto():
    if 'user_id' in session:
        if not Auto.validate_auto(request.form):
            return redirect(request.referrer)
        if not request.files['image']:
            flash('Auto image is required','image')
            return redirect(request.referrer)
        image = request.files['image']
        if not allowed_file(image.filename):
            flash('Image should be in png, jpg, jpeg format!', 'image')
            return redirect(request.referrer)
        
        if image and allowed_file(image.filename):
            filename1 = secure_filename(image.filename)
            time = datetime.now().strftime("%d%m%Y%S%f")
            time += filename1
            filename1 = time
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename1))
        

        data = {
            'make': request.form['make'],
            'model': request.form['model'],
            'price': request.form['price'],
            'year': request.form['year'],
            'new_used': request.form['new_used'],
            'comments': request.form['comments'],
            'isAvailable': 0,
            'user_id': session['user_id'],
            'image': filename1
        }
        Auto.save(data)
        return redirect('/buy/auto')
    return redirect('/')

@app.route('/buy/auto')
def buyAuto():
    if 'user_id' in session:
        data = {
            'user_id': session['user_id']
        }
        user = User.get_user_by_id(data)
        auto = Auto.get_all()
        likedAutos = User.get_user_liked_autos(data)
        savedAutos = User.get_user_saved_autos(data) 
    return render_template('buy.html', user = user, auto = auto, likedAutos=likedAutos,savedAutos=savedAutos)

@app.route('/give/auto/for/rent')
def giveAutoForRent():
    if 'user_id' in session:
        data = {
            'user_id': session['user_id']
        }
        user = User.get_user_by_id(data)
        auto = Auto.get_all()
    return render_template('giveForRent.html', user = user, auto = auto)

@app.route('/create/auto/for/rent', methods = ['POST'])
def createAutoForRent():
    if 'user_id' in session:
        if not Auto.validate_auto(request.form):
            return redirect(request.referrer)
        if not request.files['image']:
            flash('Auto image is required','image')
            return redirect(request.referrer)
        image = request.files['image']
        if not allowed_file(image.filename):
            flash('Image should be in png, jpg, jpeg format!', 'image')
            return redirect(request.referrer)
        
        if image and allowed_file(image.filename):
            filename1 = secure_filename(image.filename)
            time = datetime.now().strftime("%d%m%Y%S%f")
            time += filename1
            filename1 = time
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename1))
        

        data = {
            'make': request.form['make'],
            'model': request.form['model'],
            'price': request.form['price'],
            'year': request.form['year'],
            'new_used': request.form['new_used'],
            'comments': request.form['comments'],
            'isAvailable': 1,
            'user_id': session['user_id'],
            'image': filename1
        }
        Auto.save(data)
        return redirect('/rent/auto')
    return redirect('/')

@app.route('/rent/auto')
def rentCar():
    if 'user_id' in session:
        data = {
            'user_id': session['user_id']
        }
        user = User.get_user_by_id(data)
        auto = Auto.get_all_rent()
        likedAutos = User.get_user_liked_autos(data)
        savedAutos = User.get_user_saved_autos(data) 
    return render_template('rent.html', user = user, auto= auto, likedAutos=likedAutos,savedAutos=savedAutos)


@app.route('/show/<int:id>/auto')
def showUsersAutos(id):
    if 'user_id' in session:
        data = {
            'user_id': id
        }
        user = User.get_user_by_id(data)
        auto = Auto.get_users_autos(data)
        likedAutos = User.get_user_liked_autos(data)
        savedAutos = User.get_user_saved_autos(data)
    return render_template('showUsersAutos.html', auto = auto, user = user, likedAutos = likedAutos,savedAutos=savedAutos)

@app.route('/auto/<int:id>')
def viewAuto(id):
    if 'user_id' in session:
        data = {
            'user_id': session['user_id'],
            'auto_id': id
        }
        user = User.get_user_by_id(data)
        if user['isVerified'] == 0:
            return redirect('/verify/email')
        auto = Auto.get_auto_by_id(data)
        likesNr = Auto.get_auto_likers(data)
        likedAutos = User.get_user_liked_autos(data)
        comment = Auto.get_auto_comments(data)
        postCreator = Auto.get_autos_and_their_users(data)
        return render_template('showOne.html', user = user, postCreator=postCreator,auto= auto, likesNr= likesNr, likedAutos=likedAutos, comment = comment)
    return redirect('/')

@app.route('/update/auto/<int:id>', methods = ['post'])
def updateAuto(id):
    if 'user_id' in session:
        data1 = {
            'user_id': session['user_id'],
            'auto_id': id
        }
        loggedUser = User.get_user_by_id(data1)
        if loggedUser['isVerified'] == 0:
            return redirect('/verify/email')
        auto = Auto.get_auto_by_id(data1)
        if loggedUser['id'] == auto['user_id']:
            if not Auto.validate_auto(request.form):
                return redirect(request.referrer)
            data = {
                'make': request.form['make'],
                'model': request.form['model'],
                'price': request.form['price'],
                'year': request.form['year'],
                'new_used': request.form['new_used'],
                'comments': request.form['comments'],
                'auto_id': id
            }
            Auto.update(data)
            return redirect('/buy/auto')
        return redirect('/dashboard')
    return redirect('/')

@app.route('/update/rent/auto/<int:id>', methods = ['post'])
def updateRentAuto(id):
    if 'user_id' in session:
        data1 = {
            'user_id': session['user_id'],
            'auto_id': id
        }
        loggedUser = User.get_user_by_id(data1)
        if loggedUser['isVerified'] == 0:
            return redirect('/verify/email')
        auto = Auto.get_auto_by_id(data1)
        if loggedUser['id'] == auto['user_id']:
            if not Auto.validate_auto(request.form):
                return redirect(request.referrer)
            data = {
                'make': request.form['make'],
                'model': request.form['model'],
                'price': request.form['price'],
                'year': request.form['year'],
                'new_used': request.form['new_used'],
                'comments': request.form['comments'],
                'auto_id': id
            }
            Auto.update(data)
            return redirect('/rent/auto')
        return redirect('/dashboard')
    return redirect('/')

@app.route('/edit/auto/<int:id>')
def editAuto(id):
    if 'user_id' in session:
        data = {
            'user_id': session['user_id'],
            'auto_id': id
        }
        loggedUser = User.get_user_by_id(data)
        if loggedUser['isVerified'] == 0:
            return redirect('/verify/email')
        auto = Auto.get_auto_by_id(data)
        if loggedUser['id'] == auto['user_id']:
            return render_template('editBuy.html', loggedUser = loggedUser, auto= auto)
        return redirect('/dashboard')
    return redirect('/')

@app.route('/edit/rent/auto/<int:id>')
def editRentAuto(id):
    if 'user_id' in session:
        data = {
            'user_id': session['user_id'],
            'auto_id': id
        }
        loggedUser = User.get_user_by_id(data)
        if loggedUser['isVerified'] == 0:
            return redirect('/verify/email')
        auto = Auto.get_auto_by_id(data)
        if loggedUser['id'] == auto['user_id']:
            return render_template('editRent.html', loggedUser = loggedUser, auto= auto)
        return redirect('/dashboard')
    return redirect('/')

@app.route('/delete/auto/<int:id>')
def deleteAuto(id):
    if 'user_id' in session:
        data = {
            'user_id': session['user_id'],
            'auto_id': id
        }
        loggedUser = User.get_user_by_id(data)
        if loggedUser['isVerified'] == 0:
            return redirect('/verify/email')
        auto = Auto.get_auto_by_id(data)
        if loggedUser['id'] == auto['user_id']:
            Auto.deleteAllLikes(data)
            Auto.deleteAllComments(data)
            Auto.deleteAllSaves(data)
            Auto.delete(data)
            return redirect('/buy/auto')
        return redirect('/dashboard')
    return redirect('/')

@app.route('/comment/<int:id>', methods = ['post'])
def comment(id):
    if 'user_id' in session:
        data = {
            'comments':request.form['comments'],
            'user_id': session['user_id'],
            'auto_id': id
        }
        Auto.comment(data)
        return redirect(request.referrer)
    return redirect('/')

@app.route('/delete/comment/<int:autoid>/<int:Cid>')
def deleteComment(autoid, Cid):
    if 'user_id' in session:
        data = {
            'user_id': session['user_id'],
            'auto_id': autoid,
            'comments_id': Cid
        }
        Auto.deleteComment(data)
        return redirect(request.referrer)
    return redirect('/dashboard')

@app.route('/like/<int:id>')
def likeAuto(id):
    if 'user_id' in session:
        data = {
            'user_id': session['user_id'],
            'auto_id': id
        }
        
        likedAuto = User.get_user_liked_autos(data)
        if id not in likedAuto:
            Auto.addLike(data)
            return redirect(request.referrer)
        return redirect(request.referrer)
    return redirect('/')

@app.route('/unlike/<int:id>')
def unlikeAuto(id):
    if 'user_id' in session:
        data = {
            'user_id': session['user_id'],
            'auto_id': id
        }
        Auto.unLike(data)
        return redirect(request.referrer)
    return redirect('/')

@app.route('/save/<int:id>')
def savedAuto(id):
    if 'user_id' in session:
        data = {
            'user_id': session['user_id'],
            'auto_id': id
        }
        
        savedAuto = User.get_user_saved_autos(data)
        if id not in savedAuto:
            Auto.addSave(data)
            return redirect(request.referrer)
        return redirect(request.referrer)
    return redirect('/')

@app.route('/unsave/<int:id>')
def unsavedAuto(id):
    if 'user_id' in session:
        data = {
            'user_id': session['user_id'],
            'auto_id': id
        }
        Auto.unSave(data)
        return redirect(request.referrer)
    return redirect('/')


