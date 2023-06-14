import { useState, useEffect } from 'react';
import axios from 'axios';
import './static/css/listing_page.css';
import { Link } from 'react-router-dom';

function UserListing(props) {
  const [usersData, setUsersData] = useState(null);
  const [userList, setUserList] = useState([]);

  useEffect(() => {
    async function getAuthUser() {
      const response = await axios({
        method: 'GET',
        url: 'http://127.0.0.1:5000/get_auth_user',
        headers: {
          Authorization: `Bearer ${props.token}`,
        },
      });

      setUsersData(response.data.user);
    }

    getAuthUser();
  }, []);

  useEffect(() => {
    if (usersData) {
      axios({
        method: 'GET',
        url: 'http://127.0.0.1:5000/user_listing',
      })
        .then((response) => {
          const res = response.data;
          const updatedUserList = res.map((item) => ({
            ...item,
            isCurrentUser: item.name === usersData.username,
          }));
          setUserList(updatedUserList);
        })
        .catch((error) => {
          console.error(error);
        });
    }
  }, [usersData]);
  const handleEditScores = (id) => {
    window.location.href = `/edit_scores/${id}`;
  };
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
                {usersData.model === 'Teacher' && (
                  <div className="actions">

                    <button className="edit-button" onClick={() => handleEditScores(user.id)}>Edit scores</button>
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      </main>
      <footer>
        <div className="footer-content">
          <p>Students Rating</p>
          <p>&copy; 2023 Students Rating. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
}

export default UserListing;
