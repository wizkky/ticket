<script lang="ts">
	import Family from '$lib/components/caudal/Family.svelte';
	import Services from '$lib/components/caudal/Services.svelte';
	import * as m from '$lib/paraglide/messages.js';
</script>

<svelte:head
	><title>{m['creative.ecosystem']()} · Caudal Creativo</title><meta
		name="description"
		content={m['creative.ecosystemCopy']()}
	/><meta name="robots" content="noindex,nofollow" /></svelte:head
>
<section class="creative-section" aria-labelledby="ecosystem-page-title">
	<p class="creative-eyebrow">Caudal Creativo / {m['creative.ecosystem']()}</p>
	<h1 id="ecosystem-page-title" class="creative-title">{m['caudal.familyTitle']()}</h1>
	<p class="creative-intro">{m['creative.servicesCopy']()}</p>
</section>
<Family />
<Services />
