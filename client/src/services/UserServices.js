import Client from './';

export const requestRegister = async (
  first_name,
  last_name,
  username,
  password
) => {
  const result = await Client.post('users/', {
    first_name,
    last_name,
    username,
    password,
    re_password: password
  });

  return result.data;
};

export const requestLogin = async (username, password) => {
  try {
    const result = await Client.post('token/login/', {
      username,
      password
    });

    const auth_token = result.data.auth_token;

    Client.defaults.headers.common['Authorization'] = 'Token ' + auth_token;
    localStorage.setItem('auth_token', auth_token);
    return true;
  } catch (error) {
    console.log(error);
    return false;
  }
};

export const requestUser = async () => {
  try {
    const result = await Client.get('users/me/');
    return result.data;
  } catch (error) {
    console.log(error);
    return null;
  }
};

export const requestLogout = async () => {
  const result = await Client.post('token/logout/');
  Client.defaults.headers.common['Authorization'] = '';
  localStorage.removeItem('auth_token');

  return result.data;
};

export const requestDeletion = async (password) => {
  const result = await Client.delete('users/me/', {
    data: {
      current_password: password
    }
  });
  return result;
};
