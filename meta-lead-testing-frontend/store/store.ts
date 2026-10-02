export type Lead = {
  name: string;
  phone: string;
  email: string;
};

export const store = {
  leads: [] as Lead[],
  socket: null as WebSocket | null,
};