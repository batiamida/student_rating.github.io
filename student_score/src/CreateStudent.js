import React, { useState, useEffect } from 'react';
import useToken from './useToken';

import axios from "axios";
import './static/css/edit_delete.css';

function CreateStudent(props) {
  const { token, removeToken, setToken } = useToken();

  const [usersData, setUsersData] = useState(null);

  function redirectToPage() {
    window.location.href = '/user_listing';
  }

  useEffect(() => {
    async function getAuthUser() {
      const response = await axios({
        method: "GET",
        url: "http://127.0.0.1:5000/get_auth_user",
        headers: {
          Authorization: `Bearer ${props.token}`
        }
      });
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
    const response = await axios.post(`http://127.0.0.1:5000/student`, usersData, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    });
    redirectToPage();
  };

  const handleCancel = () => {
    setUsersData(null);
  };


  return (
    <div className="container">
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="username">Username:</label>
          <input type="text" id="username" name="username" value={usersData?.username || ''} onChange={handleInputChange} data-testid="username" />
        </div>

        <div className="form-group">
          <label htmlFor="firstName">First Name:</label>
          <input type="text" id="firstName" name="firstName" value={usersData?.firstName || ''} onChange={handleInputChange} data-testid="firstName" />
        </div>

        <div className="form-group">
          <label htmlFor="lastName">Last Name:</label>
          <input type="text" id="lastName" name="lastName" value={usersData?.lastName || ''} onChange={handleInputChange} data-testid="lastName" />
        </div>

        <div className="form-group">
          <label htmlFor="email">Email:</label>
          <input type="text" id="email" name="email" value={usersData?.email || ''} onChange={handleInputChange} data-testid="email" />
        </div>

        <div className="form-group">
          <label htmlFor="phone">Phone:</label>
          <input type="text" id="phone" name="phone" value={usersData?.phone || ''} onChange={handleInputChange} data-testid="phone" />
        </div>

        <div className="form-group">
          <label htmlFor="password">Password:</label>
          <input type="text" id="password" name="password" value={usersData?.password || ''} onChange={handleInputChange} data-testid="password" />
        </div>

        <div className="form-buttons">
          <button type="submit" className="btn btn-primary">Save Changes</button>
          <button type="button" className="btn btn-secondary" onClick={handleCancel}>Cancel</button>
        </div>
      </form>

      <hr />

    </div>
  );
}

export default CreateStudent;
