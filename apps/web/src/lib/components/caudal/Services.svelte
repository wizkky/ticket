<script lang="ts">
	import { resolve } from '$app/paths';
	import { ArrowUpRight, Ticket, CalendarDays } from '@lucide/svelte';
	import * as m from '$lib/paraglide/messages.js';
</script>

<section class="creative-section services" aria-labelledby="services-title">
	<div class="creative-heading">
		<div>
			<p class="creative-eyebrow">Caudal Creativo / {m['creative.ecosystem']()}</p>
			<h2 id="services-title">{m['creative.servicesTitle']()}</h2>
		</div>
		<p>{m['creative.servicesCopy']()}</p>
	</div>
	<div class="services-grid">
		<article>
			<div class="service-meta">
				<Ticket size={22} strokeWidth={1.3} aria-hidden="true" /><span class="creative-status"
					>{m['creative.available']()}</span
				>
			</div>
			<h3><!-- i18n-ignore: product name -->Caudal <em>Tickets</em></h3>
			<p>{m['creative.ticketsCopy']()}</p>
			<a class="creative-link" href={resolve('/(public)/events', {})}
				>{m['creative.allActivities']()}<ArrowUpRight size={18} aria-hidden="true" /></a
			>
		</article>
		<article>
			<div class="service-meta">
				<CalendarDays size={22} strokeWidth={1.3} aria-hidden="true" /><span
					class="creative-status pending">{m['creative.development']()}</span
				>
			</div>
			<h3><!-- i18n-ignore: product name -->Caudal <em>Agenda</em></h3>
			<p>{m['creative.agendaCopy']()}</p>
			<a class="creative-link" href={resolve('/(public)/agenda', {})}
				>{m['creative.learnAgenda']()}<ArrowUpRight size={18} aria-hidden="true" /></a
			>
		</article>
	</div>
</section>

<style>
	.services-grid {
		display: grid;
		grid-template-columns: 1fr 1fr;
		border-block: 1px solid hsl(var(--border));
	}
	article {
		padding: 36px 40px 36px 0;
	}
	article + article {
		border-left: 1px solid hsl(var(--border));
		padding-left: 40px;
	}
	.service-meta {
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: 15px;
	}
	h3 {
		font-size: clamp(30px, 3.6vw, 54px);
		font-weight: 400;
		letter-spacing: -0.055em;
		margin-top: 36px;
	}
	em {
		font-family: Georgia, serif;
	}
	article > p {
		color: hsl(var(--muted-foreground));
		font-size: 14px;
		line-height: 1.8;
		max-width: 430px;
		margin-block: 18px 32px;
	}
	@media (max-width: 639px) {
		.services-grid {
			grid-template-columns: 1fr;
		}
		article,
		article + article {
			padding: 28px 0;
			border-left: 0;
		}
		article + article {
			border-top: 1px solid hsl(var(--border));
		}
	}
</style>
