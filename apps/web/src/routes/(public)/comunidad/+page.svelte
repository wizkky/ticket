<script lang="ts">
	import { resolve } from '$app/paths';
	import { ArrowUpRight, MapPin, Sparkles } from '@lucide/svelte';
	import CommunityPreview from '$lib/components/caudal/CommunityPreview.svelte';
	import * as m from '$lib/paraglide/messages.js';
	import type { PageData } from './$types';
	const { data }: { data: PageData } = $props();
</script>

<svelte:head
	><title>{m['creative.community']()} · Caudal Creativo</title><meta
		name="description"
		content={m['creative.communityCopy']()}
	/><meta name="robots" content="noindex,nofollow" /></svelte:head
>
<section class="creative-section community-hero" aria-labelledby="community-title">
	<p class="creative-eyebrow">Caudal Creativo / {m['creative.community']()}</p>
	<h1 class="creative-title" id="community-title">{m['creative.communityTitle']()}</h1>
	<p class="creative-intro">{m['creative.communityCopy']()}</p>
	<a class="creative-pill" href={resolve('/(public)/organizations', {})}
		>{m['creative.directory']()}<ArrowUpRight size={20} aria-hidden="true" /></a
	>
</section>
<div class="profile-principle creative-section">
	<h2>{m['creative.profileStructure']()}</h2>
	<p>{m['creative.profileStructureCopy']()}</p>
</div>
<CommunityPreview organizations={data.organizations} unavailable={data.communityUnavailable} />
<div class="directory-access creative-section">
	<p class="creative-intro">{m['creative.organizationsCopy']()}</p>
	<a class="creative-link" href={resolve('/(public)/organizations', {})}
		>{m['creative.directory']()}<ArrowUpRight size={18} aria-hidden="true" /></a
	>
</div>
<section class="creative-section" aria-labelledby="spaces-title">
	<div class="creative-heading">
		<div>
			<p class="creative-eyebrow">{m['creative.community']()}</p>
			<h2 id="spaces-title">{m['creative.spacesTitle']()}</h2>
		</div>
		<p>{m['creative.spacesCopy']()}</p>
	</div>
	{#if data.spacesUnavailable}<p class="creative-empty" role="status">
			{m['workspace.dataUnavailable']()}
		</p>
	{:else if data.venueEvents.length}
		<div class="spaces-grid">
			{#each data.venueEvents as event (event.venue?.id)}
				<article>
					<MapPin size={30} strokeWidth={1} aria-hidden="true" />
					<h3>{event.venue?.name}</h3>
					<p>{event.venue?.city?.name}</p>
					<a
						class="creative-link"
						href={resolve('/(public)/events/[org_slug]/[event_slug]', {
							org_slug: event.organization.slug,
							event_slug: event.slug
						})}>{m['caudal.viewEvent']()}<ArrowUpRight size={17} aria-hidden="true" /></a
					>
				</article>
			{/each}
		</div>
	{:else}<p class="creative-empty">{m['creative.spacesEmpty']()}</p>{/if}
</section>
<section class="creative-section people" aria-labelledby="people-title">
	<div class="creative-heading">
		<div>
			<p class="creative-eyebrow">{m['creative.development']()}</p>
			<h2 id="people-title">{m['creative.peopleTitle']()}</h2>
		</div>
		<Sparkles size={40} strokeWidth={0.8} aria-hidden="true" />
	</div>
	<p class="creative-intro">{m['creative.peopleCopy']()}</p>
	<span class="creative-status pending">{m['creative.development']()}</span>
</section>

<style>
	.community-hero {
		border-bottom: 1px solid hsl(var(--border));
	}
	.profile-principle {
		display: grid;
		grid-template-columns: 1fr 1fr;
		gap: 60px;
		padding-bottom: 0;
	}
	.profile-principle h2 {
		font-size: clamp(27px, 3vw, 42px);
		font-weight: 400;
		letter-spacing: -0.04em;
		line-height: 1.2;
	}
	.profile-principle p {
		font-size: 14px;
		line-height: 1.8;
		color: hsl(var(--muted-foreground));
	}
	.directory-access {
		padding-top: 0;
		padding-bottom: 0;
	}
	.directory-access p {
		margin-top: 0;
	}
	.spaces-grid {
		display: grid;
		grid-template-columns: repeat(3, minmax(0, 1fr));
		gap: 30px;
	}
	.spaces-grid article {
		padding: 26px;
		border: 1px solid hsl(var(--border));
	}
	h3 {
		font-size: 25px;
		font-weight: 400;
		letter-spacing: -0.04em;
		margin-block: 25px 12px;
	}
	article > p {
		font-size: 13px;
		color: hsl(var(--muted-foreground));
	}
	article > a {
		margin-top: 20px;
	}
	.people {
		border-top: 1px solid hsl(var(--border));
		background: hsl(var(--card));
	}
	@media (max-width: 767px) {
		.profile-principle {
			grid-template-columns: 1fr;
			gap: 20px;
		}
		.spaces-grid {
			grid-template-columns: 1fr;
		}
	}
</style>
