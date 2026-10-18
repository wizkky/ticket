<script lang="ts">
	import { resolve } from '$app/paths';
	import { invalidateAll } from '$app/navigation';
	import { ArrowUpRight, Plus, CalendarDays, Ticket, ScanLine } from '@lucide/svelte';
	import PageHeader from '$lib/components/common/PageHeader.svelte';
	import StatusBadge from '$lib/components/common/StatusBadge.svelte';
	import Metrics from '$lib/components/workspace/Metrics.svelte';
	import { Button } from '$lib/components/ui/button';
	import { canPerformAction } from '$lib/utils/permissions';
	import { formatEventDate } from '$lib/utils/date';
	import * as m from '$lib/paraglide/messages.js';
	import type { PageData } from './$types';
	const { data }: { data: PageData } = $props();
	const org = $derived(data.organization);
</script>

<svelte:head><title>{org.name} · {m['workspace.producerSpace']()}</title></svelte:head>
<div class="space-y-12">
	<PageHeader
		volume="poster"
		kicker={m['workspace.workspaceKicker']()}
		title={m['workspace.eventsRecent']()}
		subtitle={org.name}
	>
		{#snippet actions()}{#if data.canCreateEvent}<Button
					href={resolve('/(auth)/org/[slug]/admin/events/new', { slug: org.slug })}
					><Plus size={16} />{m['dashboard.createEventButton']()}</Button
				>{/if}{/snippet}
	</PageHeader>
	{#if data.overview}
		<section aria-label={m['workspace.overview']()}>
			{#if data.overview.metrics}<Metrics metrics={data.overview.metrics} />{:else}<p
					class="rounded-lg border p-5 text-sm text-muted-foreground"
				>
					{m['workspace.permissionMetrics']()}
				</p>{/if}
		</section>
		<section>
			<div class="mb-6 flex flex-wrap items-center justify-between gap-3">
				<h2 class="text-lg font-medium">
					{m['workspace.eventCount']({ count: data.overview.event_count })}
				</h2>
				<a
					class="text-sm underline underline-offset-4"
					href={resolve('/(auth)/org/[slug]/admin/events', { slug: org.slug })}
					>{m['caudal.allEvents']()}</a
				>
			</div>
			<div class="producer-events">
				{#each data.overview.events as event (event.id)}<article>
						<div class="event-summary">
							<p class="text-xs text-muted-foreground">
								<time datetime={event.start}
									>{formatEventDate(event.start, 'America/Santiago')}</time
								>{#if event.city}
									· {event.city}{/if}
							</p>
							<h3>{event.name}</h3>
							<div class="mt-4 flex flex-wrap items-center gap-4">
								<StatusBadge
									tone={event.status === 'open' ? 'success' : 'neutral'}
									label={event.status === 'open'
										? m['orgAdmin.events.status.open']()
										: event.status === 'draft'
											? m['orgAdmin.events.status.draft']()
											: event.status === 'cancelled'
												? m['orgAdmin.events.status.cancelled']()
												: m['orgAdmin.events.status.closed']()}
								/>{#if event.issued !== null}<span class="text-xs text-muted-foreground"
										>{m['workspace.issued']()}: {event.issued} · {m['workspace.admissions']()}: {event.admissions}</span
									>{/if}
							</div>
						</div>
						<div class="event-actions">
							{#if canPerformAction(data.permissions, org.id, 'edit_event')}<Button
									variant="outline"
									size="sm"
									href={resolve('/(auth)/org/[slug]/admin/events/[event_id]/edit', {
										slug: org.slug,
										event_id: event.id
									})}>{m['orgAdmin.events.actions.edit']()}<ArrowUpRight size={14} /></Button
								>{/if}
							{#if event.status === 'open' && canPerformAction(data.permissions, org.id, 'check_in_attendees')}
								<Button
									size="sm"
									href={resolve('/(auth)/org/[slug]/admin/events/[event_id]/door', {
										slug: org.slug,
										event_id: event.id
									})}><ScanLine size={14} />{m['workspace.door']()}</Button
								>{/if}
						</div>
					</article>{:else}<div class="border-y py-12 text-muted-foreground">
						{m['workspace.noEvents']()}
					</div>{/each}
			</div>
		</section>
	{:else}<div role="alert" class="space-y-4 rounded-lg border p-6">
			<p>{m['workspace.dataUnavailable']()}</p>
			<Button variant="outline" onclick={() => invalidateAll()}>{m['financials.retry']()}</Button>
		</div>{/if}
	<div class="tasks">
		<a href={resolve('/(auth)/org/[slug]/admin/events', { slug: org.slug })}
			><CalendarDays size={24} strokeWidth={1} />
			<h2>{m['workspace.prepare']()}</h2>
			<p>{m['workspace.prepareCopy']()}</p></a
		>{#if canPerformAction(data.permissions, org.id, 'manage_tickets')}<a
				href={resolve('/(auth)/org/[slug]/admin/tickets', { slug: org.slug })}
				><Ticket size={24} strokeWidth={1} />
				<h2>{m['workspace.operate']()}</h2>
				<p>{m['workspace.operateCopy']()}</p></a
			>{/if}
	</div>
	<p class="border-t pt-5 text-xs leading-relaxed text-muted-foreground">
		{m['workspace.paymentScope']()}
	</p>
</div>

<style>
	.producer-events article {
		display: flex;
		justify-content: space-between;
		align-items: center;
		gap: 24px;
		border-top: 1px solid hsl(var(--border));
		padding: 26px 0;
	}
	.producer-events article:last-child {
		border-bottom: 1px solid hsl(var(--border));
	}
	h3 {
		font-size: clamp(22px, 2.5vw, 32px);
		font-weight: 400;
		letter-spacing: -0.045em;
		line-height: 1.25;
		margin-top: 10px;
	}
	.event-actions {
		display: flex;
		gap: 10px;
		flex-shrink: 0;
		flex-wrap: wrap;
	}
	.tasks {
		display: grid;
		grid-template-columns: 1fr 1fr;
		gap: 28px;
	}
	.tasks > a {
		border: 1px solid hsl(var(--border));
		padding: 28px;
	}
	.tasks h2 {
		font-size: 17px;
		margin-top: 24px;
		letter-spacing: -0.02em;
	}
	.tasks p {
		font-size: 13px;
		color: hsl(var(--muted-foreground));
		line-height: 1.8;
		margin-top: 12px;
		max-width: 400px;
	}
	@media (max-width: 767px) {
		.producer-events article {
			align-items: flex-start;
			flex-direction: column;
		}
		.tasks {
			grid-template-columns: 1fr;
		}
		.tasks > a {
			padding: 22px;
		}
	}
</style>
