<script lang="ts">
	import { resolve } from '$app/paths';
	import { ArrowUpRight, MapPin } from '@lucide/svelte';
	import type { OrganizationRetrieveSchema } from '$lib/api';
	import * as m from '$lib/paraglide/messages.js';
	interface Props {
		organizations: OrganizationRetrieveSchema[];
		unavailable?: boolean;
	}
	const { organizations, unavailable = false }: Props = $props();
</script>

<section class="creative-section" aria-labelledby="community-preview-title">
	<div class="creative-heading">
		<div>
			<p class="creative-eyebrow">{m['creative.community']()}</p>
			<h2 id="community-preview-title">{m['creative.organizationsTitle']()}</h2>
		</div>
		<a class="creative-link" href={resolve('/(public)/comunidad', {})}
			>{m['creative.community']()}<ArrowUpRight size={18} aria-hidden="true" /></a
		>
	</div>
	{#if unavailable}<p class="creative-empty" role="status">{m['workspace.dataUnavailable']()}</p>
	{:else if organizations.length}
		<div class="community-grid" class:two-profiles={organizations.length === 2}>
			{#each organizations as org (org.id)}
				<a class="profile" href={resolve('/(public)/org/[slug]', { slug: org.slug })}>
					<div class="profile-top">
						<span class="monogram" aria-hidden="true">{org.name.charAt(0)}</span><ArrowUpRight
							size={20}
							aria-hidden="true"
						/>
					</div>
					<h3>{org.name}</h3>
					{#if org.city}<p><MapPin size={13} aria-hidden="true" />{org.city.name}</p>{/if}
				</a>
			{/each}
		</div>
	{:else}<p class="creative-empty">{m['creative.emptyCommunity']()}</p>{/if}
</section>

<style>
	.community-grid {
		display: grid;
		grid-template-columns: repeat(3, minmax(0, 1fr));
		gap: 20px;
	}
	.community-grid.two-profiles {
		grid-template-columns: repeat(2, minmax(0, 1fr));
	}
	.profile {
		display: block;
		padding: 28px;
		border: 1px solid hsl(var(--border));
		background: hsl(var(--card));
		transition: transform 0.25s;
	}
	.profile:hover {
		transform: translateY(-4px);
	}
	.profile-top {
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: 12px;
	}
	.monogram {
		font-family: Georgia, serif;
		font-size: 40px;
		border: 1px solid hsl(var(--border));
		border-radius: 50%;
		width: 76px;
		height: 76px;
		display: grid;
		place-items: center;
	}
	h3 {
		font-size: 23px;
		font-weight: 400;
		letter-spacing: -0.035em;
		line-height: 1.3;
		margin-block: 28px 12px;
		overflow-wrap: anywhere;
	}
	.profile p {
		display: flex;
		align-items: center;
		gap: 8px;
		color: hsl(var(--muted-foreground));
		font-size: 12px;
	}
	@media (max-width: 767px) {
		.community-grid,
		.community-grid.two-profiles {
			grid-template-columns: 1fr;
		}
	}
	@media (prefers-reduced-motion: reduce) {
		.profile {
			transition: none;
		}
	}
</style>
