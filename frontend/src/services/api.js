export async function sendChatMessage(message) {
  const response = await fetch('/api/ping', {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'Message': message
    },
    // body: JSON.stringify({ message }),
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ error: 'Unknown error' }));
    throw new Error(error.error || 'Failed to send message');
  }

  return response;
}

export async function checkHealth() {
  const response = await fetch('/api/health');
  return response.json();
}
