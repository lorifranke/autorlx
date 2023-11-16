import {sveltekit} from '@sveltejs/kit/vite';
import type {UserConfig} from 'vite';

const config: UserConfig = {
    plugins: [sveltekit()],
    preview: {
        // same as npm run dev...  for SSO to work
        port: 5173
    }
};

export default config;
