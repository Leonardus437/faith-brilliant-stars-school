// Client-side error handling
export function handleError({ error, event }) {
  console.error('Client error:', error);
  
  // Don't log browser extension errors
  if (error.message?.includes('extension') || 
      error.message?.includes('injected') ||
      error.stack?.includes('extension')) {
    return;
  }
  
  return {
    message: 'Something went wrong'
  };
}