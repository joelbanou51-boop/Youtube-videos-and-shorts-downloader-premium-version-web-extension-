const https = require('https');
const fs = require('fs');

https.get('https://www.youtube.com/watch?v=aqz-KE-bpKQ', (res) => {
  let data = '';
  res.on('data', chunk => data += chunk);
  res.on('end', () => {
    const match = data.match(/ytInitialPlayerResponse\s*=\s*({.+?});/);
    if (match) {
      const obj = JSON.parse(match[1]);
      fs.writeFileSync('yt_formats.json', JSON.stringify(obj.streamingData, null, 2));
      console.log('Saved to yt_formats.json');
    } else {
      console.log('No ytInitialPlayerResponse found');
    }
  });
}).on('error', console.error);
