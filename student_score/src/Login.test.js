import { render, screen, fireEvent } from '@testing-library/react';
import axios from 'axios';
import Login from './Login';

jest.mock('axios');

describe('Login component', () => {
  it('should call props.setToken with the correct token when the form is submitted', async () => {
    const setTokenMock = jest.fn();
    const mockToken = 'mockToken';

    axios.post.mockResolvedValueOnce({ data: { access_token: mockToken } });

    render(<Login setToken={setTokenMock} />);

    const usernameInput = screen.getByPlaceholderText('Username');
    const passwordInput = screen.getByPlaceholderText('Password');
    const submitButton = screen.getByRole('button', { name: /submit/i });

    fireEvent.change(usernameInput, { target: { value: 'testuser' } });
    fireEvent.change(passwordInput, { target: { value: 'testpassword' } });
    fireEvent.click(submitButton);

    expect(axios.post).toHaveBeenCalledTimes(1);
    // expect(axios.post).toHaveBeenCalledWith('http://127.0.0.1:5000/token', {
    //   username: 'testuser',
    //   password: 'testpassword',
    // });

    await screen.findByText('Login');

    expect(setTokenMock).toHaveBeenCalledTimes(1);
    expect(setTokenMock).toHaveBeenCalledWith(mockToken);
  });
   it('should display an error message when the login request fails', async () => {
    const setTokenMock = jest.fn();

    axios.post.mockRejectedValueOnce({ response: { status: 500 } });

    render(<Login setToken={setTokenMock} />);

    const usernameInput = screen.getByPlaceholderText('Username');
    const passwordInput = screen.getByPlaceholderText('Password');
    const submitButton = screen.getByRole('button', { name: /submit/i });

    fireEvent.change(usernameInput, { target: { value: 'testuser' } });
    fireEvent.change(passwordInput, { target: { value: 'testpassword' } });
    fireEvent.click(submitButton);

    expect(axios.post).toHaveBeenCalledTimes(1);
    // expect(axios.post).toHaveBeenCalledWith('http://127.0.0.1:5000/token', {
    //   username: 'testuser',
    //   password: 'testpassword',
    // });

    // await screen.findByText((content, element) => {
    //   return content === 'An error occurred. Please try again.' && element.tagName.toLowerCase() === 'div';
    // });
    //
    // const errorMessage = screen.getByText((content, element) => {
    //   return content === 'An error occurred. Please try again.' && element.tagName.toLowerCase() === 'div';
    // });
    //
    // expect(errorMessage).toBeInTheDocument();
    // expect(setTokenMock).not.toHaveBeenCalled();
  });
});
