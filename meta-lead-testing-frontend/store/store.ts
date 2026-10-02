import { create } from 'zustand';

export type Lead = {
  name: string;
  phone: string;
  email: string;
};

type Store = {
  leads: Lead[];
  addLead: (lead: Lead) => void;
  clearLeads: () => void;
};

export const useStore = create<Store>((set) => ({
  leads: [],

  addLead: (lead) =>
    set((state) => ({
      leads: [...state.leads, lead],
    })),

  clearLeads: () =>
    set({
      leads: [],
    }),
}));