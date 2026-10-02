export class LeadWebSocket {
  private socket: WebSocket | null = null;

  connect() {
    this.socket = new WebSocket(
      'wss://meta-lead-testing.onrender.com/ws?token=my-super-secret-key'
    );

    this.socket.onopen = () => {
      console.log('WebSocket connected');
    };

    this.socket.onmessage = (event) => {
      console.log('Message received:', event.data);
    };

    this.socket.onerror = (error) => {
      console.log('WebSocket error:', error);
    };

    this.socket.onclose = () => {
      console.log('WebSocket disconnected');
      this.socket = null;
    };
  }

  disconnect() {
    this.socket?.close();
    this.socket = null;
  }
}