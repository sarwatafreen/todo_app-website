const express = require('express');
const path = require('path');
const fs = require('fs');

const app = express();
const PORT = 3000;

// Serve static files from public directory
app.use(express.static(path.join(__dirname, 'public')));

// For Next.js apps, we need to handle dynamic routes
// If file doesn't exist, serve index.html (for client-side routing)
app.get('*', (req, res) => {
  const filePath = path.join(__dirname, 'public', req.path);

  // Check if file exists
  fs.access(filePath, fs.constants.F_OK, (err) => {
    if (err) {
      // File doesn't exist, serve index.html for client-side routing
      res.sendFile(path.join(__dirname, 'public', 'index.html'));
    } else {
      // File exists, serve it
      res.sendFile(filePath);
    }
  });
});

app.listen(PORT, '0.0.0.0', () => {
  console.log(`Server is running on http://localhost:${PORT}`);
  console.log(`Network access: http://0.0.0.0:${PORT}`);
});