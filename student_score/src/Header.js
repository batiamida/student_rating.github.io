import axios from "axios";
import { useEffect, useState } from "react";


function Header(props) {
  const [usersData, setUsersData] = useState(null);

  useEffect(() => {
    async function getAuthUser() {
      try {
    const response = await axios({
      method: "GET",
      url: "http://127.0.0.1:5000/get_auth_user",
      headers: {
        Authorization: `Bearer ${props.token}`,
      },
    });

    if (response.data && response.data.user) {
      setUsersData(response.data.user);
    }
  } catch (error) {
    console.log("Error fetching user data:", error);
  }
    }

    getAuthUser();
    // console.log(usersData);
  }, [props.token]);

  function logMeOut() {
    axios({
      method: "POST",
      url: "http://127.0.0.1:5000/logout",
    })
      .then((response) => {
        props.token();
        // props.removeToken();
        // props.logOut();
        // props.removeToken();
        // props.token();
      })
      .catch((error) => {
        if (error.response) {
          console.log(error.response);
          console.log(error.response.status);
          console.log(error.response.headers);
        }
      });
  }

  return (
    <header>
      <nav>
        <h1>Students Rating</h1>
        <ul>
          <li><a href="/">Home</a></li>
          <li><a href="/user_listing">Users</a></li>
          <li><a href="/edit_page">Edit</a></li>
          <li><a href="/create_student">Create student</a></li>
          <li><a href="/profile">Profile</a></li>
          <li><a href="/scores_table">Scores</a></li>
          {/*<li><a href="{{ url_for('contact_page') }}">Contact</a></li>*/}
          {props.token && (
            <li>
              <a onClick={logMeOut}>Logout</a>
            </li>
          )}
        </ul>
      </nav>
    </header>
  );
}

export default Header;
