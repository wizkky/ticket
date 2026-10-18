<script lang="ts">
	import { resolve } from '$app/paths';
	import { page } from '$app/stores';
	import { ArrowLeft, ChevronDown } from '@lucide/svelte';
	import { canPerformAction } from '$lib/utils/permissions';
	import StatusBadge from '$lib/components/common/StatusBadge.svelte';
	import * as m from '$lib/paraglide/messages.js';
	import type { LayoutData } from './$types';
	const { data, children }: { data: LayoutData; children: import('svelte').Snippet } = $props();
	const currentPath = $derived($page.url.pathname);
	const navItems = $derived([
		{
			href: resolve('/(auth)/org/[slug]/admin', { slug: data.organization.slug }),
			label: m['orgAdmin.nav.dashboard']()
		},
		{
			href: resolve('/(auth)/org/[slug]/admin/events', { slug: data.organization.slug }),
			label: m['orgAdmin.nav.events']()
		},
		{
			href: resolve('/(auth)/org/[slug]/admin/event-series', { slug: data.organization.slug }),
			label: m['orgAdmin.nav.eventSeries']()
		},
		{
			href: resolve('/(auth)/org/[slug]/admin/tickets', { slug: data.organization.slug }),
			label: m['orgAdmin.nav.tickets']()
		},
		{
			href: resolve('/(auth)/org/[slug]/admin/discount-codes', { slug: data.organization.slug }),
			label: m['orgAdmin.nav.discountCodes']()
		},
		{
			href: resolve('/(auth)/org/[slug]/admin/members', { slug: data.organization.slug }),
			label: m['orgAdmin.nav.members']()
		},
		{
			href: resolve('/(auth)/org/[slug]/admin/polls', { slug: data.organization.slug }),
			label: m['orgAdmin.nav.polls']()
		},
		{
			href: resolve('/(auth)/org/[slug]/admin/questionnaires', { slug: data.organization.slug }),
			label: m['orgAdmin.nav.questionnaires']()
		},
		{
			href: resolve('/(auth)/org/[slug]/admin/resources', { slug: data.organization.slug }),
			label: m['orgAdmin.nav.resources']()
		},
		{
			href: resolve('/(auth)/org/[slug]/admin/venues', { slug: data.organization.slug }),
			label: m['orgAdmin.nav.venues']()
		},
		{
			href: resolve('/(auth)/org/[slug]/admin/blacklist', { slug: data.organization.slug }),
			label: m['blacklistPage.tabBlacklist']()
		},
		...(data.isOwner
			? [
					{
						href: resolve('/(auth)/org/[slug]/admin/billing', { slug: data.organization.slug }),
						label: m['orgAdmin.nav.billing'](),
						badge:
							data.organization.is_stripe_connected &&
							(parseFloat(data.organization.platform_fee_percent) > 0 ||
								parseFloat(data.organization.platform_fee_fixed) > 0) &&
							(!data.organization.vat_country_code ||
								!data.organization.billing_address ||
								!data.organization.billing_name)
								? 'warning'
								: undefined
					},
					{
						href: resolve('/(auth)/org/[slug]/admin/financials', { slug: data.organization.slug }),
						label: m['orgAdmin.nav.financials']()
					},
					{
						href: resolve('/(auth)/org/[slug]/admin/integrations', {
							slug: data.organization.slug
						}),
						label: m['orgAdmin.nav.integrations']()
					}
				]
			: []),
		{
			href: resolve('/(auth)/org/[slug]/admin/announcements', { slug: data.organization.slug }),
			label: m['orgAdmin.nav.announcements']()
		},
		{
			href: resolve('/(auth)/org/[slug]/admin/embed', { slug: data.organization.slug }),
			label: m['orgAdmin.nav.embed']()
		},
		{
			href: resolve('/(auth)/org/[slug]/admin/settings', { slug: data.organization.slug }),
			label: m['orgAdmin.nav.settings']()
		}
	]);
	const canManageTickets = $derived(
		data.isOwner || canPerformAction(data.permissions, data.organization.id, 'manage_tickets')
	);
	const primary = $derived(
		navItems.filter(
			(item) =>
				item.href.endsWith('/admin') ||
				item.href.endsWith('/events') ||
				(item.href.endsWith('/tickets') && canManageTickets)
		)
	);
	const secondary = $derived(
		navItems.filter(
			(item) => !primary.includes(item) && !(item.href.endsWith('/tickets') && !canManageTickets)
		)
	);
	function isActive(href: string): boolean {
		// For the dashboard (admin root), only match exact path
		if (href.endsWith('/admin')) {
			return currentPath === href;
		}
		// For other paths, match exact or starting with path + '/'
		return currentPath === href || currentPath.startsWith(href + '/');
	}
</script>

