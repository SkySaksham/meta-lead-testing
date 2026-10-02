import { useStore } from '../store/store';

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
      const lead = JSON.parse(event.data);

      console.log('Lead received:', lead);

      useStore.getState().addLead(lead);
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