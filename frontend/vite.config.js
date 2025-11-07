import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
	plugins: [sveltekit()],
	server: {
		port: 5174,
		host: true,
		proxy: {
			'/api': {
				target: 'http://localhost:8001',
				changeOrigin: true,
				secure: false
			}
		}
	},
	optimizeDeps: {
		exclude: ['@sveltejs/kit']
	}
});
