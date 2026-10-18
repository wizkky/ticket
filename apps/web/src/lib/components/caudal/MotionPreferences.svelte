<script lang="ts">
	import { onMount } from 'svelte';
	onMount(() => {
		const sync = () => {
			try {
				document.documentElement.dataset.caudalMotion =
					localStorage.getItem('caudal-motion') === 'paused' ? 'paused' : 'playing';
			} catch {
				/* optional local preference */
			}
		};
		sync();
		window.addEventListener('storage', sync);
		window.addEventListener('caudal-motion-change', sync);
		return () => {
			window.removeEventListener('storage', sync);
			window.removeEventListener('caudal-motion-change', sync);
		};
	});
</script>
