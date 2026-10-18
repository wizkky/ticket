<script lang="ts">
	import { resolve } from '$app/paths';
	import { ArrowUpRight, ShieldCheck, Users } from '@lucide/svelte';
	import PageHeader from '$lib/components/common/PageHeader.svelte';
	import Metrics from '$lib/components/workspace/Metrics.svelte';
	import * as m from '$lib/paraglide/messages.js';
	import type { PageData } from './$types';
	const { data }: { data: PageData } = $props();
	const labels = $derived({
		organizations: m['workspace.organizations'](),
		events: m['workspace.events'](),
		users: m['workspace.users'](),
		tickets: m['workspace.adminTickets']()
	});
</script>

<svelte:head
	><title>{m['workspace.administration']()} · CaudalTickets</title><meta
		name="robots"
		content="noindex,nofollow"
	/></svelte:head
>
<div class="caudal-workspace container py-12 sm:py-20">
	<p class="mb-7 flex items-center gap-2 text-xs text-muted-foreground">
		<ShieldCheck size={15} />{m['workspace.protected']()}
	</p>
	<PageHeader
		volume="poster"
		title={m['workspace.administration']()}
		subtitle={m['workspace.adminIntro']()}
	/>
	<div class="mt-9 flex items-center gap-3 text-sm">
		<Users size={18} strokeWidth={1} />{m['workspace.producersCount']({
			count: data.overview.producer_count
		})}
	</div>
	<Metrics metrics={data.overview.metrics} />
	<section class="mt-14" aria-labelledby="management-title">
		<h2 id="management-title" class="text-xl font-medium">{m['workspace.adminTools']()}</h2>
		<div class="management-grid">
			{#each data.tools as tool (tool.key)}
				<!-- eslint-disable-next-line svelte/no-navigation-without-resolve -- trusted server-built backend admin URL -->
				<a href={tool.href} class="management-card caudal-motion"
					><span>{labels[tool.key as keyof typeof labels]}</span><strong>{tool.count}</strong><span
						class="management-action">{m['workspace.adminOpen']()}<ArrowUpRight size={18} /></span
					></a
				>
			{/each}
		</div>
		<p class="mt-5 max-w-3xl text-xs leading-relaxed text-muted-foreground">
			{m['workspace.adminAuthNote']()}
		</p>
	</section>
	<section class="mt-14">
		<h2 class="mb-6 text-xl font-medium">{m['workspace.organizations']()}</h2>
		<div class="organization-list">
			{#each data.overview.organizations as org (org.id)}<a
					href={resolve('/(public)/org/[slug]', { slug: org.slug })}
					><span>{org.name}</span><ArrowUpRight size={18} /></a
				>{:else}<p class="py-8 text-muted-foreground">{m['workspace.noEvents']()}</p>{/each}
		</div>
	</section>
	<p class="mt-10 border-t pt-5 text-xs leading-relaxed text-muted-foreground">
		{m['workspace.paymentScope']()}
	</p>
</div>

<style>
	.management-grid {
		display: grid;
		grid-template-columns: repeat(4, minmax(0, 1fr));
		gap: 20px;
		margin-top: 25px;
	}
	.management-card {
		display: flex;
		flex-direction: column;
		padding: 24px;
		border: 1px solid hsl(var(--border));
		transition: background 0.2s;
	}
	.management-card:hover {
		background: hsl(var(--card));
	}
	.management-card > span:first-child {
		font-size: 13px;
	}
	strong {
		font-family: 'Manrope', sans-serif;
		font-size: 55px;
		font-weight: 400;
		letter-spacing: -0.06em;
		margin-block: 25px;
	}
	.management-action {
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: 12px;
		font-size: 11px;
		border-top: 1px solid hsl(var(--border));
		padding-top: 18px;
	}
	.organization-list > a {
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: 25px;
		border-top: 1px solid hsl(var(--border));
		padding-block: 23px;
		font-size: 17px;
	}
	.organization-list > a:last-child {
		border-bottom: 1px solid hsl(var(--border));
	}
	@media (max-width: 1023px) {
		.management-grid {
			grid-template-columns: 1fr 1fr;
		}
	}
	@media (max-width: 420px) {
		.management-card {
			padding: 17px;
		}
		.management-action {
			font-size: 10px;
		}
		strong {
			font-size: 42px;
		}
	}
	@media (prefers-reduced-motion: reduce) {
		.management-card {
			transition: none;
		}
	}
</style>
