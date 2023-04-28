import { BrowserRouter, Route, Routes } from 'react-router-dom'
import Login from './Login'
import UserListing from './UserListing'
import Header from './Header'

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
              </Routes>
          </>
        )}
      </div>
    </BrowserRouter>
  );
}

export default App;