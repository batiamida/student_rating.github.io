import React, { useState } from 'react';
import './static/css/edit_delete.css'
import axios from "axios";

function EditPage(props) {

  const [usersData, setUsersData] = useState(null);

  // const [username, setUsername] = useState(props.user.username);
  // // console.log(username);
  // const [firstName, setFirstName] = useState(props.user.firstName);
  // const [lastName, setLastName] = useState(props.user.lastName);
  // const [phone, setPhone] = useState(props.user.phone);
  // const [email, setEmail] = useState(props.user.email);

    async function getAuthUser() {
    const response = await axios({
      method: "GET",
      url:"http://127.0.0.1:5000/get_auth_user",
      headers: {
        Authorization: `Bearer ${props.token}`
      }
    });
    setUsersData(response.data);
  }
  // getAuthUser();
  // console.log(usersData);

  // const handleUsernameChange = (event) => {
  //   setUsername(event.target.value);
  // };
  //
  // const handleFirstNameChange = (event) => {
  //   setFirstName(event.target.value);
  // };
  //
  // const handleLastNameChange = (event) => {
  //   setLastName(event.target.value);
  // };
  //
  // const handlePhoneChange = (event) => {
  //   setPhone(event.target.value);
  // };
  //
  // const handleEmailChange = (event) => {
  //   setEmail(event.target.value);
  // };
  //
  // const handleSubmit = (event) => {
  //   event.preventDefault();
  //   // make API call to update user data using new values
  //   // redirect user to user listing page
  // };

  return (
    <body>
    {/*  <div className="container">*/}
    {/*    <form onSubmit={handleSubmit}>*/}
    {/*      <div className="form-group">*/}
    {/*        <label htmlFor="username">Username:</label>*/}
    {/*        <input type="text" id="username" name="username" value={username} onChange={handleUsernameChange} />*/}
    {/*      </div>*/}

    {/*      <div className="form-group">*/}
    {/*        <label htmlFor="firstName">First Name:</label>*/}
    {/*        <input type="text" id="firstName" name="firstName" value={firstName} onChange={handleFirstNameChange} />*/}
    {/*      </div>*/}

    {/*      <div className="form-group">*/}
    {/*        <label htmlFor="lastName">Last Name:</label>*/}
    {/*        <input type="text" id="lastName" name="lastName" value={lastName} onChange={handleLastNameChange} />*/}
    {/*      </div>*/}

    {/*      <div className="form-group">*/}
    {/*        <label htmlFor="phone">Phone:</label>*/}
    {/*        <input type="text" id="phone" name="phone" value={phone} onChange={handlePhoneChange} />*/}
    {/*      </div>*/}

    {/*      <div className="form-group">*/}
    {/*        <label htmlFor="email">Email:</label>*/}
    {/*        <input type="text" id="email" name="email" value={email} onChange={handleEmailChange} />*/}
    {/*      </div>*/}

    {/*      <div className="form-buttons">*/}
    {/*        <button type="submit" className="btn btn-primary">Save Changes</button>*/}
    {/*        <button type="button" className="btn btn-secondary">Cancel</button>*/}
    {/*      </div>*/}
    {/*    </form>*/}

    {/*    <hr />*/}

    {/*    /!*<h1>Delete User</h1>*!/*/}
    {/*    /!*<p>Are you sure you want to delete the user ""?</p>*!/*/}
    {/*    /!*<div className="form-buttons">*!/*/}
    {/*    /!*    <button type="submit" className="btn btn-danger">Delete User</button>*!/*/}
    {/*    /!*    <button type="button" className="btn btn-secondary">Cancel</button>*!/*/}
    {/*    /!*</div>*!/*/}
    {/*  </div>*/}
    </body>
  );
}

export default EditPage;
