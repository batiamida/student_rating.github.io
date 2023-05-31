import { BrowserRouter, Route, Routes } from 'react-router-dom'
import Login from './Login'
import EditPage from "./EditPage";
import CreateStudent from "./CreateStudent";
import UserListing from './UserListing'
import Header from './Header'
import Profile from "./Profile";
import MainPage from "./MainPage"

import useToken from './useToken'
import './App.css'

function App() {
  const { token, removeToken, setToken } = useToken();

  return (
    <BrowserRouter>
      <div className="App">
        <Header token={removeToken}/>
        {!token && token!=="" &&token!== undefined?  
        <Login setToken={setToken} />
        :(
          <>
            <Routes>
              <Route exact path="/user_listing" element={<UserListing token={token} setToken={setToken}/>}></Route>
              <Route exact path="/edit_page" element={<EditPage token={token} setToken={setToken}/>}></Route>
              <Route exact path="/create_student" element={<CreateStudent token={token} setToken={setToken}/>}></Route>
              <Route exact path="/profile" element={<Profile token={token} setToken={setToken}/>}></Route>
              <Route exact path="/home" element={<MainPage token={token} setToken={setToken}/>}></Route>
              </Routes>
          </>
        )}
      </div>
    </BrowserRouter>
  );
}

export default App;