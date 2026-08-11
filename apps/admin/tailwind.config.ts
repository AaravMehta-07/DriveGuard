import type { Config } from 'tailwindcss';

const config: Config = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        dgPrimary: '#1E40AF',
        dgSecondary: '#0F172A',
        dgAccent: '#F59E0B',
        dgDanger: '#EF4444',
        dgSuccess: '#10B981',
      },
    },
  },
  plugins: [],
};

export default config;
