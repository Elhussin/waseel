import React, { useState } from 'react';
import axios from 'axios';

const App = () => {
  const [clientId, setClientId] = useState('');
  const [token, setToken] = useState('');
  const [refreshToken, setRefreshToken] = useState('');
  const [userId, setUserId] = useState('');
  const [userData, setUserData] = useState(null);
  const [error, setError] = useState('');

  // دالة للحصول على TOKEN و REFRESH_TOKEN
  const fetchToken = async () => {
    try {
      const response = await axios.post('https://api.example.com/get_token', {
        client_id: clientId,
      });
      setToken(response.data.token);
      setRefreshToken(response.data.refresh_token);
      setError('');
    } catch (err) {
      setError('Failed to fetch token. Please check your Client ID.');
    }
  };

  // دالة للاستعلام عن بيانات المستخدم باستخدام TOKEN
  const fetchUserData = async () => {
    try {
      const response = await axios.get(`https://api.example.com/user/${userId}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setUserData(response.data);
      setError('');
    } catch (err) {
      setError('Failed to fetch user data. Please check your User ID or Token.');
    }
  };

  return (
    <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif' }}>
      <h1>React API Example</h1>

      {/* قسم الحصول على TOKEN */}
      <div>
        <h2>Get Token</h2>
        <input
          type="text"
          placeholder="Enter Client ID"
          value={clientId}
          onChange={(e) => setClientId(e.target.value)}
          style={{ padding: '8px', marginRight: '10px' }}
        />
        <button onClick={fetchToken} style={{ padding: '8px 16px', cursor: 'pointer' }}>
          Fetch Token
        </button>
        {token && (
          <div>
            <p>Token: {token}</p>
            <p>Refresh Token: {refreshToken}</p>
          </div>
        )}
      </div>

      {/* قسم الاستعلام عن بيانات المستخدم */}
      <div style={{ marginTop: '20px' }}>
        <h2>Fetch User Data</h2>
        <input
          type="text"
          placeholder="Enter User ID"
          value={userId}
          onChange={(e) => setUserId(e.target.value)}
          style={{ padding: '8px', marginRight: '10px' }}
        />
        <button onClick={fetchUserData} style={{ padding: '8px 16px', cursor: 'pointer' }}>
          Fetch User Data
        </button>
        {userData && (
          <div>
            <h3>User Data:</h3>
            <pre>{JSON.stringify(userData, null, 2)}</pre>
          </div>
        )}
      </div>

      {/* عرض الأخطاء */}
      {error && <p style={{ color: 'red' }}>{error}</p>}
    </div>
  );
};

export default App;