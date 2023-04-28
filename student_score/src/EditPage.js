// import { useState } from 'react';
// import axios from "axios";
// import './static/css/login_page.css';


function EditPage(props) {


    return (
      <div>
        <h1>Login</h1>
          <form className="login" onSubmit={logMeIn}>
            <input onChange={handleChange} 
                  type="username"
                  value={loginForm.username} 
                  name="username" 
                  placeholder="Username" 
                  />
            <input onChange={handleChange} 
                  type="password"
                  value={loginForm.password} 
                  name="password" 
                  placeholder="Password" 
                  />

          <button type="submit" className="btn btn-primary">Submit</button>
        </form>
      </div>
    );
}

export default Login;
