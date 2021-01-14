from flask import Blueprint, render_template, request, redirect, session, flash, url_for

from blog.models import User
from blog.forms import EditUserForm, AddUserForm

# define our blueprint
user_bp = Blueprint('user', __name__)


@user_bp.route('/add/user', methods=['GET', 'POST'])
def add_user():

    # create instance of our form
    add_user_form = AddUserForm()

    # handle form submission
    if add_user_form.validate_on_submit():

        # create user object
        user = User()

        # set object attributes
        user.username = add_user_form.username.data
        user.password = add_user_form.password.data
        user.first_name = add_user_form.first_name.data
        user.last_name = add_user_form.last_name.data
        user.biography = add_user_form.biography.data

        # save the user object
        user.save()

        # # another way
        # my_user = User(username = 'cookie', password = '1234')
        # my_user.save()

    # render the template
    return render_template("user/add-user.html", form=add_user_form)


@user_bp.route('/user/edit/<int:id>', methods=['GET', 'POST'])
def edit_user(id):

    # create instance of our form
    edit_user_form = EditUserForm()
    if request.method == "GET":
        edit_user_form.first_name.data = session['first_name']
        edit_user_form.last_name.data = session['last_name']
        edit_user_form.biography.data = session['biography']

    # handle form submission

    if edit_user_form.validate_on_submit():

        # read post values from the form
        first_name = edit_user_form.first_name.data
        last_name = edit_user_form.last_name.data
        biography = edit_user_form.biography.data

        print(first_name, last_name)
        # get the DB connection
        db = get_db()

        try:
            # update user information
            db.execute(
                f"""UPDATE user SET first_name = '{first_name}', last_name ='{last_name}',biography = '{biography}' WHERE id = '{session['uid']}'   """)
            db.commit()

            # update session
            session['first_name'] = first_name
            session['last_name'] = last_name
            session['biography'] = biography

            #  flash masseag
            flash("User information updated successfully!")

            # redirect
            return redirect(url_for('user.view_user', id=session['uid']))

        except sqlite3.Error as er:
            print('SQLite error: %s' % (' '.join(er.args)))
            return redirect("/404")

    # redner the login template
    return render_template("user/edit-user.html", form=edit_user_form)


@user_bp.route('/users')
def get_users():

    # get all users
    users = User.objects

    # render 'list.html' blueprint with users
    return render_template('user/list.html', users=users)


@user_bp.route('/user/view/<int:id>')
def view_user(id):
    # get the DB connection
    db = get_db()

    # get user by id
    user = db.execute(f'''select * from user  WHERE id = {id}''').fetchone()

    # render 'profile.html' blueprint with user
    return render_template('user/view-user.html', user=user)
