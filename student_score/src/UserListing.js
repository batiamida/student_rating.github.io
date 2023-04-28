import { useState, useEffect } from 'react';
import axios from "axios";
import './static/css/listing_page.css';
import { Link } from 'react-router-dom';


function UserListing(props) {

  const [usersData, setUsersData] = useState(null);
  const [userList, setUserList] = useState([]);

  async function getAuthUser() {
    const response = await axios({
      method: "GET",
      url:"http://127.0.0.1:5000/get_auth_user",
      headers: {
        Authorization: `Bearer ${props.token}`
      }
    });
    setUsersData(response.data.logged_in_as);
  }

  useEffect(() => {
    getAuthUser();
    axios({
      method: "GET",
      url: "http://127.0.0.1:5000/user_listing",
    })
      .then((response) => {
        const res = response.data;
        console.log(res);
        const updatedUserList = res.map((item) => ({
          ...item,
          isCurrentUser: item.name === usersData,
        }));
        setUserList(updatedUserList);
      })
      .catch((error) => {
        console.error(error);
      });
  }, [usersData]);

  return (
    <div>
      <main>
        <div className="users-list">
        {userList.map((user) => (
          <div className="user" key={user.id}>
            <div className="user-details">
              <h2>
                {user.firstName} {user.lastName}
              </h2>
              <p>{user.email}</p>
              {user.isCurrentUser && 
                <div className="actions">
                  <button className="edit-button">Edit</button>

                  <button className="delete-button">Delete</button>
                </div>
              }
            </div>
          </div>
        ))}
        </div>
      </main>
      <footer>
        <div className="footer-content">
          <p> Students Rating </p>
          <p>&copy; 2023 Students Rating. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
}

export default UserListing;
