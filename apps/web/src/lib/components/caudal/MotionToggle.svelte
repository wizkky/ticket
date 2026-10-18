<script lang="ts">
	import { onMount } from 'svelte';
	import { Pause, Play } from '@lucide/svelte';
	import * as m from '$lib/paraglide/messages.js';
	let paused = $state(false);
	let reduced = $state(false);
	onMount(() => {
		const media = matchMedia('(prefers-reduced-motion: reduce)');
		const sync = () => {
			reduced = media.matches;
			paused = document.documentElement.dataset.caudalMotion === 'paused';
		};
		sync();
		media.addEventListener('change', sync);
		window.addEventListener('caudal-motion-change', sync);
		window.addEventListener('storage', sync);
		return () => {
			media.removeEventListener('change', sync);
			window.removeEventListener('caudal-motion-change', sync);
			window.removeEventListener('storage', sync);
		};
	});
	function toggle() {
		paused = !paused;
		document.documentElement.dataset.caudalMotion = paused ? 'paused' : 'playing';
		try {
			localStorage.setItem('caudal-motion', paused ? 'paused' : 'playing');
		} catch {
			/* optional preference */
		}
		window.dispatchEvent(new Event('caudal-motion-change'));
		if (paused) window.dispatchEvent(new Event('caudal-motion-paused'));
	}
</script>

<button
	type="button"
	onclick={toggle}
	disabled={reduced}
	aria-pressed={paused}
	class="inline-flex min-h-11 items-center gap-2 rounded-full px-3 text-xs text-muted-foreground hover:text-foreground focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-4"
>
	{#if paused || reduced}<Play size={12} aria-hidden="true" />{:else}<Pause
			size={12}
			aria-hidden="true"
		/>{/if}
	{reduced ? m['caudal.reducedMotion']() : paused ? m['caudal.play']() : m['caudal.pause']()}
</button>
