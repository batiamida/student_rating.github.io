import logo from './logo.svg'
import axios from "axios";

function Header(props) {

  function logMeOut() {
    axios({
      method: "POST",
      url:"http://127.0.0.1:5000/logout",
    })
    .then((response) => {
       props.token()
    }).catch((error) => {
      if (error.response) {
        console.log(error.response)
        console.log(error.response.status)
        console.log(error.response.headers)
        }
    })}

    return(
    <header>
      <nav>
        <h1>Students Rating</h1>
        <ul>
          <li><a href="/home">Home</a></li>
          <li><a href="/user_listing">Users</a></li>
          <li><a href="#">Pricing</a></li>
          <li><a href="{{ url_for('contact_page') }}">Contact</a></li>
          <li><a onClick={logMeOut}> 
                Logout
            </a></li>
        </ul>
      </nav>
    </header>
    )
}

export default Header;
