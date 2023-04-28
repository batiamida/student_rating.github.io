import React from 'react';
import './static/css/edit_delete.css'


function EditPage(props) {
    return (
        <body>
        <div className="container">
            <form method="POST" action="{{ url_for('update_student') }}">
                <div className="form-group">
                    <label htmlFor="username">Username:</label>
                    <input type="text" id="username" name="username" value="{{ user.username }}" />
                </div>

                <div className="form-group">
                    <label htmlFor="firstName">First Name:</label>
                    <input type="text" id="firstName" name="firstName" value="{{ user.firstName }}" />
                </div>

                <div className="form-group">
                    <label htmlFor="lastName">Last Name:</label>
                    <input type="text" id="lastName" name="lastName" value="{{ user.lastName }}" />
                </div>

                <div className="form-group">
                    <label htmlFor="phone">Phone:</label>
                    <input type="text" id="phone" name="phone" value="{{ user.phone }}" />
                </div>

                <div className="form-group">
                    <label htmlFor="email">Email:</label>
                    <input type="text" id="email" name="email" value="{{ user.email }}" />
                </div>

                {/*<div className="form-group">
                    <label htmlFor="password">Password:</label>
                    <input type="password" id="password" name="password" />
                </div>

                <div className="form-group">
                    <label htmlFor="confirm-password">Confirm Password:</label>
                    <input type="password" id="confirm-password" name="confirm-password" />
                </div>*/}

                <div className="form-buttons">
                    <button type="submit" className="btn btn-primary">Save Changes</button>
                    <button type="button" className="btn btn-secondary">Cancel</button>
                </div>
            </form>

            <hr />

            {/*<h1>Delete User</h1>*/}
            {/*<p>Are you sure you want to delete the user ""?</p>*/}
            {/*<div className="form-buttons">*/}
            {/*    <button type="submit" className="btn btn-danger">Delete User</button>*/}
            {/*    <button type="button" className="btn btn-secondary">Cancel</button>*/}
            {/*</div>*/}
        </div>
        </body>
    );
}

export default EditPage;
