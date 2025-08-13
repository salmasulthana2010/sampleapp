<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>User Fetcher</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        
        .container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1);
            padding: 40px;
            max-width: 600px;
            width: 100%;
            transform: translateY(0);
            transition: transform 0.3s ease;
        }
        
        .container:hover {
            transform: translateY(-5px);
        }
        
        h1 {
            text-align: center;
            color: #333;
            margin-bottom: 30px;
            font-size: 2.5em;
            font-weight: 700;
            background: linear-gradient(135deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .input-group {
            margin-bottom: 25px;
        }
        
        label {
            display: block;
            margin-bottom: 8px;
            color: #555;
            font-weight: 600;
            font-size: 1.1em;
        }
        
        input[type="text"] {
            width: 100%;
            padding: 15px 20px;
            border: 2px solid #e1e8ed;
            border-radius: 12px;
            font-size: 16px;
            transition: all 0.3s ease;
            background: #f8fafc;
        }
        
        input[type="text"]:focus {
            outline: none;
            border-color: #667eea;
            background: white;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }
        
        button {
            width: 100%;
            padding: 15px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            border: none;
            border-radius: 12px;
            font-size: 18px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            transform: translateY(0);
        }
        
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(102, 126, 234, 0.3);
        }
        
        button:active {
            transform: translateY(0);
        }
        
        button:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }
        
        .loading {
            display: none;
            text-align: center;
            margin: 20px 0;
            color: #667eea;
            font-weight: 600;
        }
        
        .spinner {
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 2px solid #f3f3f3;
            border-top: 2px solid #667eea;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin-right: 10px;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .result {
            margin-top: 30px;
            padding: 20px;
            border-radius: 12px;
            display: none;
            animation: fadeIn 0.5s ease;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .success {
            background: linear-gradient(135deg, #56f39a, #1dd1a1);
            color: white;
        }
        
        .error {
            background: linear-gradient(135deg, #ff6b6b, #ee5a24);
            color: white;
        }
        
        .user-list {
            list-style: none;
            margin: 15px 0 0 0;
        }
        
        .user-list li {
            padding: 10px 15px;
            background: rgba(255, 255, 255, 0.2);
            margin: 8px 0;
            border-radius: 8px;
            font-weight: 500;
            border-left: 4px solid rgba(255, 255, 255, 0.5);
        }
        
        .health-status {
            margin-top: 10px;
            padding: 10px 15px;
            background: rgba(255, 255, 255, 0.2);
            border-radius: 8px;
            font-weight: 500;
        }
        
        .example {
            font-size: 0.9em;
            color: #666;
            font-style: italic;
            margin-top: 5px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 User Fetcher</h1>
        
        <div class="input-group">
            <label for="apiUrl">API URL (Load Balancer or Public IP):</label>
            <input type="text" id="apiUrl" placeholder="http://your-load-balancer-url" />
            <div class="example">Example: http://lb-123456789.us-east-1.elb.amazonaws.com or http://3.14.159.26:5000</div>
        </div>
        
        <button onclick="fetchUsers()" id="fetchBtn">
            Fetch Users
        </button>
        
        <div class="loading" id="loading">
            <div class="spinner"></div>
            Loading users...
        </div>
        
        <div class="result" id="result"></div>
    </div>

    <script>
        async function fetchUsers() {
            const apiUrl = document.getElementById('apiUrl').value.trim();
            const fetchBtn = document.getElementById('fetchBtn');
            const loading = document.getElementById('loading');
            const result = document.getElementById('result');
            
            // Clear previous results
            result.style.display = 'none';
            
            // Validate URL
            if (!apiUrl) {
                showError('Please enter an API URL');
                return;
            }
            
            // Add http:// if not present
            let fullUrl = apiUrl;
            if (!fullUrl.startsWith('http://') && !fullUrl.startsWith('https://')) {
                fullUrl = 'http://' + fullUrl;
            }
            
            // Remove trailing slash if present
            fullUrl = fullUrl.replace(/\/$/, '');
            
            // Show loading state
            fetchBtn.disabled = true;
            loading.style.display = 'block';
            
            try {
                // First check health endpoint
                const healthResponse = await fetch(`${fullUrl}/health`, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                });
                
                const healthStatus = healthResponse.ok ? 'API is healthy ✅' : 'API health check failed ⚠️';
                
                // Fetch users
                const usersResponse = await fetch(`${fullUrl}/api/users`, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                });
                
                if (!usersResponse.ok) {
                    throw new Error(`HTTP ${usersResponse.status}: ${usersResponse.statusText}`);
                }
                
                const data = await usersResponse.json();
                
                if (data.users && Array.isArray(data.users)) {
                    showSuccess(data.users, healthStatus);
                } else {
                    throw new Error('Invalid response format - expected users array');
                }
                
            } catch (error) {
                console.error('Error fetching users:', error);
                showError(`Failed to fetch users: ${error.message}`);
            } finally {
                // Hide loading state
                fetchBtn.disabled = false;
                loading.style.display = 'none';
            }
        }
        
        function showSuccess(users, healthStatus) {
            const result = document.getElementById('result');
            result.className = 'result success';
            result.innerHTML = `
                <h3>✅ Success!</h3>
                <div class="health-status">${healthStatus}</div>
                <p><strong>Found ${users.length} users:</strong></p>
                <ul class="user-list">
                    ${users.map(user => `<li>👤 ${user}</li>`).join('')}
                </ul>
            `;
            result.style.display = 'block';
        }
        
        function showError(message) {
            const result = document.getElementById('result');
            result.className = 'result error';
            result.innerHTML = `
                <h3>❌ Error</h3>
                <p>${message}</p>
                <p><small>Make sure your API is running and the URL is correct. Check for CORS issues if running from a different domain.</small></p>
            `;
            result.style.display = 'block';
        }
        
        // Allow Enter key to submit
        document.getElementById('apiUrl').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                fetchUsers();
            }
        });
    </script>
</body>
</html>
