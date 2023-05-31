import React, {useEffect, useState} from 'react'
import axios from "axios";

function Profile(props) {

  const [profileData, setProfileData] = useState(null)
 useEffect(() => {
    async function getAuthUser() {
      const response = await axios({
        method: "GET",
        url:"http://127.0.0.1:5000/get_auth_user",
        headers: {
          Authorization: `Bearer ${props.token}`
        }
      });
      setProfileData(response.data.user);
    }
    getAuthUser();
  }, [props.token]);
  const handleDelete = async () => {
      const model = profileData.model.toLowerCase();
      // console.log(model);

      const response = await axios.delete(`http://127.0.0.1:5000/${model}`, {
        headers: {
          Authorization: `Bearer ${props.token}`,
        },
      })
      window.location.href = '/user_listing';

};

  return (
    <div className="Profile">
        {/*<p>To get your profile details: </p><button onClick={}>Click me</button>*/}
        {profileData && <div>
              <p>Username: {profileData.username}</p>
              <p>First name: {profileData.firstName}</p>
              <p>Last name: {profileData.lastName}</p>
            </div>
        }
        <div className="form-buttons">
            <button type="button" className="btn btn-secondary" onClick={handleDelete}>Delete</button>
        </div>
    </div>

      // handleDelete
  );
}

export default Profile;
