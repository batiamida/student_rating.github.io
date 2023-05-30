import React, { useState, useEffect } from 'react';
import useToken from './useToken';

// import { useHistory } from 'react-router-dom';

import axios from "axios";
import './static/css/edit_delete.css';

function EditPage(props) {
  const { token, removeToken, setToken } = useToken();

  const [HistoryData, setHistory] = useState(null);

  const [usersData, setUsersData] = useState(null);

  function redirectToPage() {
    window.location.href = '/user_listing';
  }

  useEffect(() => {
    async function getAuthUser() {
      const response = await axios({
        method: "GET",
        url:"http://127.0.0.1:5000/get_auth_user",
        headers: {
          Authorization: `Bearer ${props.token}`
        }
      });
      setUsersData(response.data.user);
      setHistory(response.data.user);
    }
    getAuthUser();
  }, [props.token]);

  const handleInputChange = (event) => {
    const target = event.target;
    const name = target.name;
    const value = target.value;

    setUsersData({
      ...usersData,
      [name]: value
    });
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    // make API call to update user data using new values
    const model = usersData.model.toLowerCase();
    console.log(props.token);
    console.log(`http://127.0.0.1:5000/${model}`);
    console.log(usersData);
    const response = await axios.put(`http://127.0.0.1:5000/${model}`, usersData, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    });
    //
    const newToken = response.data.token;
    setToken(newToken);

    // redirect user to user listing page
    redirectToPage();
  };

  const handleCancel = () => {
    // Check if HistoryData is not null before setting the usersData state to its value
    // This prevents setting the state to null if HistoryData is not defined
    if (HistoryData !== null) {
      setUsersData(HistoryData);
    }
  };


  return (
    <body>
      <div className="container">
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="username">Username:</label>
            <input type="text" id="username" name="username" value={usersData?.username || ''} onChange={handleInputChange} />
          </div>

          <div className="form-group">
            <label htmlFor="firstName">First Name:</label>
            <input type="text" id="firstName" name="firstName" value={usersData?.firstName || ''} onChange={handleInputChange} />
          </div>

          <div className="form-group">
            <label htmlFor="lastName">Last Name:</label>
            <input type="text" id="lastName" name="lastName" value={usersData?.lastName || ''} onChange={handleInputChange} />
          </div>

          <div className="form-group">
            <label htmlFor="email">Email:</label>
            <input type="text" id="email" name="email" value={usersData?.email || ''} onChange={handleInputChange} />
          </div>
          {/*<div>{usersData.model}</div>*/}
          <div className="form-buttons">
            <button type="submit" className="btn btn-primary">Save Changes</button>
            <button type="button" className="btn btn-secondary" onClick={handleCancel}>Cancel</button>
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
