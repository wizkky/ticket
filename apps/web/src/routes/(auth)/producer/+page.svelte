<script lang="ts">
	import { resolve } from '$app/paths';
	import { ArrowUpRight, Plus, Waves } from '@lucide/svelte';
	import { Button } from '$lib/components/ui/button';
	import PageHeader from '$lib/components/common/PageHeader.svelte';
	import * as m from '$lib/paraglide/messages.js';
	import type { PageData } from './$types';
	const { data }: { data: PageData } = $props();
</script>

<svelte:head
	><title>{m['workspace.producerSpace']()} · Caudal Creativo</title><meta
		name="robots"
		content="noindex,nofollow"
	/></svelte:head
>
<div class="caudal-workspace container py-12 sm:py-20">
	<PageHeader
		volume="poster"
		kicker={m['workspace.workspaceKicker']()}
		title={m['workspace.producerSpace']()}
		subtitle={m['workspace.producerIntro']()}
	/>
	{#if data.workspace === null}<p role="alert" class="mt-12 rounded-lg border p-6">
			{m['workspace.dataUnavailable']()}
		</p>
	{:else if data.workspace.organizations.length}
		<div class="organization-grid">
			{#each data.workspace.organizations as org (org.id)}
				<a
					class="organization-card caudal-motion"
					href={resolve('/(auth)/org/[slug]/admin', { slug: org.slug })}
				>
					<div class="card-meta">
						<span
							>{org.role === 'owner'
								? m['orgAdminLayout.ownerBadge']()
								: m['orgAdmin.layout.staffBadge']()}</span
						><ArrowUpRight size={22} strokeWidth={1} />
					</div>
					<Waves class="my-10 h-12 w-12" strokeWidth={1} aria-hidden="true" />
					<h2>{org.name}</h2>
					<span class="card-action">{m['workspace.openSpace']()}<ArrowUpRight size={17} /></span>
				</a>
			{/each}
		</div>
	{:else}<section class="mt-12 space-y-6 border-t py-10">
			<h2 class="max-w-xl text-3xl font-normal tracking-tight">{m['workspace.noOrgTitle']()}</h2>
			<p class="max-w-xl text-muted-foreground">{m['workspace.noOrgText']()}</p>
			{#if data.canCreateOrganization}<Button href={resolve('/(auth)/create-org', {})}
					><Plus size={16} />{m['userMenu.createOrganization']()}</Button
				>{/if}
		</section>{/if}
	<p class="mt-8 max-w-3xl text-xs leading-relaxed text-muted-foreground">
		{m['workspace.paymentScope']()}
	</p>
</div>

<style>
	.organization-grid {
		display: grid;
		grid-template-columns: repeat(2, minmax(0, 1fr));
		gap: 24px;
		margin-top: 50px;
	}
	.organization-card {
		border: 1px solid hsl(var(--border));
		padding: 30px;
		transition:
			background 0.2s,
			transform 0.2s;
	}
	.organization-card:hover {
		background: hsl(var(--card));
		transform: translateY(-3px);
	}
	.card-meta,
	.card-action {
		display: flex;
		justify-content: space-between;
		align-items: center;
		gap: 15px;
		font-size: 11px;
	}
	.card-meta {
		color: hsl(var(--muted-foreground));
	}
	h2 {
		font-size: clamp(24px, 3vw, 40px);
		font-weight: 400;
		letter-spacing: -0.05em;
		line-height: 1.2;
	}
	.card-action {
		margin-top: 28px;
		padding-top: 20px;
		border-top: 1px solid hsl(var(--border));
	}
	@media (max-width: 640px) {
		.organization-grid {
			grid-template-columns: 1fr;
		}
		.organization-card {
			padding: 24px;
		}
	}
	@media (prefers-reduced-motion: reduce) {
		.organization-card {
			transition: none;
			transform: none !important;
		}
	}
</style>