<div class="caudal-workspace producer-shell" style="--admin-sticky-top: 5.5rem">
	<div class="producer-context">
		<a href={resolve('/(auth)/producer', {})}
			><ArrowLeft size={15} />{m['workspace.backToProducer']()}</a
		>
		<span class="org-name">{data.organization.name}</span>
		<StatusBadge
			tone="neutral"
			label={data.isOwner ? m['orgAdminLayout.ownerBadge']() : m['orgAdmin.layout.staffBadge']()}
			size="sm"
		/>
	</div>
	<div class="producer-grid">
		<aside class="producer-side" aria-label={m['orgAdmin.layout.mobileAdminNavigation']()}>
			<nav aria-label={m['workspace.producerSpace']()}>
				{#each primary as item (item.href)}
					<!-- eslint-disable-next-line svelte/no-navigation-without-resolve -- all nav paths are produced by resolve above -->
					<a href={item.href} aria-current={isActive(item.href) ? 'page' : undefined}
						>{item.label}</a
					>
				{/each}
			</nav>
			<details open={secondary.some((item) => isActive(item.href))}>
				<summary>{m['workspace.moreTools']()}<ChevronDown size={14} /></summary>
				<nav aria-label={m['workspace.moreTools']()}>
					{#each secondary as item (item.href)}
						<!-- eslint-disable-next-line svelte/no-navigation-without-resolve -- all nav paths are produced by resolve above -->
						<a href={item.href} aria-current={isActive(item.href) ? 'page' : undefined}
							>{item.label}{#if item.badge === 'warning'}<span class="text-xs text-destructive"
									>●</span
								>{/if}</a
						>
					{/each}
				</nav>
			</details>
		</aside>
		<div class="producer-content">{@render children()}</div>
	</div>
</div>

<style>
	.producer-shell {
		max-width: 1600px;
		margin: auto;
		padding: 0 clamp(20px, 4vw, 70px) 65px;
	}
	.producer-context {
		display: flex;
		align-items: center;
		gap: 22px;
		border-bottom: 1px solid hsl(var(--border));
		padding-block: 24px;
		min-width: 0;
	}
	.producer-context > a {
		display: flex;
		gap: 8px;
		align-items: center;
		font-size: 11px;
		color: hsl(var(--muted-foreground));
		flex-shrink: 0;
	}
	.org-name {
		margin-left: auto;
		font-family: 'Manrope', sans-serif;
		font-size: 16px;
		letter-spacing: -0.035em;
		overflow: hidden;
		text-overflow: ellipsis;
		white-space: nowrap;
	}
	.producer-grid {
		display: grid;
		grid-template-columns: 190px minmax(0, 1fr);
		gap: 45px;
		margin-top: 45px;
	}
	.producer-side {
		align-self: start;
		position: sticky;
		top: 112px;
	}
	.producer-side nav {
		display: flex;
		flex-direction: column;
		gap: 5px;
	}
	.producer-side a {
		display: flex;
		justify-content: space-between;
		gap: 10px;
		font-size: 12px;
		color: hsl(var(--muted-foreground));
		padding: 13px 15px;
		border-left: 1px solid transparent;
	}
	.producer-side a:hover {
		color: hsl(var(--foreground));
		background: hsl(var(--card));
	}
	.producer-side a[aria-current='page'] {
		border-color: hsl(var(--foreground));
		background: hsl(var(--card));
		color: hsl(var(--foreground));
	}
	details {
		border-top: 1px solid hsl(var(--border));
		margin-top: 22px;
		padding-top: 12px;
	}
	summary {
		display: flex;
		cursor: pointer;
		justify-content: space-between;
		gap: 12px;
		padding: 14px 15px;
		font-size: 11px;
		list-style: none;
	}
	summary::-webkit-details-marker {
		display: none;
	}
	.producer-content {
		min-width: 0;
	}
	details nav {
		max-height: 60svh;
		overflow: auto;
	}
	@media (max-width: 1023px) {
		.producer-grid {
			grid-template-columns: 155px minmax(0, 1fr);
			gap: 25px;
		}
		.producer-side a {
			padding-inline: 9px;
		}
		.producer-context {
			gap: 14px;
		}
	}
	@media (max-width: 767px) {
		.producer-context {
			flex-wrap: wrap;
			gap: 12px;
			padding-block: 20px;
		}
		.producer-context > a {
			width: 100%;
		}
		.org-name {
			margin-left: 0;
			flex: 1;
		}
		.producer-grid {
			display: block;
			margin-top: 0;
		}
		.producer-side {
			position: static;
			margin-bottom: 35px;
			border-bottom: 1px solid hsl(var(--border));
			padding-block: 12px;
		}
		.producer-side > nav {
			flex-direction: row;
			overflow: auto;
		}
		.producer-side > nav > a {
			white-space: nowrap;
			border-left: 0;
			border-bottom: 1px solid transparent;
			padding: 12px 14px;
		}
		details {
			margin-top: 8px;
			padding-top: 4px;
		}
		details nav {
			display: grid !important;
			grid-template-columns: 1fr 1fr;
			max-height: 400px;
		}
		.producer-side a {
			font-size: 11px;
		}
		.producer-content {
			padding-top: 0;
		}
	}
</style>
