/**
 * Debug script to verify chatbot configuration
 * Run with: node debug-chatbot.js
 */

const fs = require('fs');
const path = require('path');

console.log('🔍 Chatbot Configuration Debug\n');

// Check .env.local
console.log('1. Checking .env.local file...');
const envPath = path.join(__dirname, '.env.local');
if (fs.existsSync(envPath)) {
  const envContent = fs.readFileSync(envPath, 'utf8');
  const mcpLine = envContent.split('\n').find(line => line.includes('NEXT_PUBLIC_MCP_SERVER_URL'));
  if (mcpLine) {
    console.log('   ✅ Found:', mcpLine);
  } else {
    console.log('   ❌ NEXT_PUBLIC_MCP_SERVER_URL not found in .env.local');
  }
} else {
  console.log('   ❌ .env.local file not found');
}

// Check chat.ts
console.log('\n2. Checking lib/api/chat.ts...');
const chatPath = path.join(__dirname, 'lib', 'api', 'chat.ts');
if (fs.existsSync(chatPath)) {
  const chatContent = fs.readFileSync(chatPath, 'utf8');
  const urlLine = chatContent.split('\n').find(line => line.includes('MCP_SERVER_URL'));
  if (urlLine) {
    console.log('   ✅ Found:', urlLine.trim());
  }
  
  // Check default port
  if (chatContent.includes('localhost:8000')) {
    console.log('   ✅ Default port is 8000');
  } else if (chatContent.includes('localhost:8001')) {
    console.log('   ⚠️  Default port is still 8001 - needs update');
  }
} else {
  console.log('   ❌ chat.ts file not found');
}

// Check ChatBot.tsx
console.log('\n3. Checking components/chatbot/ChatBot.tsx...');
const chatbotPath = path.join(__dirname, 'components', 'chatbot', 'ChatBot.tsx');
if (fs.existsSync(chatbotPath)) {
  const chatbotContent = fs.readFileSync(chatbotPath, 'utf8');
  
  if (chatbotContent.includes('localhost:8000')) {
    console.log('   ✅ Error message shows port 8000');
  } else if (chatbotContent.includes('localhost:8001')) {
    console.log('   ⚠️  Error message still shows port 8001 - needs update');
  }
} else {
  console.log('   ❌ ChatBot.tsx file not found');
}

console.log('\n4. Testing backend connection...');
const http = require('http');

const testUrl = 'http://localhost:8000';
http.get(testUrl, (res) => {
  console.log(`   ✅ Backend is running on port 8000 (Status: ${res.statusCode})`);
}).on('error', (err) => {
  console.log(`   ❌ Cannot connect to backend on port 8000`);
  console.log(`   Error: ${err.message}`);
});

console.log('\n📋 Summary:');
console.log('   - If all checks pass, restart frontend: npm run dev');
console.log('   - Clear browser cache (Ctrl+Shift+Delete)');
console.log('   - Open DevTools (F12) and check Console tab');
console.log('   - Try the chatbot again\n');
