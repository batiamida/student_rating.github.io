import { useState } from 'react';
import axios from 'axios';
import './static/css/login_page.css';

function Login(props) {
  const [loginForm, setLoginForm] = useState({
    username: '',
    password: '',
  });

  const logMeIn = (event) => {
    event.preventDefault();

    axios
      .post('http://127.0.0.1:5000/token', {
        username: loginForm.username,
        password: loginForm.password,
      })
      .then((response) => {
        props.setToken(response.data.access_token);
      })
      .catch((error) => {
        if (error.response) {
          console.log(error.response);
          console.log(error.response.status);
          console.log(error.response.headers);
        }
      });

    setLoginForm({ username: '', password: '' });
  };

  const handleChange = (event) => {
    const { value, name } = event.target;
    setLoginForm((prevLoginForm) => ({
      ...prevLoginForm,
      [name]: value,
    }));
  };

  return (
    <div>
      <h1>Login</h1>
      <form className="login" onSubmit={logMeIn}>
        <input
          onChange={handleChange}
          type="username"
          value={loginForm.username}
          name="username"
          placeholder="Username"
        />
        <input
          onChange={handleChange}
          type="password"
          value={loginForm.password}
          name="password"
          placeholder="Password"
        />

        <button type="submit" className="btn btn-primary">
          Submit
        </button>
      </form>
    </div>
  );
}

export default Login;
