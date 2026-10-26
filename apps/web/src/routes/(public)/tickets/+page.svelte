<script lang="ts">
	import { resolve } from '$app/paths';
	import { ArrowUpRight, Ticket, QrCode, Users } from '@lucide/svelte';
	import * as m from '$lib/paraglide/messages.js';
</script>

<svelte:head
	><title>Caudal Tickets · Caudal Creativo</title><meta
		name="description"
		content={m['creative.ticketsCopy']()}
	/><meta name="robots" content="noindex,nofollow" /></svelte:head
>
<section class="creative-section" aria-labelledby="tickets-title">
	<p class="creative-eyebrow">Caudal Creativo / {m['creative.available']()}</p>
	<h1 id="tickets-title" class="creative-title">
		<!-- i18n-ignore: service name -->Caudal <em>Tickets</em>
	</h1>
	<p class="creative-intro">{m['creative.ticketsCopy']()}</p>
	<div class="actions">
		<a class="creative-pill" href={resolve('/(public)/events', {})}
			>{m['creative.allActivities']()}<ArrowUpRight size={20} aria-hidden="true" /></a
		><a class="creative-link" href={resolve('/(auth)/dashboard/tickets', {})}
			>{m['nav.myTickets']()}<ArrowUpRight size={18} aria-hidden="true" /></a
		>
	</div>
	<p class="scope">{m['workspace.paymentScope']()}</p>
</section>
<section class="creative-section operations" aria-labelledby="ticket-operations">
	<h2 id="ticket-operations">{m['caudal.flowTitle']()}</h2>
	<div class="operations-grid">
		<article>
			<Ticket size={26} strokeWidth={1} aria-hidden="true" />
			<h3>{m['caudal.stepTicket']()}</h3>
			<p>{m['caudal.ticketsDescription']()}</p>
			<a class="creative-link" href={resolve('/(auth)/dashboard/tickets', {})}
				>{m['nav.myTickets']()}<ArrowUpRight size={16} aria-hidden="true" /></a
			>
		</article>
		<article>
			<QrCode size={26} strokeWidth={1} aria-hidden="true" />
			<h3>{m['caudal.stepEntry']()}</h3>
			<p>{m['caudal.stepEntryCopy']()}</p>
			<a class="creative-link" href={resolve('/(auth)/producer', {})}
				>{m['workspace.producerSpace']()}<ArrowUpRight size={16} aria-hidden="true" /></a
			>
		</article>
		<article>
			<Users size={26} strokeWidth={1} aria-hidden="true" />
			<h3>{m['creative.publishLabel']()}</h3>
			<p>{m['workspace.producerIntro']()}</p>
			<a class="creative-link" href={resolve('/(auth)/producer', {})}
				>{m['caudal.producerAction']()}<ArrowUpRight size={16} aria-hidden="true" /></a
			>
		</article>
	</div>
</section>

<style>
	em {
		font-family: Georgia, serif;
	}
	.actions {
		display: flex;
		align-items: center;
		flex-wrap: wrap;
		gap: 25px;
	}
	.scope {
		font-size: 11px;
		line-height: 1.8;
		color: hsl(var(--muted-foreground));
		max-width: 650px;
		margin-top: 28px;
	}
	.operations {
		border-top: 1px solid hsl(var(--border));
	}
	h2 {
		font-size: clamp(30px, 4vw, 56px);
		letter-spacing: -0.05em;
		font-weight: 400;
		margin-bottom: 40px;
	}
	.operations-grid {
		display: grid;
		grid-template-columns: repeat(3, minmax(0, 1fr));
		gap: 38px;
	}
	h3 {
		font-weight: 400;
		font-size: 26px;
		letter-spacing: -0.04em;
		margin-block: 22px 14px;
	}
	article p {
		color: hsl(var(--muted-foreground));
		font-size: 13px;
		line-height: 1.8;
	}
	article a {
		margin-top: 20px;
	}
	@media (max-width: 767px) {
		.operations-grid {
			grid-template-columns: 1fr;
		}
		article {
			border-top: 1px solid hsl(var(--border));
			padding-top: 25px;
		}
	}
</style>
